# Quickstart Guide: AI-Powered Conversational Todo System

## Prerequisites

Before getting started, ensure you have the following installed:

- **Node.js**: Version 18 or higher
- **npm**: Version 8 or higher (usually comes with Node.js)
- **Python**: Version 3.9 or higher
- **pip**: Python package installer (usually comes with Python)
- **Git**: Version control system
- **PostgreSQL-compatible database** (Neon recommended for cloud deployment)

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Backend Setup

Navigate to the backend directory and install dependencies:

```bash
cd backend
pip install -r requirements.txt
```

### 3. Frontend Setup

Navigate to the frontend directory and install dependencies:

```bash
cd frontend  # From project root
npm install
```

### 4. Environment Configuration

Copy the example environment file and configure your settings:

```bash
# In both backend and frontend directories
cp .env.example .env
```

Then update the `.env` files with your specific configuration:

**Backend (.env):**
- `DATABASE_URL`: Your PostgreSQL connection string
- `BETTER_AUTH_SECRET`: Secret key for authentication
- `JWT_SECRET`: Secret key for JWT signing
- `COHERE_API_KEY`: Your Cohere API key for AI services

**Frontend (.env.local):**
- `NEXT_PUBLIC_BASE_URL`: Base URL for your application
- `NEXT_PUBLIC_COHERE_API_KEY`: Your Cohere API key for AI services (if needed on frontend)

### 5. Database Setup

Run the database initialization script to create tables:

```bash
cd backend
python create_tables.py
```

### 6. Running the Application

#### Development Mode

Start the backend server:

```bash
cd backend
uvicorn main:app --reload
```

In a new terminal, start the frontend development server:

```bash
cd frontend
npm run dev
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000

## Using the AI Assistant

1. Navigate to the dashboard at http://localhost:3000/dashboard
2. Log in with your credentials
3. You'll see the AI assistant panel alongside your task list
4. Type natural language commands like:
   - "Add a task to buy groceries"
   - "Show me my tasks"
   - "Mark the first task as complete"
   - "Update the meeting task to tomorrow"
   - "Delete the old task"

## Key Features

### Natural Language Processing
- Communicate with your todo list using everyday language
- The AI understands various ways to express the same intent
- Supports both English and Urdu input

### Task Management
- Create, read, update, delete, and complete tasks
- Set priorities, due dates, and recurrence patterns
- Filter and search through your tasks

### Security
- All operations are secured with JWT authentication
- Users can only access their own tasks
- All AI-driven actions are validated through MCP tools

## Troubleshooting

### Common Issues

1. **Environment Variables Missing**
   - Ensure all required environment variables are set in both backend and frontend
   - Check that your database connection string is correct

2. **Cohere API Not Working**
   - Verify your Cohere API key is valid and properly set
   - Check that your account has sufficient quota for API calls

3. **Database Connection Issues**
   - Confirm your PostgreSQL database is running
   - Verify the connection string format in your environment variables

### Getting Help

- Check the logs in both backend and frontend for error messages
- Ensure all dependencies are properly installed
- Verify that ports 3000 and 8000 are not in use by other applications

## Next Steps

1. Customize the UI to match your branding
2. Extend the AI capabilities with additional features
3. Add more sophisticated natural language understanding
4. Implement additional security measures as needed
5. Deploy to production using your preferred hosting platform