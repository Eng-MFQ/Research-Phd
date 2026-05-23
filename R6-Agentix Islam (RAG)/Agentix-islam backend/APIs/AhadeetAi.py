import json
from datetime import datetime

import firebase_admin
import pandas as pd
from firebase_admin import firestore
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CohereRerank
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import CSVLoader
from fastapi import FastAPI, HTTPException
from langchain_community.embeddings import OpenAIEmbeddings
from OpenAI.FatawaPrompts import getTranslateSystemInstruction, getFatwaTitleSystemInstruction, \
    getMufityHelperSysInsructions
from models.Constants import Chapters
import os
from models.FirebaseHelper import init_firebase
from models.Functions import tools
from models.Models import Message, RequestBody, TextInputTranslate, TextInputFatwaId, TextInputFatwaTitle
from openai import OpenAI
import requests

milvus_url = 'https://in03-f5f7c02f88e38e6.api.gcp-us-west1.zillizcloud.com/v2/vectordb/entities/'
milvus_key = '231ded61a218a9e4132f5f92f4b35c6fddefd402e18531b55fe4379e13572341d1080b7e90a7a77d59b6fdf119c9ba1cbe18830d'

databaseUrl = "whilearn/faiis/FatawaFull/fatawa"
sheetUrl = "whilearn/faiis/FatawaFull/fawat-ai.csv"


