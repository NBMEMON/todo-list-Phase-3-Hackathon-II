from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)