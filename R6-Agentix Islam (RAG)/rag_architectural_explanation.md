# Technical Implementation of the Agentic Islamic Fatwa (RAG) Framework

This document details the exact methodology, architecture, and logic used to construct the custom Retrieval-Augmented Generation (RAG) system for the Islamic Fatwa agent (as seen in the `R6-Agentix Islam (RAG)` project). This text is formulated to be easily integrated into the "Implementation" chapter of your PhD Thesis.

## 1. Data Ingestion & Structured Parsing
The foundational step involved digitizing and parsing classical Islamic jurisprudence texts into a machine-readable format while strictly preserving scholarly integrity.

*   **Batch Processing with LLMs:** The system uses the **Gemini 2.5 Pro** model via the Batch API to process raw manuscript pages at scale. 
*   **JSON Schema Enforcement:** To ensure structural consistency, a strict JSON schema was provided in the system prompt. The model was instructed to extract content page-by-page into a strict dictionary containing:
    *   `page_content`: The main text of the page.
    *   `page_number`: The specific, verifiable page number to ensure accurate citation later.
    *   `notes`: A specialized sub-object designed to uniquely capture classical text annotations, heavily separating `footnote`s (الهوامش) from `marginalia` (الحواشي).

## 2. Hierarchical Metadata & Table of Contents (TOC) Engineering
An intelligent RAG system requires semantic understanding of the book's structure, not just isolated flat text strings.

*   **TOC Flattening:** The books' structural Table of Contents were mapped into a hierarchical JSON array. Each section, chapter, or topic (e.g., "مقدمة الطبعة الجديدة") was mapped with a `title`, `startPage`, `endPage`, and its nesting `level` or `parentId` (pathIds and pathTitles).
*   **Markdown Synthesis:** The extracted raw JSON pages were subsequently stitched together to form a clean, continuous Markdown structure. Crucially, page numbers and separated footnotes were interleaved at designated points, maintaining the text's academic validity while making it parsable for chunking algorithms.

## 3. Vectorization and Database Construction
Before being queried, the structured text was transformed into embeddings designed for high-precision semantic search.

*   **Intelligent Text Splitting:** The compiled Markdown documents were chunked using LangChain’s `RecursiveCharacterTextSplitter`. Because Islamic jurisprudence requires high context retention, the chunks were set to `1000` characters with a safety overlap of `200` characters to prevent cutting off crucial conditions or *Ahadith*.
*   **Metadata Tagging:** Every individual chunk was injected with localized metadata referencing its origin: `book_id`, `book_name`, `book_part_number` (volume), and the exact `page_number`.
*   **Embeddings & Storage:** Text chunks were vectorized using Google's `gemini-embedding-001` model and stored immutably into a cloud-hosted **Chroma DB** (with an architectural fallback to local FAISS storage).
*   **Two-Stage Retrieval Mechanism (MMR + Reranking):** To solve the pervasive issue of irrelevant fatwa generation, the retrieval strategy utilizes a rigorous pipeline:
    1.  **Initial Retrieval:** Maximum Marginal Relevance (MMR) fetches the top *k=5* diverse but highly relevant chunks.
    2.  **Contextual Compression:** A `CohereRerank` (multilingual v3.0) model is layered on top to re-score and compress the returned nodes, pushing the most semantically relevant theological rulings to the absolute top of the context window.

## 4. Agentic Orchestration and Backend Logic (FastAPI)
The central intelligence of the framework is a dynamic orchestrator built with FastAPI, deploying **Gemini 3 Flash Preview** (and Gemini 2.5 Flash). It functions autonomously as an "Islamic Scholar" agent.

*   **Strict RAG Guardrails:** The LLM is given a definitive system instruction commanding it to act strictly as an Islamic scholar. It is forced to answer **only** from the retrieved context. If the ruling does not exist, it must declare its inability to answer ("المعلومة غير متوفرة في المصادر المقدمة") instead of hallucinating. It must answer in Arabic and maintain scholarly etiquette.
*   **Function Calling (The Agentic Component):** Rather than blindly performing similarity searches on every query, the LLM is equipped with specialized tools (functions):
    *   `query_vector_store`: Triggered automatically for general theological queries across the whole database.
    *   `find_page_scopes` & `get_pages_in_range`: Triggered if the user asks for a deep dive, or specifies a book part and page. The LLM intelligently navigates the previously defined TOC JSON tree to fetch specific, contiguous pages.
*   **Verification and Output Generation:** 
    *   The LLM enforces strict citation mechanisms natively structured from the chunk metadata (e.g., "(صفحة 584، الجزء 1)").
    *   It generates its final response in a strictly validated `JSON` format ensuring three keys: `answer` (the theological ruling in markdown), `relevant_questions` (generating 3 contextually aware follow-up discussion points to keep the user engaged in a learning loop), and `resources` (an array tracking all accessed page numbers and volumes).
    *   A continuous Database layer (`TocManager`) quietly intercepts the LLM's tool usages, storing token counts, search trajectories, and conversation history asynchronously using FastAPI's `BackgroundTasks`.