class AhadeethAi:
    def __init__(self, app: FastAPI):
        @app.get("/searchAhadeeth")
        def searchAhadeeth(query: str = "شروط قبول الدعاء", number: int = 3, is_mmr=False):
            """
                AI-Search for Ahadeeth Prophet Muhammad based on a given query from the book Ryiad Al Salheen .

                Parameters:
                - query (str): The search query. can accept any language
                - number (int): The number of Ahadeeth to retrieve, default is 3.
                - is_mmr (bool): If True, it will use the MMR (Maximal Marginal Relevance) algorithm for result diversification.
                                If False, it will use a similarity search algorithm for relevance.

                Returns:
                - List of Ahadeeth matching the search query.

                Example:
                ```python
                # Basic search for Ahadeeth related to "المال"
                searchAhadeeth(query="المال")

                # Customize the number of results to retrieve
                searchAhadeeth(query="money", number=5)

                # Apply the MMR algorithm for diversified results
                searchAhadeeth(query="المال", is_mmr=True)

                # Use a similarity search algorithm for relevance
                searchAhadeeth(query="money", is_mmr=False)
                ```


            """
            if number >= 50:
                number = 50
            try:
                os.environ['OPENAI_API_KEY'] = 'sk-REPLACED'
                embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
                db = FAISS.load_local(f"./whilearn/faiis/ahadeethAI/vectorDB", embeddings,
                                      allow_dangerous_deserialization=True)
                # if not is_mmr:
                #     relevant = db.as_retriever(search_kwargs={"k": number}).get_relevant_documents(query=f'{query}')
                # else:
                #     relevant = db.as_retriever(search_type="mmr",
                #                                search_kwargs={'k': number, 'fetch_k': 50}).get_relevant_documents(
                #         query=f'{query}')

                relevant = getResultReRanked(query, number, db)

                ahadeeth = []
                for h in relevant:
                    row = int(h.metadata["row"])
                    hadeeth_info = get_hadeeth(row)
                    print(hadeeth_info["title_ar_gpt4"])
                    # print(f'Hadeeth: {hadeeth_info["matin_ar"]}')
                    ahadeeth.append(hadeeth_info)

                return ahadeeth
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Error: {e}")

        @app.get("/getAhadeeth")
        def getAhadeeth(lastHadeethIdInBook: int = 0, chapter_id: int = 1):
            """
               Retrieve Ahadeeth ( of Prophet Muhammad) for a specific chapter from Ryiad Al Salheen's Book.

               Parameters:
               - lastHadeethIdInBook (int): The last known Hadeeth ID in the book for pagination. Send zero to fetch the first 20 Ahadeeth.
                                            To retrieve more Ahadeeth, provide the last Hadeeth ID you can find in a JSON item called 'idInBook'.
                                            Default to 0.

               - chapter_id (int): The ID of the chapter for which Ahadeeth are requested. Value ranges from 1 to 20, default to 1.

               Returns:
               - Ahadeeth JSON array of The requested Ahadeeth data. or Empty array if there are no Ahadeeth left in the specified chapter

               Example usage:
               ```python
               # Fetch the first 20 Ahadeeth for chapter 1
               getAhadeeth(chapter_id=1)
               >> this will return 20 Ahadeeth from chapter 1.

               # Fetch the next set of Ahadeeth after the Hadeeth with ID 25 in chapter 1
               getAhadeeth(lastHadeethIdInBook=25, chapter_id=1)
               >> this will return 20 Ahadeeth starting from hadeeth 26.

               ```

               """
            try:
                with open("./whilearn/faiis/ahadeethAI/Ryiad Al Salheen Dataset.json", 'r') as file:
                    data = json.load(file)

                filtered_hadeeth = filter(lambda x: x['chapterId'] == chapter_id, data)
                filtered_list = list(filtered_hadeeth)
                startIndex = 0
                if lastHadeethIdInBook != 0:
                    lastHadeethIdInBook += 1
                    lastHadeeth = list(filter(lambda x: x['idInBook'] == lastHadeethIdInBook, filtered_list))
                    if len(lastHadeeth) == 0:
                        return []
                    startIndex = filtered_list.index(lastHadeeth[0])
                return filtered_list[startIndex:min(startIndex + 20, len(filtered_list))]

            except FileNotFoundError:
                print(f"Error: File not found")
                raise HTTPException(status_code=400, detail="Error: File not found")
            except json.JSONDecodeError:
                print(f"Error: Invalid JSON format in the file")
                raise HTTPException(status_code=400, detail="Error: Invalid JSON format in the file")
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Error: {e}")

        @app.get("/getChapters")
        def getChapters():
            """
               Retrieve Chapters of Ryiad Al Salheen's Book.20 Chapters.
               You can use this ids to call #getAhadeeth() end point.
            """
            return Chapters

        @app.get("/searchFatwa", tags=["Fatawa"])
        def searchFatwaNew(query: str = "الخشوع", ):
            os.environ['OPENAI_API_KEY'] = 'sk-REPLACED'
            results = get_relevant_documents_from_milvus(query)
            try:
                firebase_admin.get_app()
            except ValueError:
                init_firebase()

            client = {'query': query, "timestamp": datetime.now()}
            firestore.client().collection("FatwaSearchCollection").document().set(client)

            return results["data"]

        @app.get("/searchFatwaWithSolimansIds")
        def searchFatwaNew(query: str = "الخشوع"):
            os.environ['OPENAI_API_KEY'] = 'sk-REPLACED'
            results = get_relevant_documents_from_milvus(query)

            try:
                firebase_admin.get_app()
            except ValueError:
                init_firebase()

            client = {'query': query, "timestamp": datetime.now()}

            # Process results and filter out entries with empty fatwa_id
            filtered_data = []
            for data in results["data"]:
                print(data)
                fatwaNewId = get_row_id_by_value(data["question"])
                if fatwaNewId:  # Only include non-empty fatwa_id
                    data["fatwa_id"] = fatwaNewId
                    filtered_data.append(data)

            firestore.client().collection("FatwaSearchCollection").document().set(client)

            return filtered_data

        @app.post("/getFatwaIdForSuleiman")
        def getFatwaForSuleiman(input: TextInputFatwaId):
            fatwaId = None
            question = input.fatwaQuestion.strip()
            fatwaNewId = get_row_id_by_value(question)
            print(fatwaNewId)
            if len(fatwaNewId) > 0:
                fatwaId = fatwaNewId[0]
            return {"fatwaId": fatwaId}

        @app.post("/translateFatwa")
        async def translateFatwa(input: TextInputTranslate):
            os.environ['OPENAI_API_KEY'] = 'sk-REPLACED'
            client = OpenAI()
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": [
                            {
                                "type": "text",
                                "text": getTranslateSystemInstruction()
                            }
                        ]
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": f"targeted language is {input.translateToLanguage}, tranlsate the follwing: - title: <{input.tileToTranslate}> -question: <{input.questionToTranslate}> -Answer: <{input.answerToTranslate}>"
                            }
                        ]
                    },

                ],

            )
            print("----- NEW -------")
            translated_text = response.choices[0].message.content.strip()
            print(translated_text)
            data = json.loads(translated_text)
            return data

        @app.post("/generateFatwaTitle")
        async def generateFatwaTitle(input: TextInputFatwaTitle):
            os.environ['OPENAI_API_KEY'] = 'sk-REPLACED'
            client = OpenAI()
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": [
                            {
                                "type": "text",
                                "text": getFatwaTitleSystemInstruction()
                            }
                        ]
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": f"Fatwa Question: {input.fatwaQuestion}.\n Fatwa Answer:  {input.fatwaAnswer}"
                            }
                        ]
                    },

                ],

            )
            fatwa_title = response.choices[0].message.content.strip()
            return {"fatwa_title": fatwa_title}

        @app.get("/searchFatwaOld")
        def searchFatwaOld(query: str = "الخشوع", ):
            os.environ['OPENAI_API_KEY'] = 'sk-REPLACED'
            try:
                os.environ['OPENAI_API_KEY'] = 'sk-REPLACED'
                embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
                db = FAISS.load_local(databaseUrl, embeddings, allow_dangerous_deserialization=True)
                relevant = getResultReRanked(query, 5, db)
                fatawaList = []
                print(f'user question: {query}')
                for fatwa in relevant:
                    row = int(fatwa.metadata["row"])
                    hadeeth_info = get_fataw(row)
                    print("---------------------hadeeth_info")
                    print(hadeeth_info)
                    print("---------------------")
                    print(f'title: {hadeeth_info["title"]}')
                    print(f'question: {hadeeth_info["question"]}')
                    print(f'answer: {hadeeth_info["answer"]}')
                    print(f'---')
                    fatawaList.append(hadeeth_info)
                return fatawaList
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Error: {e}")

        @app.get("/fatwaGpt")
        def fatwaGPT(query):
            try:
                try:
                    firebase_admin.get_app()
                except ValueError:
                    init_firebase()

                os.environ['OPENAI_API_KEY'] = 'sk-REPLACED'
                client = OpenAI()
                messagesAi = [{"role": "system", "content": f"Answer the given question from your knowledge {query}"}]
                fatwaList = searchFatwaNew(query)
                # gptPrompt = buildFatwaUserPrompt(fatwaList, query)
                # messagesAi.append({"role": "user", "content": gptPrompt})
                response = client.chat.completions.create(
                    model="ft:gpt-3.5-turbo-0125:whilelearnacademy:fatwagpt-full:9QLAWMoP",
                    messages=messagesAi,
                    max_tokens=500,
                )
                print(response.usage)
                result = {
                    "gptAnswer": response.choices[0].message.content,
                    "userQuestion": query,
                    "usage": {
                        "completion_tokens": response.usage.completion_tokens,
                        "prompt_tokens": response.usage.prompt_tokens,
                        "total_tokens": response.usage.total_tokens,
                    },
                    "fatawList": fatwaList,
                }
                addCostToFirebaseWeb(result)
                return result
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Error: {e}")

        @app.post("/searchHadithBrain")
        def searchHadithBrain(messages: list[Message], ):
            os.environ['OPENAI_API_KEY'] = 'sk-REPLACED'
            messagesAi = [{"role": "system",
                           "content": """
        I want you to act as a Muslim Sheikh:
        - Always treat people with Islamic greetings.
        - Start your conversation by saying that you are "SheikhGPT" and here to help them answering Fatwa.
        - Speak from the point of view of Islam.
        - Do not make assumptions about user requests; ask for clarification if a request is ambiguous.
        - Please ensure to answer in Arabic.
                                """}]
            messagesAi.extend([{"role": f"{m.role}", "content": f"{m.content}"} for m in messages])
            os.environ['OPENAI_API_KEY'] = 'sk-REPLACED'
            client = OpenAI()
            chat_response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messagesAi,
                tools=tools,
            )

            assistant_message = chat_response.choices[0].message
            print(assistant_message)
            isSendToSheikh = False
            question = ""
            fatwaList = []
            if chat_response.choices[0].message.tool_calls:
                function = chat_response.choices[0].message.tool_calls[0].function
                print(f"function ===> {function}")
                print(f"chat_response ----->{chat_response}")
                print("-------")
                if function.name == "function_search_fatwa":
                    assistant_message = {"content": "قمت بإيجاد هذه المصادر لك، هل تم الإجابة على سؤالك؟"}
                    question = function.arguments
                    question = json.loads(question)["question"]
                    print(question)
                    fatwaList = searchFatwaNew(question)
                else:
                    isSendToSheikh = True
                    assistant_message = {
                        "content": "عذرا على عدم المقدرة على الإجابة، سوف يتم إرسال المحادثة إلى شيخ وسوف نقوم بالإجابة على سؤالك قريبا"}

            return {"gptAnswer": assistant_message, "question": question, "fatwaList": fatwaList,
                    "isSendToSheikh": isSendToSheikh}

        @app.post("/searchHadithBrainNew")
        def searchHadithBrain(req: RequestBody, ):
            os.environ['OPENAI_API_KEY'] = 'sk-REPLACED'
            messagesAi = [{"role": "system",
                           "content": getMufityHelperSysInsructions()}]
            messages = req.data
            messagesAi.extend([{"role": f"{m.role}", "content": f"{m.content}"} for m in messages])
            os.environ['OPENAI_API_KEY'] = 'sk-REPLACED'
            client = OpenAI()
            chat_response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messagesAi,
                tools=tools,
            )
            assistant_message = chat_response.choices[0].message
            print(assistant_message)
            isSendToSheikh = False
            question = ""
            fatwaList = []
            if chat_response.choices[0].message.tool_calls:
                function = chat_response.choices[0].message.tool_calls[0].function
                print(f"function ===> {function}")
                print(f"chat_response ----->{chat_response}")
                print("-------")
                if function.name == "function_search_fatwa":
                    question = function.arguments
                    question = json.loads(question)["question"]
                    assistant_message = {
                        "content": "قمت بإيجاد هذه المصادر لك، في حال لم تجد إجابة الرجاء إرسال 'طلب التحدث إلى شيخ' وسوف أرسل سؤالك للكادر العلمي"}
                    print(question)
                    fatwaList = searchFatwaNew(question)
                else:
                    isSendToSheikh = True
                    assistant_message = {
                        "content": "عذرا على عدم المقدرة على الإجابة، سوف يتم إرسال المحادثة إلى الكادر العلمي وسوف نقوم بالإجابة على سؤالك قريبا"}

            return {"gptAnswer": assistant_message, "question": question, "fatwaList": fatwaList,
                    "isSendToSheikh": isSendToSheikh}

        def get_hadeeth(row):
            df = pd.read_csv(f"./whilearn/faiis/ahadeethAI/Ryiad Al Salheen Dataset.csv")
            row_dict = df.iloc[row].to_dict()
            return row_dict

        def getResultReRanked(query, number, db):
            cohereKey = "REPLACED_COHERE_KEY"
            compressor = CohereRerank(cohere_api_key=cohereKey, model="rerank-multilingual-v3.0",
                                      top_n=number)
            compression_retriever = ContextualCompressionRetriever(base_compressor=compressor,
                                                                   base_retriever=db.as_retriever(
                                                                       search_kwargs={"k": number}))
            return compression_retriever.get_relevant_documents(query)

        def buildFatwaUserPrompt(fatwaList, query):
            givenData = ""
            for hadeeth_info in fatwaList:
                givenData = givenData + f"""
        title: {hadeeth_info["title"].strip()}
        question: {hadeeth_info["question"].strip()}
        answer: {hadeeth_info["answer"].strip()}
         ---
        """
            gptPrompt = f"""
        User question:\n{query}

        Given Data:\n {givenData}
        """
            return gptPrompt.strip()

        def systemPrompt():
            return "You will be given a User question and Given Data: data related to the question.\n\nYour task is to read the data carefully, understand it, and then answer the user question based on the given data. Answer only in Arabic." \
                # "\n\nDo not invent an answer if the question is not related to the given data. Answer unrelated questions \n\nLastly, return only the answer in Arabic.\n\nData example: \n\nUser question: \nما حكم الخشوع في الصلاة\n\nGiven Data: \ntitle: حضور العقل وقت تكبيرة الإحرام\nquestion: ما حكم الخشوع أثناء تكبيرة الإحرام؟ وهل تبطل التكبيرة إذا لم نخشع قلبًا وعقلًا؟\nanswer: أقول وبالله التوفيق: الخشوع في الصلاة من التكبيرة إلى التسليمة مستحبّ، فلا تبطل الصلاة بتركه، والله أعلم.\n---\ntitle: فقدان الخشوع في الصلاة\nquestion: هل تعاد الصلاة إذا كانت بغير خشوع؟\nanswer: أقول وبالله التوفيق: الخشوع من مستحبات الصلاة، وهي صحيحة بدونه، لكن الخشوع روح الصلاة، وهو المقصود منها، وعليها أن نبقى نعالج أنفسنا حتى نحققه، والله أعلم.\n---\ntitle: الخشوع في الصلاة\nquestion: هل الخشوع من واجبات الصلاة؟ ومن لم يأت به في الصلاة، هل يعيد الصلاة؟\nanswer: أقول وبالله التوفيق: الخشوع من مستحبات الصلاة؛ لأنَّ تحقيقه يحتاج \nمجاهدة كبيرة من المصلي، والله أعلم.\n---\ntitle: أذكار الركوع والسجود\nquestion: ما هي أذكار الركوع والسجود؟\nanswer: أقول وبالله التوفيق: التسبيح ثلاثاً هو المسنون في الركوع والسجود، والله أعلم.\n---\ntitle: عدد التسبيحات في الركوع والسجود\nquestion: هل يجزئ تسبيحة واحدة في الركوع والسجود مع الاطمئنان؟\nanswer: أقول وبالله التوفيق: الطمأنينة واجبة في الركوع، وهي الاستقرار مقدار تسبيحة، وأما تلفظ التسبيح فهو سنة مؤكدة، وتتحقق السنة بثلاث تسبيحات، والله أعلم.\n\nYour answer:\nأقول وبالله التوفيق\nالصلاة الإبراهيمية سنة، فلا يلزم بتركها سجود السهو، والله أعلم."

        def get_fataw(row):
            df = pd.read_csv(sheetUrl)
            row_dict = df.iloc[row].to_dict()
            return row_dict

        def addCostToFirebaseWeb(result):
            result["timestamp"] = datetime.now()
            print(result)
            firestore.client().collection("Fatawa").document().set(result)


