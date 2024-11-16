import pymupdf4llm

def pdf2md(pdf_path: str):
    md_text = pymupdf4llm.to_markdown(pdf_path)
    return md_text