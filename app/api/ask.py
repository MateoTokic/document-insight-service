from fastapi import APIRouter, HTTPException
from app.models.schemas import AskRequest
from app.services.shared_state import rag_service, state
from app.services.cache_state import cache_service
from app.services.cache_utils import build_question_cache_key

router = APIRouter()


@router.post("/ask")
async def ask_question(request: AskRequest):
    question = request.question.strip()

    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
    
    document_id = state.get("current_document_id")
    if not document_id:
        raise HTTPException(status_code=400, detail="No document has been uploaded yet.")
    
    cache_key = build_question_cache_key(document_id, question)

    cached_result = cache_service.get(cache_key)
    if cached_result:
        return {
            "question": question,
            "answer": cached_result["answer"],
            "retreived_chunks": cached_result["retreived_chunks"],
            "cached":True
        }
    
    try:
        answer, retrieved_chunks = rag_service.answer_question(question, top_k=3)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    result = {
        "answer": answer,
        "retreived_chunks": retrieved_chunks
    }

    cache_service.set(cache_key, result, expire_seconds=3600)

    return {
        "question": question,
        "answer": answer,
        "retrieved_chunks": retrieved_chunks,
        "cached": False
    }