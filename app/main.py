from fastapi import FastAPI
from app.api.upload import router as upload_router
from app.api.ask import router as ask_router
from app.api.health import router as health_router

app = FastAPI(
    title="Document Insight Service",
    description="AI-Powered service to extract insights from document",
    version="1.0"
)

app.include_router(upload_router, prefix="/api", tags=["Upload"])
app.include_router(ask_router, prefix="/api", tags=["QA"])
app.include_router(health_router, prefix="/api", tags=["Health"])

@app.get("/")
def root():
    return {"message": "Document Insight Service running"}