# Code used to clean the data from the .docx
def parse_fatwa(text):
    fatwa = {}
    # Extracting the fatwa number
    question_start = text.find("فتوى") + len("فتوى")
    question_end = text.find("السؤال:")
    fatwa['title'] = text[question_start:question_end].strip()

    # Extracting question and answer
    question_start = text.find("السؤال:") + len("السؤال:")
    question_end = text.find("الجواب:")
    fatwa['question'] = text[question_start:question_end].strip()

    answer_start = text.find("الجواب:") + len("الجواب:")
    answer_end = text.find("🙟", answer_start)
    fatwa['answer'] = text[answer_start:answer_end].strip()

    return fatwa


def extract_fatawas(text):
    fatawas = []
    start_index = text.find("فتوى")
    while start_index != -1:
        end_index = text.find("فتوى", start_index + 1)
        if end_index == -1:
            fatawas.append(text[start_index:])
            break
        fatawas.append(text[start_index:end_index])
        start_index = end_index
    return fatawas


def read_text_file(file_path="fawat-ai.txt"):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            textR = file.read()
        return textR
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"Error reading file '{file_path}': {e}")
        return None


def dict_to_csv(data, file_path="fawat-ai-old.csv"):
    try:
        df = pd.DataFrame(data)
        df.to_csv(file_path, index=False)
        print(f"CSV file '{file_path}' has been created successfully.")
    except Exception as e:
        print(f"Error converting list of dictionaries to CSV: {e}")


