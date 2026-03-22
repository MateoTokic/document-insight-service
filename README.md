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

## 📦 Manual Installation

### 1. Clone repository

```bash
git clone https://github.com/YOUR_USERNAME/document-insight-service.git
cd document-insight-service

---

### 2. Create virtual environment

It is recommended to use a virtual environment to isolate project dependencies.

```bash
python -m venv venv

Activate:

Windows:
```bash
venv\Scripts\activate

Linux / macOS:
```bash
source venv/bin/activate

---

### 3. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt

---

### 4. Run Redis (required for caching)

Docker:
```bash
docker run -d --name redis-doc-insight -p 6379:6379 redis

---

### 5. Run FastAPI backend

```bash
uvicorn app.main:app --reload

Open:
http://127.0.0.1:8000/docs

---

### 6. Run Gradio UI

```bash
python gradio_ui/app.py

Open:
http://127.0.0.1:7860

---

### 7. Verify Redis connection

http://127.0.0.1:8000/api/health

---

## 🐳 Docker Setup

Run full system
```bash
docker compose up --build

Stop:
```bash
docker compose down

---

## 📡 API Examples

Upload:
POST /api/upload

Ask:
POST /api/ask

---

