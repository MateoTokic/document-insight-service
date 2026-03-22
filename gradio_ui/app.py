import os
import gradio as gr
import requests

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000/api")


def upload_pdf(file):
    if file is None:
        return "Please select a PDF file first."

    try:
        with open(file, "rb") as f:
            files = {
                "file": (file.split("\\")[-1].split("/")[-1], f, "application/pdf")
            }
            response = requests.post(f"{API_BASE_URL}/upload", files=files)

        if response.status_code == 200:
            data = response.json()
            return (
                "Document processed successfully.\n\n"
                f"Document ID: {data.get('document_id')}\n"
                f"Filename: {data.get('filename')}\n"
                f"Number of chunks: {data.get('num_chunks')}"
            )
        return f"Upload failed:\n{response.text}"

    except Exception as e:
        return f"Error during upload:\n{str(e)}"


def ask_question(question):
    if not question.strip():
        return "Please enter a question.", "No chunks to display."

    try:
        response = requests.post(
            f"{API_BASE_URL}/ask",
            json={"question": question}
        )

        if response.status_code == 200:
            data = response.json()
            answer = data.get("answer", "No answer returned.")
            retrieved_chunks = data.get("retrieved_chunks", [])
            cached = data.get("cached", False)

            answer_text = f"{answer}\n\nCached: {cached}"
            chunks_text = "\n\n---\n\n".join(retrieved_chunks) if retrieved_chunks else "No retrieved chunks."

            return answer_text, chunks_text
        else:
            return f"Request failed: {response.text}", ""

    except Exception as e:
        return f"Error during question answering:\n{str(e)}", ""


with gr.Blocks() as demo:
    gr.Markdown("# AI Document Insight Service")
    gr.Markdown(
        "This demo allows you to upload a PDF document and ask questions about its content "
        "using retrieval-augmented question answering."
    )

    with gr.Row():
        with gr.Column():
            gr.Markdown("## 1. Upload PDF")
            file_input = gr.File(
                label="Select PDF file",
                file_types=[".pdf"],
                type="filepath"
            )
            upload_button = gr.Button("Upload PDF")
            upload_status = gr.Textbox(label="Upload Status", lines=8)

        with gr.Column():
            gr.Markdown("## 2. Ask Questions")
            question_input = gr.Textbox(
                label="Question",
                placeholder="Example: What is the monthly payment?"
            )
            ask_button = gr.Button("Get Answer")
            answer_output = gr.Textbox(label="Answer", lines=4)

    gr.Markdown("## Retrieved Context")
    retrieved_chunks_output = gr.Textbox(label="Top Retrieved Chunks", lines=14)

    upload_button.click(
        fn=upload_pdf,
        inputs=file_input,
        outputs=upload_status
    )

    ask_button.click(
        fn=ask_question,
        inputs=question_input,
        outputs=[answer_output, retrieved_chunks_output]
    )

demo.launch(server_name="0.0.0.0", server_port=7860)