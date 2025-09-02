import re
from typing import List, Dict, Any
import pdfplumber

def extract_pages(pdf_path: str) -> List[Dict[str, Any]]:
    pages: List[Dict[str, Any]]= []
    with pdfplumber.open(pdf_path) as pdf:

        for i, page in enumerate(pdf.pages, start=1):
            text= page.extract_text() or ""
            text= re.sub(r"\s+\n","\n", text).strip()
            pages.append({"page":i, "text": text})
    return pages
