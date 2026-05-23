import os
import firebase_admin
from firebase_admin import credentials, firestore
from google.genai import types
from langchain_chroma import Chroma
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from TocManager import find_page_scopes, get_pages_in_range
from langchain_cohere import CohereRerank
from langchain.retrievers import ContextualCompressionRetriever

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")  # set in environment
OPEN_AI_KEY = "sk-REPLACED"

try:
    firebase_admin.get_app()
except ValueError:
    cred = credentials.Certificate(f"./whilearn/firebase/service_account_key.json")
    firebase_admin.initialize_app(cred)
db = firestore.client()


def getResultReRanked(number, db):
    cohereKey = "REPLACED_COHERE_KEY"
    compressor = CohereRerank(cohere_api_key=cohereKey, model="rerank-multilingual-v3.0",
                              top_n=number)
    compression_retriever = ContextualCompressionRetriever(base_compressor=compressor,
                                                           base_retriever=db.as_retriever(
                                                               search_kwargs={"k": number}))
    return compression_retriever


def get_vector_store(book_id: str, embeddings):
    # This book was done in FAISS and I'm too lazy to reread it and add it to chroma
    if book_id == "Agtx-Azkar_Nawawi-6b24f2abfde641a1a6f89357890dd3b4":
        db_path = f"./whilearn/Agentix-Islam/books_db/{book_id}"
        return FAISS.load_local(
            db_path, embeddings, allow_dangerous_deserialization=True
        )

    api_key = 'ck-5ZouSNRMWbN4etnwop1WZ7hatQBt8nZRbeKo1A22kZvJ'
    tenant = '26b9b170-8f0f-48b3-ad2a-d9e7a3d94e4c'
    chroma_database = 'E7ya-3loom-eldeen'
    vector_store = Chroma(
        collection_name=book_id,
        embedding_function=embeddings,
        chroma_cloud_api_key=api_key,
        tenant=tenant,
        database=chroma_database,
    )
    return vector_store


async def query_vector_store(book_id: str, query: str, limit: int = 10):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001", google_api_key=GOOGLE_API_KEY)
    print(f"function called with q: {query}")
    vector_store = get_vector_store(book_id, embeddings)
    # results = vector_store.similarity_search(query, k=10)
    retriever = getResultReRanked(limit, vector_store)
    results = retriever.invoke(query)
    context = []
    for res in results:
        context.append({
            "page_content": res.page_content,
            "page_number": int(res.metadata.get("page_number")),
            "book_name": res.metadata.get("book_name"),
            "book_id": res.metadata.get("book_id"),
            "book_part_number": res.metadata.get("book_part_number", 0)  # send 0 back if the book doesn't have parts
        })
    return context


async def handle_functions(response, contents, advanced_search=True):
    if response.candidates[0].content.parts[0].function_call:
        function_call = response.candidates[0].content.parts[0].function_call
        #  In a real app, you would call your function here:
        print("$$" * 30)
        print(f"Function to call: {function_call.name}")
        print(f"Arguments: {function_call.args}")
        print("$$" * 30)
        if function_call.name == "query_vector_store":
            result = await query_vector_store(**function_call.args)
            print(">>" * 10)
            print(result)
            print(">>" * 10)
            if advanced_search:
                book_id = result[0]["book_id"]
                scope = await find_page_scopes(book_id, result[0]["page_number"])
                print("---ADVANCED---")
                range_result = await get_pages_in_range(book_id, scope["leaf"]["startPage"], scope["leaf"]["endPage"])
                print(">> SCOPE <<" * 20)
                print(scope)
                print(">> Range <<" * 20)
                print(range_result)
                print(">> END <<" * 20)
                contents.append(add_function_response_to_contents(function_call.name, range_result))
            else:
                contents.append(add_function_response_to_contents(function_call.name, result))

            print(">> $$ Answer $$<<" * 30)
            print(">> $$ Answer $$<<" * 30)
        if function_call.name == "find_page_scopes_function":
            result = find_page_scopes(**function_call.args)
            print(result)
            contents.append(add_function_response_to_contents(function_call.name, result))
            return result or None


def add_function_response_to_contents(function, results):
    return types.Content(
        role="tool",
        parts=[types.Part.from_function_response(
            name=function,
            response={"results": results},
        )],
    )


# Function Declaration
query_vector_store_function = {
    "name": "query_vector_store",
    "description": "Searches a vector store to find the most relevant document chunks based on a query.",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The search query to find relevant documents.",
            }
        },
        "required": ["query"],
    },
}
get_pages_in_range_function = {
    "name": "get_pages_in_range",
    "description": "Retrieves pages of a book within a specified range.",
    "parameters": {
        "type": "object",
        "properties": {
            "book_id": {
                "type": "string",
                "description": "The unique identifier of the book.",
            },
            "start_page": {
                "type": "integer",
                "description": "The starting page number of the range (inclusive).",
            },
            "end_page": {
                "type": "integer",
                "description": "The ending page number of the range (inclusive).",
            },
        },
        "required": ["book_id", "start_page", "end_page"],
    },
}
find_page_scopes_function = {
    "name": "find_page_scopes",
    "description": "search a book in details given a specific page number and a book part number.",
    "parameters": {
        "type": "object",
        "properties": {
            "page_number": {
                "type": "integer",
                "description": "The page number to find the scopes for.",
            },
            "book_part_number": {
                "type": "integer",
                "description": "The page number to find the scopes for.",
                "default": 0
            },
        },
        "required": ["page_number", "book_part_number"],
    },
}