def indexWebsite(save_to="./whilearn/faiis/fatawaOld"):
    os.environ['OPENAI_API_KEY'] = 'sk-REPLACED'
    print("Indexing ....")
    loader = CSVLoader(file_path="whilearn/faiis/fatawaOld/fawat-ai-old.csv")
    texts = loader.load()
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    # db = FAISS.from_documents(texts, embeddings)
    # db.save_local(save_to)
    return texts


def get_embedding(text):
    os.environ['OPENAI_API_KEY'] = 'sk-REPLACED'
    client = OpenAI()
    text.strip()
    response = client.embeddings.create(
        model="text-embedding-3-large",
        input=[text]
    )
    # Extract the AI output embedding as a list of floats
    embedding = response.data[0].embedding
    return embedding


def get_relevant_documents_from_milvus(query: str):
    embedding = get_embedding(query)

    url = f"{milvus_url}/search"

    headers = {
        "Authorization": f'Bearer {milvus_key}',
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = {
        "collectionName": "fatawa",
        "outputFields": ["question", "answer", "chapter", "title"],
        "limit": 10,
        "data": [embedding]
    }
    data = json.dumps(payload)

    try:
        response = requests.post(url, data=data, headers=headers)
        response.raise_for_status()  # Raises a HTTPError if the response was an error
        return response.json()
    except requests.exceptions.RequestException as e:
        return None


def get_row_id_by_value(value, column_name="question"):
    """
    Reads a CSV file and returns the ID(s) of the row(s) where the value in the given column matches the specified value.

    Parameters:
        csv_file (str): The path to the CSV file.
        column_name (str): The name of the column to search in.
        value (str): The value to search for in the specified column.

    Returns:
        list: A list of IDs of the matching rows. If no matches are found, returns an empty list.
    """
    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv("./AgentixAi/fatawa/csv/fatawa/Fatwas Classified.csv")

        # Check if the column exists in the DataFrame
        if column_name not in df.columns:
            raise ValueError(f"Column '{column_name}' does not exist in the CSV file.")

        # Find rows where the value in the column matches the given value
        matching_rows = df[df[column_name] == value]

        # Return the IDs (assumes the ID column is named 'id')
        if 'id' in df.columns:
            return matching_rows['id'].tolist()[0]
        else:
            raise ValueError("The CSV file does not contain an 'id' column.")
    except Exception as e:
        print(f"Error: {e}")
        return []
