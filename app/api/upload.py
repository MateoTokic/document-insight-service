from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
import os
from uuid import uuid4

from app.services.pdf_extractor import extract_text_from_pdf
from app.services.chunker import chunk_text
from app.services.shared_state import rag_service, state

router = APIRouter()

UPLOAD_FOLDER = "api/storage/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported for now.")
    
    document_id = str(uuid4())
    file_path = os.path.join(UPLOAD_FOLDER, f"{document_id}_{file.filename}")

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    extracted_text = extract_text_from_pdf(file_path) 

    if not extracted_text.strip():
        raise HTTPException(status_code=400, detail="No readable text found in PDF.")

    chunks = chunk_text(extracted_text, chunk_size=500, overlap=100)
    rag_service.build_index(chunks)

    state["current_document_id"] = document_id
    state["current_filename"] = file.filename
    
    return {
        "message": "PDF uploaded and processed successfully",
        "document_id": document_id,
        "filename": file.filename,
        "num_chunks": len(chunks)
    }