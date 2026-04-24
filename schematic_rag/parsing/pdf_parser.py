
import fitz

def extract_text(pdf_path):
    doc = fitz.open(pdf_path)
    return "\n".join([p.get_text() for p in doc])
