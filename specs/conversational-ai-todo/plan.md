# AI-Powered Conversational Todo System - Implementation Plan

## 1. Technical Context

### 1.1 System Architecture
The AI-Powered Conversational Todo System will be built as an enhancement to the existing FlowForge todo application. The system will implement a conversational AI layer that sits between the user and the existing task management backend.

### 1.2 Technology Stack
- **Frontend**: Next.js 16+ with App Router, React for UI components
- **Backend**: FastAPI for API endpoints and agent orchestration
- **Database**: Neon PostgreSQL with SQLModel for ORM
- **Authentication**: Better Auth with JWT for user validation
- **AI/ML**: Cohere API for natural language processing
- **AI Agents**: Custom-built agents for intent parsing, tool execution, and response formatting
- **MCP Tools**: Custom tools for task operations (add, list, complete, update, delete, set recurring)

### 1.3 Integration Points
- Existing task management API endpoints
- Better Auth JWT validation system
- Neon PostgreSQL database with existing task schema
- Frontend dashboard UI with new conversational AI component

### 1.4 Unknowns
- Specific Cohere API usage patterns for intent classification
- Exact conversation state management approach
- Performance characteristics of AI processing

## 2. Constitution Check

Based on the project constitution (version 2.0.0), this implementation must adhere to the following principles:

### 2.1 AI-First Interaction
- All user actions must be driven through natural language conversation
- The system behaves as an intelligent assistant, not a command-based UI
- All functionality must be accessible through conversational interface

### 2.2 Agent-Based Architecture
- System intelligence is decomposed into reusable AI agents
- Each agent has a single, clearly defined responsibility
- Agents must be designed for reusability and clear separation of concerns

### 2.3 Security by Design
- All AI actions must be bound to authenticated user context
- No cross-user data access is allowed under any condition
- All AI-driven operations must enforce user isolation and data privacy

### 2.4 Deterministic Execution
- AI reasoning may be flexible, but all side effects must occur only through validated MCP tools
- No direct database access from the AI layer
- All operations must be traceable and auditable

### 2.5 Spec-Driven Development
- All behavior is defined through specifications and agent skills
- No manual business logic outside specs and skills
- Implementation follows spec and plan documents precisely

### 2.6 Intent-Driven Processing
- User input must be parsed into intent and structured entities before execution
- Natural language understanding is a core requirement for all user interactions

## 3. Gates

### 3.1 Security Gate
- ✅ JWT authentication will be validated for every AI-driven operation
- ✅ User isolation will be enforced through existing user_id associations
- ✅ MCP tools will validate user ownership before executing operations

### 3.2 Architecture Gate
- ✅ Agent responsibilities are clearly separated (intent parsing, tool execution, response formatting)
- ✅ MCP tools provide deterministic execution layer between AI and database
- ✅ Conversation state will be managed separately from task data

### 3.3 Performance Gate
- ✅ AI processing will be asynchronous to prevent blocking UI
- ✅ Caching mechanisms will be considered for repeated operations
- ✅ API rate limits will be respected

## 4. Phase 0: Research & Resolution of Unknowns

### 4.1 Research: Cohere API Usage Patterns
**Decision**: Use Cohere's classify endpoint for intent detection and generate endpoint for response formatting
**Rationale**: Cohere's classification API is well-suited for categorizing user input into predefined intent classes, while the generation API can create natural language responses
**Alternatives considered**: OpenAI GPT models, Hugging Face transformers, rule-based parsing

### 4.2 Research: Conversation State Management
**Decision**: Store conversation context in browser memory for session persistence with optional server-side storage for cross-device continuity
**Rationale**: Client-side storage reduces server load while maintaining conversation context during user sessions; server-side storage can be added later for enhanced functionality
**Alternatives considered**: Server-side sessions, local storage, URL parameters

### 4.3 Research: AI Processing Performance
**Decision**: Implement loading indicators and timeout handling for AI responses; cache common responses where appropriate
**Rationale**: Provides user feedback during processing and handles potential API delays gracefully
**Alternatives considered**: Preloading models, edge computing, simpler rule-based responses

## 5. Phase 1: Design & Contracts

### 5.1 Data Model

#### 5.1.1 Task Entity (Extends existing model)
- **id**: String (Primary Key)
- **title**: String (Required, max 200 chars)
- **description**: String (Optional, max 1000 chars)
- **completed**: Boolean (Default: false)
- **priority**: Integer (1-5, 1 being highest)
- **due_date**: DateTime (Optional)
- **recurrence_pattern**: String (Optional, values: daily, weekly, monthly, custom)
- **user_id**: String (Foreign Key to User)
- **created_at**: DateTime (Auto-generated)
- **updated_at**: DateTime (Auto-generated)

