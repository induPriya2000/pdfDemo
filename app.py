import os, uuid
from fastapi import FastAPI, UploadFile, File
from rag_core import extract_pages

app = FastAPI()
os.makedirs("data/uploads", exist_ok=True)

@app.get("/")
def health():
    return {"ok": True}

@app.post("upload")
async def upload(file: UploadFile = File(...)):
    doc_id = str(uuid.uuid4())[:8]
    raw = await file.read()
    path = f"data/uploads/{doc_id}__{file.filename}"
    with open(path, "wb") as f:
        f.write(raw)

    pages= extract_pages(path)
    page_count= len(pages)
    sample=pages[0]["text"][:200] if pages and pages[0]["text"] else ""
    return {
        "doc_id": doc_id,
        "filename": file.filename,
        "pages": page_count,
        "sample": sample
    }
