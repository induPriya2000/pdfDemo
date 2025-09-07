import os, uuid, time
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from rag_core import extract_pages, chunk_pages

app = FastAPI()
os.makedirs("data/uploads", exist_ok=True)

@app.get("/")
def health():
    return {"ok": True}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        return JSONResponse(status_code=400, content={"error": "Please upload a .pdf file."})

    try:
        doc_id = str(uuid.uuid4())[:8]
        raw = await file.read()
        path = f"data/uploads/{doc_id}__{file.filename}"
        with open(path, "wb") as f:
            f.write(raw)

        pages = extract_pages(path)
        chunks = chunk_pages(pages)

        return {
            "doc_id": doc_id,
            "filename": file.filename,
            "pages": len(pages),
            "chunks": len(chunks),
        }
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": f"Failed to process PDF: {str(e)}"})


    except Exception as e:
        # Return readable error instead of crashing the server
        return JSONResponse(
            status_code=400,
            content={"error": f"Failed to process PDF: {str(e)}"}
        )
