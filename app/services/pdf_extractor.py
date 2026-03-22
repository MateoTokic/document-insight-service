import fitz

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text from a PDF using PyMuPDF.
    Returns one comined string from all pages.
    """
    full_text = []

    doc = fitz.open(pdf_path)

    for page_num, page in enumerate(doc):
        page_text = page.get_text("text")
        if page_text:
            full_text.append(f"--- Page {page_num + 1} ---\n{page_text.strip()}")

    doc.close()

    return "\n\n".join(full_text).strip()