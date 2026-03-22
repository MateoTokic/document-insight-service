import hashlib

def build_question_cache_key(document_id: str, question: str) -> str:
    normalized_question = question.strip().lower()
    question_hash = hashlib.md5(normalized_question.encode("utf-8")).hexdigest()
    return f"qa:{document_id}:{question_hash}"