import re
from typing import List, Dict, Any
import pdfplumber

def extract_pages(pdf_path: str) -> List[Dict[str, Any]]:
    pages: List[Dict[str, Any]] = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            text = re.sub(r"\s+\n", "\n", text).strip()
            pages.append({"page": i, "text": text})
    return pages

# --- NEW: token estimate + chunker ---

def token_len_est(s: str) -> int:
    # rough: ~1 token per 0.75 words
    return max(1, int(len(s.split()) / 0.75))

def chunk_pages(pages: List[Dict[str, Any]],
                max_tokens: int = 900,
                overlap_tokens: int = 120) -> List[Dict[str, Any]]:
    """
    Make overlapping chunks with a sliding window.
    Each output: {"page": <page_number>, "text": <chunk_text>}
    """
    chunks: List[Dict[str, Any]] = []
    for p in pages:
        words = p["text"].split()
        if not words:
            continue
        n = len(words)
        start = 0
        while start < n:
            end = start
            buf = []
            cur_tokens = 0
            # grow a single chunk up to ~max_tokens
            while end < n and cur_tokens < max_tokens:
                buf.append(words[end]); end += 1
                cur_tokens = token_len_est(" ".join(buf))
            # finalize chunk
            text = " ".join(buf).strip()
            if text:
                chunks.append({"page": p["page"], "text": text})
            # slide window forward, keeping overlap
            next_start = max(0, end - int(overlap_tokens))
            if next_start <= start:     # safety for very short pages
                next_start = end
            start = next_start
    return chunks
