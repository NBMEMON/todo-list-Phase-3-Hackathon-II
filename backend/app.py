"""
Hugging Face Space entry point for the FlowForge Todo API
"""
import gradio as gr
from main import app  # Import your FastAPI app
import uvicorn
import threading
import time

def run_fastapi_app():
    """Function to run the FastAPI application"""
    uvicorn.run(app, host="0.0.0.0", port=7860, log_level="info")

def start_api():
    """Start the FastAPI backend"""
    # Start the FastAPI app in a separate thread
    thread = threading.Thread(target=run_fastapi_app, daemon=True)
    thread.start()

    # Give the server a moment to start
    time.sleep(3)

    return "✅ API Server Started Successfully! Access the API at: https://naeeb-hackathon_phase_3_1.hf.space/"

# Create a simple Gradio interface to manage the API
with gr.Blocks(title="FlowForge Todo API") as demo:
    gr.Markdown("# 🚀 FlowForge Todo API Server")
    gr.Markdown("Backend API for the FlowForge Todo application running on Hugging Face Spaces")

    with gr.Row():
        with gr.Column():
            start_btn = gr.Button("🔌 Start API Server", variant="primary")
            status_output = gr.Textbox(label=">Status", interactive=False)

            start_btn.click(fn=start_api, inputs=[], outputs=[status_output])

    gr.Markdown("## 📡 API Endpoints")
    gr.Markdown("""
    Once started, access these endpoints:
    - `GET /`: Welcome message
    - `POST /api/v1/register`: User registration
    - `POST /api/v1/login`: User login
    - `GET /api/v1/users/me`: Get current user info
    - `GET /api/v1/tasks`: Get user's tasks
    - `POST /api/v1/tasks`: Create a new task
    - `PUT /api/v1/tasks/{task_id}`: Update a task
    - `DELETE /api/v1/tasks/{task_id}`: Delete a task
    """)

    gr.Markdown("## ℹ️ Notes")
    gr.Markdown("""
    - Click the 'Start API Server' button to initialize the backend
    - The API will be accessible at the Space URL with the appropriate endpoints
    - Database is initialized automatically on startup
    - Visit the Space URL followed by /docs to access the API documentation
    """)

# For Hugging Face Spaces, we need to launch the Gradio app
if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)