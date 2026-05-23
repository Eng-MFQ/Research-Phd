import os
import uuid
from typing import Dict, Any
from pydantic import Field
from typing import Optional
import firebase_admin
from firebase_admin import credentials, firestore
from pydantic import BaseModel, TypeAdapter
from io import BytesIO
from pypdf import PdfReader, PdfWriter
from google import genai
from google.genai import types
from fastapi import File, UploadFile
from fastapi.responses import JSONResponse
import fitz  # PyMuPDF
import base64
from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
import pandas as pd
from langchain.retrievers.document_compressors import CohereRerank
from langchain.retrievers import ContextualCompressionRetriever
import io
import re
import json
import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

from APIs.AiUtilis import calculate_gemini_cost
from APIs.prompts.PdfPrompts import initial_default_prompt, \
    system_prompt_csv_no_translation, system_instructions_historical, system_h_html

# Make sure you set GEMINI_API_KEY in your environment!
# This is a placeholder, you should use an environment variable
API_KEY = os.environ.get("GEMINI_API_KEY")  # set in environment
OPEN_AI_KEY = "sk-REPLACED"

# Initialize the Firebase app ONCE when the application starts
cred = credentials.Certificate("./APIs/Sidiqqi/firebase.json")
sidiqqi_app = firebase_admin.initialize_app(cred, name='sidiqqi')
print("Firebase app 'sidiqqi' initialized successfully.")


class MetaData(BaseModel):
    """
    Represents the metadata for a financial table.
    """
    type: str = Field(description="The type of the financial statement ('normal' or 'note').")
    note_number: Optional[str] = Field(
        description="The note number if the table is a 'note' type, otherwise null.",
        default=None
    )


class ExtractedTable(BaseModel):
    """
    Represents a single financial table extracted from a document.
    """
    title_english: str = Field(description="The English title of the financial table, following specific naming logic.")
    table_english: str = Field(description="The table data formatted as a CSV string.")
    meta_data: MetaData = Field(description="An object containing metadata about the table.")
    has_error: bool = Field(
        description="Indicates if any numbers in the table were unreadable and replaced with '[Unclear number]'.")


class FinancialDocument(BaseModel):
    """
    Represents the complete JSON output for a financial document.
    """
    tables: List[ExtractedTable] = Field(description="A list of all tables extracted from the financial document.")


class FixedTable(BaseModel):
    table_english: str


class PdfExtractor(BaseModel):
    prompt: Optional[str] = initial_default_prompt
    model: Optional[str] = "gemini-2.5-flash"
    base64_image: str = ""
    page_number: int
    client_id: str = "pwc 12345"
    statement_year: int = 2020


class PdfExtractoFixer(BaseModel):
    model: Optional[str] = "gemini-2.5-flash"
    prompt: str = ""
    base64_image: str = ""
    wrong_table: str = ""


