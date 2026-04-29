# Agent Documentation: The PhD Thesis "Glue Strategy"

**Target Audience:** Future AI Agents (Antigravity, etc.) assisting the user.
**Context:** This project successfully merged six distinct research papers (R1-R6, covering NLP, SLR, Hadith AI, Fatawa AI, and Agentix RAG) into a single, cohesive LaTeX Master Thesis.

## The Architecture
The thesis utilizes a **"Glue Strategy"** where the user writes the overarching narrative ("The Golden Thread") combining introduction, transitions, and conclusion, and the agent computationally injects the heavy, peer-reviewed research papers into the document seamlessly.

### 1. The Master Draft (`Master Thesis/Thesis_Draft_v1.md`)
*   **Purpose:** Serving as the structural blueprint, this Markdown document compiles the Abstract, Introduction, Conclusions, and critically: **the Transition Statements**.
*   **Status:** It contains all the exact text intended for the final thesis. Future modifications to the thesis narrative should be modeled here first.

### 2. The Python Sanitizer (`scripts/latex_sanitizer.py`)
*   **Purpose:** Because each research paper (R1, R2, R3, R5) was originally written as a standalone compiled LaTeX file (often Overleaf templates for IEEE/ACM), they cannot be directly grouped together without throwing `Preamble` and `\begin{document}` conflicts.
*   **Mechanism:** The `latex_sanitizer.py` script automatically parses the target `.tex` files, stripping out headers, `\documentclass`, bibliography calls, and isolating the raw content. 
*   **Output:** It generates `*_cleaned.tex` files deposited straight into the `Master Thesis/chapters/` directory.

### 3. The Unified Bibliography (`Master Thesis/thesis_master.bib`)
*   **Purpose:** To prevent overlapping citation keys and broken reference chains, all individual `.bib` files from R1-R6 were appended into a single massive `thesis_master.bib` file. 

### 4. The Master LaTeX File (`Master Thesis/Thesis_Master.tex`)
*   This is the final compiling target.
*   It houses the universal global preamble (`biblatex`, `hyperref`, `booktabs`, etc.).
*   It physically injects the cleaned chapters via `\input{chapters/R1_cleaned.tex}`.
*   **Agent Rule:** **DO NOT** manually copy/paste the 100+ pages of the research papers into this file. Always use the `\input{}` schema to ensure modularity.

## Important Notes on Recent Updates
*   **R6 (Agentix Islam RAG):** Originally drafted in Markdown, its core logic (`rag_architectural_explanation.md`) has been fully mapped and integrated directly into Chapter 4 of the Master Thesis Draft and safely translated into the LaTeX compilation flow. 

## How to Proceed with Future Edits
1.  **If the user wants to change a transition or the Introduction:** Edit `Thesis_Draft_v1.md` and then mirror the changes to `Thesis_Master.tex` if they are LaTeX structural.
2.  **If the user wants to update the core of a Research Paper (e.g., Fatawa AI):** Update the specific standalone document inside its respective R-folder, and re-run `latex_sanitizer.py` to overwrite the `chapters/` output safely. 
3.  **Compilation:** The user runs `pdflatex` or `biber` directly against `Thesis_Master.tex`. If packages are missing, add them to the master preamble.
