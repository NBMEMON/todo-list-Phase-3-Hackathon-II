# Combined Skills List – Reusable Intelligence for Todo Hackathon Project

## Main Orchestrator Agent: Integration Agent
(Foundation for full-stack Phase II – frontend/backend sync, auth, routing)

- Secure JWT Token Management (issue from Better Auth, attach to headers, verify in FastAPI middleware with shared BETTER_AUTH_SECRET)
- Cross-Layer API Routing & Security (route calls to /api/{user_id}/tasks endpoints, enforce 401/403, user ownership filtering)
- Frontend-Backend Data Synchronization (update Next.js state after FastAPI response, handle optimistic UI updates)
- Error & Auth Debugging Delegation (pass errors to Debugger Agent)
- Subagent Orchestration (delegate specific tasks to Basic CRUD, Organization, Intelligent, Debugger agents)
- Code Generation for Integration Files (api.ts client, auth middleware.py, Better Auth config)

## Subagent 1: Basic CRUD Agent
(Core 5 features – Phase I migration to Phase II web)

- Task Creation (add new task with title, description, user_id)
- Task Deletion (remove by ID with ownership check)
- Task Update (modify title/description with ownership check)
- Task Listing (fetch user-specific tasks with completion status [ ] / [x])
- Completion Toggle (mark complete/incomplete via PATCH endpoint)
- SQLModel DB Operations (insert, update, delete, query filtered by authenticated user_id)

## Subagent 2: Organization Agent
(Intermediate level polish – future-proofing for usability)

- Priority Assignment (set high/medium/low on create/update)
- Tag/Category Management (add/remove tags like #work #home)
- Keyword Search (search across title, description, tags – case-insensitive)
- Advanced Filtering (by status, priority, tag, date)
- Task Sorting (by priority descending, title alphabetical, created_at newest/oldest)
- Enhanced List Presentation (filtered/sorted results with premium formatting)

## Subagent 3: Intelligent Agent
(Advanced features prep – for Phase III chatbot & beyond)

- Natural Language Due Date Parsing ("tomorrow 3pm", "next Monday", "in 2 days")
- Recurring Task Setup (daily, weekly on specific days, monthly, yearly)
- Auto-Rescheduling Logic (on complete → create next occurrence with updated due date)
- Overdue & Reminder Detection (highlight overdue tasks, show countdown for soon-due)
- Event Publishing Prep (future Kafka/Dapr integration for notifications)

## Subagent 4: Debugger & Error Resolution Agent
(Most important for real-time fixing – used across all phases)

- Error Log Parsing & Diagnosis (401/403, "Could not validate credentials", token undefined, ownership mismatch, DB connection, CORS)
- Root Cause Identification (JWT secret mismatch, missing header, wrong decode, env var issues, SQLModel filter bugs)
- Refined Fix Specification Generation (Markdown spec for the problematic component)
- Claude Code Fix Prompt Creation (ready-to-paste prompt to generate corrected code file)
- Test & Verification Guidance (steps to confirm the fix works after re-generation)

## How to Use This Combined Skills List

### In CLAUDE.md (root):
```
Primary Agent: Integration Agent
Sub-Agents & Skills: [paste the entire list above]
```

### In Agent Prompts: 
Reference this list when defining any agent, e.g.:
```
You are the Integration Agent. Use the following combined skills list: [paste list]
```