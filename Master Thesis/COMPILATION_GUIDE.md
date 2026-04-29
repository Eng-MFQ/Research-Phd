# PhD Thesis Compilation Guide

This document explains how to compile the **Thesis_Master.tex** project into a professional PDF directly on your Mac.

## 1. Prerequisites (Installed on your System)
The following tools are already configured on your system and must be called by their full paths for maximum reliability:

*   **XeLaTeX:** Used for processing modern fonts and Arabic text.
    *   Path: `/Library/TeX/texbin/xelatex`
*   **BibTeX:** Used for generating the bibliography.
    *   Path: `/Library/TeX/texbin/bibtex`

## 2. Compilation Strategy (The 4-Pass Method)
To ensure that all References, Citations, List of Figures, and the Table of Contents are perfectly synchronized, you must run the tools in the following sequence:

1.  **Pass 1 (Initialize):** Run `xelatex`.
2.  **Pass 2 (Bibliography):** Run `bibtex`.
3.  **Pass 3 (Cross-References):** Run `xelatex` again.
4.  **Pass 4 (Final Polish):** Run `xelatex` one last time.

## 3. Terminal Commands
Open your terminal, navigate to the folder, and run these commands:

```bash
# Step 1: Initial compile
/Library/TeX/texbin/xelatex -interaction=nonstopmode Thesis_Master.tex

# Step 2: Process the Bibliography
/Library/TeX/texbin/bibtex Thesis_Master

# Step 3: Sync references
/Library/TeX/texbin/xelatex -interaction=nonstopmode Thesis_Master.tex

# Step 4: Final link
/Library/TeX/texbin/xelatex -interaction=nonstopmode Thesis_Master.tex
```

## 4. Common Warnings & Troubleshooting
*   **Overfull/Underfull \hbox:** These are common LaTeX warnings about text spacing. They do **not** stop the PDF from being generated. You can ignore them for now.
*   **Undefined References:** If you see "?? " instead of a citation number, it means you need to re-run the 4-pass sequence above.
*   **BibTeX "Repeated entry":** This occurs if your `.bib` file has duplicate keys. It is non-fatal; BibTeX will simply ignore the duplicates.

## 5. Working Directory
Ensure you are always working inside the following directory before running commands:
`/Users/mac/Dropbox/Agentix AI/Research Phd/Master Thesis/`
