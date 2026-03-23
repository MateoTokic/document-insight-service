# 📄 AI-driven Document Insight Service

This project implements an AI-powered document analysis service that allows users to:

- Upload PDF documents
- Extract text content
- Ask questions about the document
- Receive answers using a Retrieval-Augmented Generation (RAG) pipeline

The system is built using **FastAPI**, **sentence-transformers**, **FAISS**, **DistilBERT QA**, **Redis caching**, and **Gradio UI** for demonstration.

---

## 🚀 Features

- 📤 Upload PDF documents
- 🧠 Extract text using PyMuPDF
- 🔍 Retrieval-Augmented Generation (RAG) with FAISS
- ❓ Question answering using DistilBERT
- ⚡ Redis caching for repeated queries
- 🌐 REST API (FastAPI)
- 🎨 Simple UI with Gradio
- 🐳 Fully Dockerized setup

---

## 🧠 Approach & Design

### Architecture Overview

The system follows a **RAG (Retrieval-Augmented Generation)** pipeline:

1. **Upload PDF**
2. Extract text using **PyMuPDF**
3. Split text into chunks
4. Generate embeddings using **sentence-transformers**
5. Store embeddings in **FAISS**
6. On question:
   - Retrieve relevant chunks
   - Run **DistilBERT QA** on context
   - Return answer
7. Cache results in **Redis**

---

### 🛠️ Tools & Models Used

| Component | Tool | Why |
|----------|------|-----|
| Backend API | FastAPI | Fast, modern, auto-docs |
| PDF Extraction | PyMuPDF | Efficient and reliable |
| Embeddings | sentence-transformers | Lightweight and accurate |
| Vector Search | FAISS | Fast similarity search |
| QA Model | DistilBERT | Lightweight extractive QA |
| Cache | Redis | Improves performance |
| UI | Gradio | Quick demo interface |
| Containerization | Docker | Reproducibility |

---

## Setup

### Option 1: Docker (Recommended)

Spins up the FastAPI backend, Redis, and Gradio UI with one command. Requires Docker and Docker Compose installed.

```bash
docker compose up --build
```

Once running:

| Service | URL |
| --- | --- |
| API Docs (Swagger) | <http://localhost:8000/docs> |
| Gradio UI | <http://localhost:7860> |
| Health Check | <http://localhost:8000/api/health> |

The Docker Compose setup includes three services:
- `backend` — FastAPI app on port 8000
- `redis` — Redis 7 on port 6379
- `gradio` — Gradio UI on port 7860, connected to the backend internally

To stop everything:

```bash
docker compose down
```

---

### Option 2: Manual Installation

Prerequisites: Python 3.10+, Redis running locally (or via Docker).

**1. Clone and create a virtual environment**

```bash
git clone <your-repo-url>
cd document-insight-service

python -m venv venv
```

Activate it:

```bash
# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

**2. Install dependencies**

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**3. Start Redis**

If you don't have Redis installed locally, run it via Docker:

```bash
docker run -d --name redis-doc-insight -p 6379:6379 redis:7
```

**4. Start the FastAPI backend**

```bash
uvicorn app.main:app --reload
```

API docs at <http://127.0.0.1:8000/docs>

**5. Start the Gradio UI** (optional, in a separate terminal)

```bash
python gradio_ui/app.py
```

UI at <http://127.0.0.1:7860>

**6. Verify everything is running**

```bash
curl http://127.0.0.1:8000/api/health
```

Expected:

```json
{ "status": "ok", "redis": "connected" }
```

---

## API Reference

### `POST /api/upload` — Upload a PDF document

Request (multipart/form-data):

```bash
curl -X POST http://localhost:8000/api/upload \
  -F "file=@/path/to/document.pdf"
```

Response (`200 OK`):

```json
{
  "message": "PDF uploaded and processed successfully",
  "document_id": "3a275fd8-e313-4fc9-ba15-4319d8abc9e5",
  "filename": "document.pdf",
  "num_chunks": 42
}
```

### `POST /api/ask` — Ask a question about the uploaded document

Request (JSON):

```bash
curl -X POST http://localhost:8000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the monthly payment?"}'
```

Response (`200 OK`):

```json
{
  "question": "What is the monthly payment?",
  "answer": "$1,250",
  "retrieved_chunks": [
    "The monthly payment for the service is $1,250, due on the first of each month...",
    "Payment terms: Net 30. Monthly installment of $1,250 applies to all..."
  ],
  "cached": false
}
```

On repeated identical questions, `"cached": true` is returned and inference is skipped.

### `GET /api/health` — Health check

```bash
curl http://localhost:8000/api/health
```

Response:

```json
{ "status": "ok", "redis": "connected" }
```

## Example

After uploading invoice.pdf (available at storage/uploads/invoice.pdf) this is an answer for question: "What is total amount due?" As this file was not uploaded and no questions had been asked before this question, there was no answer caached.

<img width="1844" height="596" alt="image" src="https://github.com/user-attachments/assets/694ef0b3-6e9a-4d1f-a95b-0c110559414c" />

This is the answer for question: "What is the price for consulting services in EUR?" related to the same pdf file.
<img width="1769" height="565" alt="image" src="https://github.com/user-attachments/assets/27630f9b-7ecb-4e58-80e7-68cd2e37b9f2" />

At the bottom of the webpage user can see chunks that are created from this pdf file:
<img width="1825" height="656" alt="image" src="https://github.com/user-attachments/assets/ce690609-f373-45b2-ba16-22569dd0abae" />


## Author

Mateo Tokić
