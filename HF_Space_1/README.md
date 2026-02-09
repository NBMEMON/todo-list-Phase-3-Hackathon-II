---
title: Hackathon Phase 3 - Todo List Backend
emoji: 🚀
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 4.28.3
app_file: app.py
pinned: false
---

# FlowForge Todo API

This Hugging Face Space hosts the backend API for the FlowForge Todo application, developed as part of Hackathon Phase 3.

## Features

- User authentication and management
- Task creation, retrieval, updating, and deletion
- Secure API endpoints with JWT authentication
- Database persistence with SQLModel

## Technologies Used

- FastAPI: Modern, fast web framework for building APIs
- SQLModel: SQL databases in Python, with Type Hints
- Gradio: For the Hugging Face Space interface
- JWT: For secure authentication

## Usage

The backend provides RESTful API endpoints for managing todos. The Gradio interface allows you to start the backend service.

## API Endpoints

- `GET /`: Welcome message
- `POST /api/v1/register`: User registration
- `POST /api/v1/login`: User login
- `GET /api/v1/users/me`: Get current user info
- `GET /api/v1/tasks`: Get user's tasks
- `POST /api/v1/tasks`: Create a new task
- `PUT /api/v1/tasks/{task_id}`: Update a task
- `DELETE /api/v1/tasks/{task_id}`: Delete a task

## Status
Last updated: January 31, 2026

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference