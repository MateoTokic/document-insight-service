from app.services.rag_service import RAGService

rag_service = RAGService()

state = {
    "current_document_id": None,
    "current_filename": None
}