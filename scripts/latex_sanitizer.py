import os
import re

def sanitize_latex(input_path, output_path, chapter_title=None, is_markdown=False):
    if is_markdown:
        # Convert simple Markdown to LaTeX
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Super basic MD to LaTeX for headers
        content = re.sub(r'^# (.*?)$', r'\\section{\1}', content, flags=re.MULTILINE)
        content = re.sub(r'^## (.*?)$', r'\\subsection{\1}', content, flags=re.MULTILINE)
        content = re.sub(r'^### (.*?)$', r'\\subsubsection{\1}', content, flags=re.MULTILINE)
        content = re.sub(r'\*\*(.*?)\*\*', r'\\textbf{\1}', content)
        content = re.sub(r'\*(.*?)\*', r'\\textit{\1}', content)
        
        final_content = content
    else:
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract content between \begin{document} and \end{document}
        doc_match = re.search(r'\\begin\{document\}(.*?)\\end\{document\}', content, re.DOTALL)
        if doc_match:
            body = doc_match.group(1)
        else:
            body = content # fallback

        # Remove \maketitle, abstract environment
        body = re.sub(r'\\maketitle', '', body)
        body = re.sub(r'\\begin\{abstract\}.*?\\end\{abstract\}', '', body, flags=re.DOTALL)
        body = re.sub(r'\\title\{.*?\}', '', body, flags=re.DOTALL)
        body = re.sub(r'\\author\{.*?\}', '', body, flags=re.DOTALL)
        
        # Fix formatting for sections: since they go inside a chapter, we actually don't NEED to demote 
        # \section to \subsection IF we just let them be the \sections of the current \chapter. 
        # But wait! A conference paper uses \section for Introduction. In a book, \chapter{...} is followed by \section{Introduction}, which becomes 2.1 Introduction. 
        # So \section is ACTUALLY CORRECT! We DO NOT demote \section to \subsection!
        # This is serendipitous! 
        
        # We just need to remove \keywords if present
        body = re.sub(r'\\begin\{keywords\}.*?\\end\{keywords\}', '', body, flags=re.DOTALL)
        
        final_content = body.strip()

    # Wrap in chapter title if provided
    if chapter_title:
        header = f"\\chapter{{{chapter_title}}}\n\\label{{chap:{chapter_title.replace(' ', '_')}}}\n\n"
        final_content = header + final_content

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_content)
    print(f"Processed: {input_path} -> {output_path}")

def merge_bibs(bib_files, output_path):
    merged = ""
    for bib in bib_files:
        if os.path.exists(bib):
            with open(bib, 'r', encoding='utf-8') as f:
                merged += f"\n% From {bib}\n" + f.read() + "\n"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(merged)
    print(f"Merged {len(bib_files)} bib files into {output_path}")

if __name__ == "__main__":
    base_dir = "/Users/mac/Dropbox/Agentix AI/Research Phd"
    os.makedirs(os.path.join(base_dir, "chapters"), exist_ok=True)
    
    # R1
    r1_in = os.path.join(base_dir, "R1-2023_ilia_TransitionalWords_NLP_paper", "paper.tex")
    if not os.path.exists(r1_in):
        r1_in = os.path.join(base_dir, "R1-2023_ilia_TransitionalWords_NLP_paper", "conference_101719.tex")
    r1_out = os.path.join(base_dir, "chapters", "R1_cleaned.tex")
    sanitize_latex(r1_in, r1_out, "Traditional AI Applications in Education: NLP and Transitional Words")

    # R2
    r2_in = os.path.join(base_dir, "R2-Inno_conf_SLR_2025", "templates", "author.tex")
    r2_out = os.path.join(base_dir, "chapters", "R2_cleaned.tex")
    sanitize_latex(r2_in, r2_out, "Systematic Literature Review: Generative AI in Specialized Educational Domains")

    # R3
    r3_in = os.path.join(base_dir, "R3-Inno_conf_Ahadeth_AI_2025", "templates", "author.tex")
    r3_out = os.path.join(base_dir, "chapters", "R3_cleaned.tex")
    sanitize_latex(r3_in, r3_out, "Ahadith AI: Navigating Authenticity and Classification")

    # R5
    r5_in = os.path.join(base_dir, "R5-Fatwa AI", "paper", "main.tex")
    if not os.path.exists(r5_in):
        r5_in = os.path.join(base_dir, "R5-Fatwa AI", "paper_source", "aaai25.tex")
    r5_out = os.path.join(base_dir, "chapters", "R5_cleaned.tex")
    sanitize_latex(r5_in, r5_out, "Fatawa AI: Identifying the Hallucination Deficit in LLMs")

    # R6 (Markdown converted to LaTeX)
    r6_in = os.path.join(base_dir, "rag_architectural_explanation.md")
    r6_out = os.path.join(base_dir, "chapters", "R6_cleaned.tex")
    if os.path.exists(r6_in):
        sanitize_latex(r6_in, r6_out, "Agentix Islam: Architecting the Zero-Hallucination Framework", is_markdown=True)
    else:
        print("Could not find R6 markdown file at root, skipping R6...")

    # Merge Bibs
    bibs = [
        os.path.join(base_dir, "R1-2023_ilia_TransitionalWords_NLP_paper", "ref.bib"),
        os.path.join(base_dir, "R2-Inno_conf_SLR_2025", "references.bib"),
        os.path.join(base_dir, "R3-Inno_conf_Ahadeth_AI_2025", "references.bib"),
        os.path.join(base_dir, "R5-Fatwa AI", "paper", "main.bib"),
        os.path.join(base_dir, "R5-Fatwa AI", "paper_source", "aaai25.bib"),
    ]
    merge_bibs(bibs, os.path.join(base_dir, "thesis_master.bib"))
