---
id: 1
title: "Update Project Constitution"
stage: constitution
date_iso: 2026-01-11
surface: agent
model: Qwen Code
feature: todo-app
branch: main
user: User
command: "/sp.constitution Project: Todo Full-Stack Web Application (Hackathon Phase II)"
labels: ["constitution", "todo-app", "spec"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - ".specify/memory/constitution.md"
tests_yaml: []
---

# Update Project Constitution

## Original Prompt

```
/sp.constitution Project: Todo Full-Stack Web Application (Hackathon Phase II)
Core principles:

Spec-Driven Development: All code generated via Claude Code from refined specs
Multi-User Isolation: Tasks filtered by authenticated user_id
Clean Architecture: Layered design with RESTful API and responsive UI
Security First: JWT-based auth for all endpoints

Key standards:

No manual coding: Refine specs until Claude Code outputs correctly
Monorepo Organization: Use Spec-Kit for /specs/ structure (features, api, database, ui)
Authentication: Better Auth on frontend, JWT verification in FastAPI middleware
Persistence: SQLModel models with Neon PostgreSQL
API Endpoints: GET/POST/PUT/DELETE/PATCH under /api/{user_id}/tasks with ownership enforcement

Constraints:

Features: Implement only 5 Basic Level (Add, Delete, Update, View, Mark Complete) as web app
Tech Stack: Next.js 16+ (App Router), FastAPI, SQLModel, Neon Serverless PostgreSQL, Better Auth
Deployment: Vercel for frontend; local Docker Compose for dev
Windows Dev: Use WSL 2
Bonus Focus: Reusable Intelligence via subagents (+200 points)

Success criteria:

Functional multi-user web app with persistent data
Secure API: 401/403 errors for unauthorized access
Spec Traceability: All features linked to specs history
Demo Video: <90 seconds showing features and auth flow
Submission: GitHub repo, Vercel link, video via form
```

## Response Summary

Updated the project constitution file (.specify/memory/constitution.md) with specific principles and standards for the Todo Full-Stack Web Application project. The new constitution includes:

- Core principles: Spec-Driven Development, Multi-User Isolation, Clean Architecture, Security First, and Reusable Intelligence
- Additional standards covering tech stack requirements, API design standards, and persistence standards
- Development workflow guidelines with feature implementation, deployment requirements, and quality gates
- Governance section outlining constitutional authority and amendment procedures

The constitution now properly reflects the requirements for Hackathon Phase II with focus on the specified technology stack and multi-user functionality.

## Outcome

Successfully created and updated the project constitution with all specified principles and standards. The file is now properly configured for the Todo Full-Stack Web Application project with clear guidelines for development.