#### 5.1.2 Conversation Thread Entity (New)
- **id**: String (Primary Key)
- **user_id**: String (Foreign Key to User)
- **session_id**: String (Unique session identifier)
- **messages**: JSON (Array of message objects with role, content, timestamp)
- **context**: JSON (Current conversation context/state)
- **created_at**: DateTime (Auto-generated)
- **updated_at**: DateTime (Auto-generated)

### 5.2 API Contracts

#### 5.2.1 MCP Tools API
```
POST /api/v1/mcp/add_task
Headers: Authorization: Bearer {JWT_TOKEN}
Body: {
  "title": string,
  "description"?: string,
  "due_date"?: string,
  "recurrence_pattern"?: string,
  "priority"?: integer,
  "tags"?: string[]
}
Response: {
  "success": boolean,
  "task_id": string,
  "message": string
}

GET /api/v1/mcp/list_tasks
Headers: Authorization: Bearer {JWT_TOKEN}
Query Params: {
  "filter_status"?: "completed"|"pending"|"all",
  "filter_priority"?: integer,
  "search_keyword"?: string
}
Response: {
  "success": boolean,
  "tasks": Task[],
  "count": integer
}

POST /api/v1/mcp/complete_task
Headers: Authorization: Bearer {JWT_TOKEN}
Body: {
  "task_id": string
}
Response: {
  "success": boolean,
  "message": string
}

POST /api/v1/mcp/update_task
Headers: Authorization: Bearer {JWT_TOKEN}
Body: {
  "task_id": string,
  "title"?: string,
  "description"?: string,
  "due_date"?: string,
  "recurrence_pattern"?: string,
  "priority"?: integer,
  "tags"?: string[]
}
Response: {
  "success": boolean,
  "message": string
}

POST /api/v1/mcp/delete_task
Headers: Authorization: Bearer {JWT_TOKEN}
Body: {
  "task_id": string
}
Response: {
  "success": boolean,
  "message": string
}

POST /api/v1/mcp/set_recurring
Headers: Authorization: Bearer {JWT_TOKEN}
Body: {
  "task_id": string,
  "pattern": "daily"|"weekly"|"monthly"
}
Response: {
  "success": boolean,
  "message": string
}
```

#### 5.2.2 Conversational AI API
```
POST /api/v1/chat/process
Headers: Authorization: Bearer {JWT_TOKEN}
Body: {
  "message": string,
  "session_id"?: string
}
Response: {
  "success": boolean,
  "response": string,
  "action_taken"?: string,
  "session_id": string
}
```

### 5.3 Quickstart Guide

#### 5.3.1 Prerequisites
- Node.js 18+ for frontend
- Python 3.9+ for backend
- PostgreSQL-compatible database (Neon recommended)
- Better Auth account for authentication
- Cohere API key for AI services

#### 5.3.2 Setup Instructions
1. Clone the repository
2. Install backend dependencies: `cd backend && pip install -r requirements.txt`
3. Install frontend dependencies: `cd frontend && npm install`
4. Set up environment variables (see .env.example)
5. Run database migrations: `cd backend && python create_tables.py`
6. Start backend: `cd backend && uvicorn main:app --reload`
7. Start frontend: `cd frontend && npm run dev`

#### 5.3.3 Running the Application
- Backend API will be available at http://localhost:8000
- Frontend will be available at http://localhost:3000
- Access the dashboard at http://localhost:3000/dashboard to use the AI assistant

## 6. Phase 2: Implementation Approach

### 6.1 Agent Architecture
The system will implement four main agents as specified:

1. **Main Orchestrator Agent**: Coordinates the overall conversation flow
2. **Intent Parser Agent**: Identifies user intent and extracts entities
3. **MCP Tool Executor Agent**: Executes validated operations via MCP tools
4. **Reply Formatter Agent**: Creates natural language responses

### 6.2 Implementation Sequence
1. Implement MCP tools with JWT validation
2. Create the four AI agents with defined responsibilities
3. Integrate agents with existing frontend
4. Add conversation state management
5. Implement bilingual support (English/Urdu)
6. Add UI enhancements and loading states

### 6.3 Quality Assurance
- Unit tests for each agent component
- Integration tests for agent coordination
- End-to-end tests for complete conversation flows
- Security tests for JWT validation and user isolation