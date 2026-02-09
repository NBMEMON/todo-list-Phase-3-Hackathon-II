import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import API routers
from api.tasks import router as tasks_router
from api.auth import router as auth_router
from api.users import router as users_router

# Import models to ensure they're registered with SQLModel
from models.user import User
from models.task import Task

app = FastAPI(title="FlowForge Todo API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to FlowForge Todo API"}

# Include API routers
app.include_router(auth_router, prefix="/api/v1", tags=["authentication"])
app.include_router(users_router, prefix="/api/v1", tags=["users"])
app.include_router(tasks_router, prefix="/api/v1", tags=["tasks"])

# Create database tables on startup
@app.on_event("startup")
def on_startup():
    from sqlmodel import SQLModel
    from database.session import engine
    print("Creating database tables...")
    SQLModel.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

# For Hugging Face Spaces, we'll create a Gradio interface that integrates with our FastAPI backend
import gradio as gr

def run_backend():
    """Function to run the backend API"""
    return "Backend is running and accessible via API endpoints!"

with gr.Blocks() as demo:
    gr.Markdown("# FlowForge Todo API")
    gr.Markdown("This space hosts the backend API for the FlowForge Todo application.")

    with gr.Row():
        with gr.Column():
            status_output = gr.Textbox(label="Status", interactive=False, value=run_backend())

    gr.Markdown("## API Endpoints")
    gr.Markdown("""
    - `GET /` - Welcome message
    - `POST /api/v1/register` - User registration
    - `POST /api/v1/login` - User login
    - `GET /api/v1/users/me` - Get current user info
    - `GET /api/v1/tasks` - Get user's tasks
    - `POST /api/v1/tasks` - Create a new task
    - `PUT /api/v1/tasks/{task_id}` - Update a task
    - `DELETE /api/v1/tasks/{task_id}` - Delete a task
    """)

# Run the application
if __name__ == "__main__":
    import uvicorn
    demo.launch(server_name="0.0.0.0", server_port=7860, show_error=True)
else:
    # Mount the Gradio app to the FastAPI app for Hugging Face Spaces at /ui path
    import gradio as gr
    app = gr.mount_gradio_app(app, demo, path="/ui")