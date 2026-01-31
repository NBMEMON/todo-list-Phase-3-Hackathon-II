# FlowForge Todo Application - Implementation Plan v2.0 (Phase II – Premium Edition)

## Technical Context

- **Application**: FlowForge - Premium Todo Web Application
- **Frontend**: Next.js 16+ with App Router
- **Backend**: FastAPI with SQLModel
- **Database**: Neon PostgreSQL (serverless)
- **Authentication**: Better Auth with JWT
- **UI Framework**: Tailwind CSS with custom design system
- **Animations**: Framer Motion
- **Styling**: Glassmorphism, dark mode first with light mode toggle
- **Colors**: Deep Navy (#0f172a), Electric Cyan (#06b6d4), Royal Purple (#7c3aed)

## Constitution Check

Based on the project constitution, this implementation plan adheres to:

- **Spec-Driven Development**: All code will be generated from this plan and the underlying spec
- **Multi-User Isolation**: Tasks will be filtered by authenticated user_id
- **Clean Architecture**: Layered design with RESTful API and responsive UI
- **Security First**: JWT-based auth for all endpoints
- **Reusable Intelligence**: Implementation will leverage subagents for different functionality areas

## Gates

- [x] Feature scope aligns with specification
- [x] Tech stack matches constitutional requirements
- [x] Security measures planned per constitution
- [x] Multi-user isolation addressed
- [x] No manual coding - all via Claude Code from specs

## Phase 0: Outline & Research

### Research Tasks

#### 1. JWT Token Management Policy
- **Decision**: Implement JWT access tokens expiring in 15 minutes with refresh tokens valid for 7 days
- **Rationale**: Balances security (short-lived access tokens) with user experience (longer refresh tokens)
- **Alternatives considered**: Longer-lived tokens (less secure), shorter refresh tokens (worse UX)

#### 2. JWT Token Management Implementation
- **Implementation**: Access tokens expire in 15 minutes with refresh tokens valid for 7 days
- **Rationale**: This policy balances security (short-lived access tokens) with user experience (longer refresh tokens)
- **Technical approach**: Use Better Auth for frontend authentication with JWT middleware in FastAPI

#### 3. Infinite Scroll vs Pagination
- **Decision**: Implement infinite scroll for task lists
- **Rationale**: Provides smoother user experience for large task lists, matches modern app patterns
- **Alternatives considered**: Traditional pagination, windowing (more complex to implement)

#### 4. Notification System Choice
- **Decision**: Implement toast notifications for all user actions
- **Rationale**: Unobtrusive feedback that doesn't interrupt user flow
- **Alternatives considered**: Modal dialogs (interruptive), dedicated notification area (less prominent)

#### 5. Data Retention Policy
- **Decision**: Retain user tasks indefinitely unless explicitly deleted
- **Rationale**: Matches user expectations for task management apps
- **Alternatives considered**: Automatic deletion after periods of inactivity

## Phase 1: Design & Contracts

### Data Model

#### Task Entity
- **id**: UUID (primary key)
- **user_id**: UUID (foreign key to user, required)
- **title**: String (max 255 characters, required)
- **description**: Text (optional, unlimited length)
- **completed**: Boolean (default: false)
- **created_at**: DateTime (auto-generated)
- **updated_at**: DateTime (auto-generated, updates on change)

#### User Entity (via Better Auth)
- **id**: UUID (primary key)
- **email**: String (unique, required)
- **name**: String (optional)
- **created_at**: DateTime (auto-generated)
- **updated_at**: DateTime (auto-generated)

### API Contracts

#### Authentication Endpoints
```
POST /api/auth/login
- Request: {email: string, password: string}
- Response: {token: string, refreshToken: string, user: {id, email, name}}
- Auth: None

POST /api/auth/register
- Request: {email: string, password: string, name: string}
- Response: {token: string, refreshToken: string, user: {id, email, name}}
- Auth: None
```

#### Task Management Endpoints
```
GET /api/{user_id}/tasks
- Query params: limit (default 20), offset (for pagination if needed)
- Response: [{id, title, description, completed, created_at, updated_at}]
- Auth: JWT required, verifies user_id matches token

POST /api/{user_id}/tasks
- Request: {title: string, description?: string}
- Response: {id, title, description, completed, created_at, updated_at}
- Auth: JWT required, verifies user_id matches token

GET /api/{user_id}/tasks/{task_id}
- Response: {id, title, description, completed, created_at, updated_at}
- Auth: JWT required, verifies user_id matches token and task belongs to user

PUT /api/{user_id}/tasks/{task_id}
- Request: {title?: string, description?: string}
- Response: {id, title, description, completed, updated_at}
- Auth: JWT required, verifies user_id matches token and task belongs to user

PATCH /api/{user_id}/tasks/{task_id}/complete
- Request: {completed: boolean}
- Response: {id, completed, updated_at}
- Auth: JWT required, verifies user_id matches token and task belongs to user

DELETE /api/{user_id}/tasks/{task_id}
- Response: 204 No Content
- Auth: JWT required, verifies user_id matches token and task belongs to user
```

### Quickstart Guide

#### Prerequisites
- Node.js 18+ 
- Python 3.9+
- PostgreSQL (or Neon account)
- Better Auth account

#### Setup Instructions
1. Clone the repository
2. Install backend dependencies: `pip install -r requirements.txt`
3. Install frontend dependencies: `npm install`
4. Set up environment variables:
   ```
   DATABASE_URL=postgresql://user:password@host:port/dbname
   BETTER_AUTH_SECRET=your-secret-key
   NEXT_PUBLIC_BASE_URL=http://localhost:3000
   ```
5. Run database migrations
6. Start backend: `uvicorn main:app --reload`
7. Start frontend: `npm run dev`
8. Visit http://localhost:3000

## Phase 2: Implementation Strategy

### Agent-Specific Implementation Notes

#### Integration Agent
- Coordinates between frontend and backend
- Manages JWT token flow between Better Auth and FastAPI
- Handles API routing and error handling

#### Basic CRUD Agent
- Implements core task operations (create, read, update, delete, toggle complete)
- Ensures user isolation at both frontend and backend
- Validates data before sending to backend

#### Organization Agent
- Handles task filtering, sorting, and search
- Manages priority and tagging features
- Optimizes task display and presentation

#### Intelligent Agent
- Implements infinite scroll functionality
- Manages notification system
- Handles offline synchronization if needed

## Architecture Overview

### Frontend Architecture
```
app/
├── layout.tsx (Root layout with theme provider)
├── page.tsx (Landing page)
├── dashboard/
│   ├── page.tsx (Dashboard with task list)
│   └── layout.tsx (Dashboard layout with sidebar)
├── login/
│   └── page.tsx (Login/Registration form)
├── globals.css (Global styles)
└── providers/
    └── theme-provider.tsx (Theme context provider)
components/
├── header.tsx
├── sidebar.tsx
├── task-card.tsx
├── task-list.tsx
├── floating-action-button.tsx
└── toast-notifications.tsx
lib/
├── auth.ts (Authentication utilities)
└── api.ts (API client with JWT handling)
styles/
└── globals.css
```

### Backend Architecture
```
backend/
├── main.py (FastAPI app entry)
├── models/
│   ├── __init__.py
│   └── task.py (SQLModel definitions)
├── api/
│   ├── __init__.py
│   └── tasks.py (Task endpoints)
├── auth/
│   ├── __init__.py
│   └── middleware.py (JWT validation)
├── database/
│   ├── __init__.py
│   └── session.py (Database session management)
└── utils/
    ├── __init__.py
    └── jwt.py (Token utilities)
```

## Security Considerations

1. JWT tokens validated on every request
2. User ownership verified for all task operations
3. Input validation on both frontend and backend
4. Rate limiting to prevent abuse
5. HTTPS enforcement in production
6. Secure storage of sensitive data

## Performance Targets

- API response time: <200ms for 95% of requests
- Support up to 100 concurrent users in free tier, 1000+ for paid tiers
- Page load time: <3 seconds for initial load, <1 second for subsequent navigation
- Handle minimum 10,000 tasks per user without performance degradation

## Testing Strategy

1. Unit tests for individual components
2. Integration tests for API endpoints
3. End-to-end tests for user flows
4. Security tests for authentication and authorization
5. Performance tests to validate targets