class AgentixAIPdf:
    def __init__(self, app: FastAPI):

        @app.post("/fix-table")
        async def generatCSV(fixer: PdfExtractoFixer):
            #  make sure to return the right json
            list_of_tables_adapter = TypeAdapter(FixedTable)
            response_schema_dict = list_of_tables_adapter.json_schema()

            contents = [
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_bytes(
                            mime_type="image/png",
                            data=base64.b64decode(fixer.base64_image),
                        ),
                        types.Part.from_text(
                            text=f"{fixer.prompt}. Note that previously you already extracted the table, and the result below has an error. # Wrong table: {fixer.wrong_table}"),
                    ],
                ),
            ]

            print(contents)

            client = genai.Client(api_key=API_KEY)
            response = client.models.generate_content(
                model=fixer.model,
                config=types.GenerateContentConfig(
                    thinking_config=types.ThinkingConfig(thinking_budget=-1),
                    response_mime_type="application/json",
                    response_schema=response_schema_dict,
                    system_instruction=system_prompt_csv_no_translation),
                contents=contents
            )
            fixed_table = json.loads(response.text)
            print(fixed_table)

            return fixed_table

        @app.post("/split-pdf-to-images")
        async def split_pdf_to_images(file: UploadFile = File(...), dpi: int = 300):
            if file.content_type != "application/pdf":
                raise HTTPException(400, "Only PDFs supported.")
            pdf_bytes = await file.read()
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")

            scale = dpi / 72
            images = []
            for page in doc:
                pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=False)
                img_bytes = pix.tobytes(output="png")
                images.append(base64.b64encode(img_bytes).decode())

            return JSONResponse({"pages": images})

        @app.post("/extract-tables")
        async def extract_tables(pdf: PdfExtractor):
            """
            Streams out the model's internal thoughts line by line,
            then finally yields a JSON object with all results.
            """
            list_of_tables_adapter = TypeAdapter(FinancialDocument)
            response_schema_dict = list_of_tables_adapter.json_schema()

            async def event_stream():
                client = genai.Client(api_key=API_KEY)
                all_results = []

                # Prepare the multimodal content payload
                contents = [
                    types.Content(
                        role="user",
                        parts=[
                            types.Part.from_bytes(
                                mime_type="image/png",
                                data=base64.b64decode(pdf.base64_image),
                            ),
                            types.Part.from_text(text=pdf.prompt),
                        ],
                    ),
                ]
                config = types.GenerateContentConfig(
                    thinking_config=types.ThinkingConfig(
                        thinking_budget=-1,
                        include_thoughts=True
                    ),
                    response_mime_type="application/json",
                    response_schema=response_schema_dict,
                    system_instruction=system_prompt_csv_no_translation
                )

                full_answer_text = ""
                last_chunk = None
                start_thinking = True

                # Stream the model output
                for chunk in client.models.generate_content_stream(
                        model=pdf.model,
                        contents=contents,
                        config=config,
                ):
                    # Each chunk may contain a “thought” or final text
                    candidate = chunk.candidates[0]
                    print(candidate)
                    for part in candidate.content.parts:
                        # If it’s a thought, yield it immediately
                        if part.thought and part.text:
                            if start_thinking:
                                yield "--Thinking--\n"
                                start_thinking = False

                            yield part.text + "\n"
                        # If it’s actual JSON text, accumulate it
                        elif part.text:
                            full_answer_text += part.text
                    last_chunk = chunk
                    print("reached Last chunk")

                # Once this image is done, parse out tables + usage
                try:
                    tables = json.loads(full_answer_text)["tables"]
                    print(tables)
                    tables = [
                        {**table, "id": f"table_{str(uuid.uuid4()).split('-')[0]}", "page_number": pdf.page_number} for
                        i, table in
                        enumerate(tables)]

                except json.JSONDecodeError:
                    raise HTTPException(
                        status_code=502,
                        detail="Failed to parse JSON from model for image"
                    )

                usage = {
                    "prompt_token_count": last_chunk.usage_metadata.prompt_token_count,
                    "candidates_token_count": last_chunk.usage_metadata.candidates_token_count,
                    "total_token_count": last_chunk.usage_metadata.total_token_count,
                    "thoughts_token_count": last_chunk.usage_metadata.thoughts_token_count,
                }
                calculate_gemini_flash_cost(usage)
                all_results = {
                    "client_id": pdf.client_id,
                    "statement_year": pdf.statement_year,
                    "tables": tables,
                    "usage": usage,

                }

                # Finally, stream out the complete JSON
                yield "--JSON--\n"
                json_results = json.dumps(all_results)
                await save_tables_to_db(all_results)
                print(json_results)
                print("--DONE--" * 20)
                yield json_results

            return StreamingResponse(event_stream(), media_type="text/plain")

        def split_pdf_pypdf2(file_bytes: bytes):
            reader = PdfReader(BytesIO(file_bytes))
            pages = []

            for page_num in range(len(reader.pages)):
                writer = PdfWriter()
                writer.add_page(reader.pages[page_num])

                buffer = BytesIO()
                writer.write(buffer)
                buffer.seek(0)
                pages.append(buffer.read())

            return pages

        @app.post("/split-pdf")
        async def split_pdf(file: UploadFile = File(...)):
            if file.content_type != "application/pdf":
                return {"error": "Uploaded file must be a PDF"}

            file_bytes = await file.read()
            pages = split_pdf_pypdf2(file_bytes)

            return {
                "total_pages": len(pages),
                "pages_info": [f"Page {i + 1} - {len(p)} bytes" for i, p in enumerate(pages)]
            }

        def sanitize_sheet_name(title: str, lang: str) -> str:
            """Sanitizes a string to be a valid Excel sheet name."""
            sanitized_title = re.sub(r'[\\/?*\[\]:]', '', title).strip()
            return f"{sanitized_title}_{lang}"[:31]

        @app.post("/generate-excel/")
        async def generate_excel(tables_json: list[dict]):
            output = BytesIO()

            # 1) Use XlsxWriter as the engine
            with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                workbook = writer.book
                worksheet = workbook.add_worksheet("Sheet1")
                writer.sheets["Sheet1"] = worksheet

                row_offset = 0
                for table_data in tables_json:
                    title = table_data.get("title_english", "Untitled Table")
                    csv_text = table_data.get("table_english", "")
                    if not csv_text:
                        continue

                    # write the title
                    title_df = pd.DataFrame([[title]])
                    title_df.to_excel(
                        writer,
                        sheet_name="Sheet1",
                        index=False,
                        header=False,
                        startrow=row_offset,
                        startcol=0
                    )
                    row_offset += 1

                    # parse CSV
                    try:
                        df = pd.read_csv(BytesIO(csv_text.encode("utf-8")))
                    except Exception:
                        df = pd.DataFrame()

                    # write the data
                    df.to_excel(
                        writer,
                        sheet_name="Sheet1",
                        index=False,
                        startrow=row_offset,
                        startcol=0
                    )

                    # now apply number format to all numeric columns
                    #  - create a format with comma separators
                    fmt = workbook.add_format({"num_format": "#,##0"})
                    #  - for each numeric column, figure out its 0-based column index
                    for col_idx, col_name in enumerate(df.columns):
                        if pd.api.types.is_numeric_dtype(df[col_name]):
                            # set width=None so we don’t override pandas’ auto‐width,
                            # and apply our thousands‐comma format
                            worksheet.set_column(
                                col_idx,  # first col
                                col_idx,  # last col
                                None,  # width
                                fmt  # cell format
                            )

                    # bump the row offset past this table + a blank row
                    row_offset += len(df) + 2

                writer.close()

            output.seek(0)
            headers = {
                "Content-Disposition": "attachment; filename=tables_data.xlsx",
                "Content-Type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            }
            return StreamingResponse(output, headers=headers)

        @app.post("/save-table/")
        async def save_tables_to_db(data: Dict[str, Any]):
            """
            Saves financial statement data to Firestore, flattening tables and
            creating a separate usage collection.

            Args:
                data (dict): The JSON data containing client info, tables, and usage.
            """
            db = firestore.client(app=sidiqqi_app)
            client_id = data.get("client_id")
            statement_year = data.get("statement_year")

            if not client_id or not statement_year:
                print("Client ID or statement year is missing. Aborting.")
                return

            # --- Save Statements ---
            statements_ref = db.collection("statements")

            for table in data.get("tables", []):
                doc_data = {
                    **table,  # Flatten the table dictionary
                    "client_id": client_id,
                    "statement_year": statement_year,
                }
                statements_ref.add(doc_data)

            # --- Save Usage ---
            usage_ref = db.collection("usage")
            usage_data = data.get("usage", {})
            if usage_data:
                usage_doc_data = {
                    **usage_data,
                    "client_id": client_id,
                    "statement_year": statement_year,
                }
                usage_ref.add(usage_doc_data)

            return {"success": True}

        async def get_statements_data(client_id: str, is_group_by_year: bool = True, ):
            """
            Retrieves and groups financial statements for a client from Firestore.

            Args:
                client_id (str): The ID of the client to retrieve statements for.
                is_group_by_year (str, optional): The field to group statements by.
                                          Accepts "year" or "buckets". Defaults to "year".

            Returns:
                dict: A dictionary where keys are the grouping values (e.g., year or bucket)
                      and values are lists of statement documents.
                      Returns None if no statements are found.
            """
            # Use your app instance
            db = firestore.client(app=sidiqqi_app)
            statements_ref = db.collection('statements')

            # Query for all statements belonging to the specific client
            query = statements_ref.where('client_id', '==', client_id).stream()

            # Determine the key to group by based on the function argument
            if not is_group_by_year:
                grouping_key = 'title_english'
            else:
                grouping_key = 'statement_year'

            statements_by_group = {}

            for doc in query:
                statement_data = doc.to_dict()

                # Get the value for the chosen grouping key
                group_value = statement_data.get(grouping_key)

                # If the group value exists, add the statement to the correct list
                if group_value:
                    if group_value not in statements_by_group:
                        statements_by_group[group_value] = []
                    statements_by_group[group_value].append(statement_data)

            if not statements_by_group:
                return None
            return statements_by_group

        async def get_statements_notes(client_id: str, statement_year: int, note_number: str):
            db = firestore.client(app=sidiqqi_app)
            # Query Firestore
            query = (
                db.collection("statements")
                .where("client_id", "==", client_id)
                .where("meta_data.note_number", "==", note_number)
                .where("statement_year", "==", statement_year)
            )

            results = query.stream()

            # Collect results into a list
            docs = [doc.to_dict() for doc in results]
            return docs

        def _canon_title(s: str) -> str:
            # Collapse whitespace, trim, and casefold for case-insensitive compares
            return re.sub(r"\s+", " ", (s or "")).strip().casefold()

        async def get_statements_data_grouped(
                client_id: str,
        ) -> Dict[str, List[dict]] | None:
            db = firestore.client(app=sidiqqi_app)
            statements_ref = db.collection("statements")

            # Only pull the fields we actually use
            query = (
                statements_ref
                .where("client_id", "==", client_id)
                .select(["title_english", "statement_year", "table_english"])
                .stream()
            )

            groups: Dict[str, List[dict]] = {}

            for doc in query:
                data = doc.to_dict() or {}
                title = data.get("title_english")
                if not title:
                    continue

                groups.setdefault(title, []).append(
                    {
                        "title_english": title,
                        "statement_year": data.get("statement_year"),
                        "table_english": data.get("table_english"),
                    }
                )

            return groups or None

        @app.get("/statements/{client_id}")
        async def get_statements_by_client(client_id: str = "pwc-test-123456", is_year: bool = True):
            statements = await get_statements_data(client_id, is_year)
            if statements is None:
                raise HTTPException(status_code=404, detail=f"No statements found for client ID: {client_id}")
            return statements

        @app.get("/notes/{client_id}/{statement_year}/{note_number}")
        async def get_statements_by_client(client_id: str = "pwc-test-123456", statement_year: int = 2018,
                                           note_number: str = "16"):
            statements = await get_statements_notes(client_id, statement_year, note_number)
            if statements is None:
                raise HTTPException(status_code=404, detail=f"No statements found for client ID: {client_id}")
            return statements

        @app.get("/statements/grouped/{client_id}")
        async def get_statements_by_client(client_id: str = "pwc-test-123456"):
            statements = await get_statements_data_grouped(client_id)
            if statements is None:
                raise HTTPException(status_code=404, detail=f"No statements found for client ID: {client_id}")
            return statements

        @app.get("/statements/historical/ai/{client_id}")
        async def get_historical_statements_by_client(client_id: str = "pwc-test-123456"):
            # This now calls the refactored function
            buckets_json = await get_statements_data_grouped(client_id)
            if buckets_json is None:
                raise HTTPException(status_code=404, detail=f"No statements found for client ID: {client_id}")
            prompt = "Create HTML table for all the seprate them by title: Statement of Cash Flows, Statement of Comprehensive Income, Statement of Financial Position"

            results = create_historical_gemini(buckets_json, prompt)
            db = firestore.client(app=sidiqqi_app)
            statements_ref = db.collection("historical")

            doc_data = {
                "client_id": client_id,
                "historical": results["table_english"],
            }
            statements_ref.add(doc_data)

            return results

        def create_historical_gemini(historical_json, user_prompt: str):
            # The rest of your code for calling the Gemini API is fine
            list_of_tables_adapter = TypeAdapter(FixedTable)
            response_schema_dict = list_of_tables_adapter.json_schema()
            contents = [f"{user_prompt} this is the json: {historical_json} "]
            print(contents)
            print("----starting AI -----")
            client = genai.Client(api_key=API_KEY)
            response = client.models.generate_content(
                model="gemini-2.5-pro",
                config=types.GenerateContentConfig(
                    thinking_config=types.ThinkingConfig(thinking_budget=-1),
                    response_mime_type="application/json",
                    response_schema=response_schema_dict,
                    system_instruction=system_h_html),
                contents=contents
            )
            fixed_table = json.loads(response.text)
            print(fixed_table)
            return fixed_table

        @app.get("/statements/historical/firestore/{client_id}", )
        async def get_historical_tables(client_id: str = "pwc-test-123456"):
            """
            Reads the 'historical' collection from Firestore and returns the
            'table_english' field from each document.
            """
            try:
                db = firestore.client(app=sidiqqi_app)
                collection_ref = db.collection("historical")
                docs = collection_ref.where("client_id", "==", client_id).stream()
                table_data = {}

                for doc in docs:
                    doc_data = doc.to_dict()

                    if "historical" in doc_data:
                        table_data = doc_data["historical"]

                # Return the list as a JSON response
                return {"historical": table_data}

            except Exception as e:
                # Basic error handling
                return {"error": str(e)}, 500

        @app.get("/fiqh/search/{query}/{number}", )
        async def get_historical_tables(query: str = """" من هو جابر بن زيد""",
                                        number: int = 5):
            db = FAISS.load_local(f"./APIs/Nabil/Faiss",
                                  OpenAIEmbeddings(api_key=OPEN_AI_KEY, model="text-embedding-3-large"),
                                  allow_dangerous_deserialization=True)

            # if not is_ranked:
            results = db.similarity_search(query, k=number, )
            # else:
            #     retriever = getResultReRanked(number, db)
            #     results = retriever.get_relevant_documents(query=f'{query}')
            final_results = []
            for res in results:
                final_results.append({"content": res.page_content,
                                      "source": res.metadata["page_number"]})
            return final_results

        def getResultReRanked(number, db):
            cohereKey = "REPLACED_COHERE_KEY"
            compressor = CohereRerank(cohere_api_key=cohereKey, model="rerank-multilingual-v3.0",
                                      top_n=number)
            compression_retriever = ContextualCompressionRetriever(base_compressor=compressor,
                                                                   base_retriever=db.as_retriever(
                                                                       search_kwargs={"k": number}))
            return compression_retriever
