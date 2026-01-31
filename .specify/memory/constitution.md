<!--
Sync Impact Report:
- Version change: 1.0.0 → 2.0.0
- Modified principles: All principles updated to reflect AI-powered conversational system
- Added sections: None
- Removed sections: None
- Templates requiring updates: .specify/templates/plan-template.md, .specify/templates/spec-template.md, .specify/templates/tasks-template.md (all need to reflect AI agent architecture)
- Follow-up TODOs: None
-->
# FlowForge AI-Powered Conversational Todo Application Constitution

## Core Principles

### I. AI-First Interaction
All user actions must be driven through natural language conversation. The system behaves as an intelligent assistant, not a command-based UI. All functionality must be accessible through conversational interface.

### II. Agent-Based Architecture
System intelligence is decomposed into reusable AI agents. Each agent has a single, clearly defined responsibility. Agents must be designed for reusability and clear separation of concerns.

### III. Security by Design
All AI actions must be bound to authenticated user context. No cross-user data access is allowed under any condition. All AI-driven operations must enforce user isolation and data privacy.

### IV. Deterministic Execution
AI reasoning may be flexible, but all side effects must occur only through validated MCP tools. No direct database access from the AI layer. All operations must be traceable and auditable.

### V. Spec-Driven Development
All behavior is defined through specifications and agent skills. No manual business logic outside specs and skills. Implementation follows spec and plan documents precisely.

### VI. Intent-Driven Processing
User input must be parsed into intent and structured entities before execution. Natural language understanding is a core requirement for all user interactions.

## Additional Constraints

Technology Stack: Next.js 16+, FastAPI, SQLModel, Neon PostgreSQL, Better Auth, Tailwind CSS, Framer Motion, Qwen CLI for LLM interactions
Scope: AI interaction supports only the 5 Basic Todo features: Add task, View tasks, Update task, Delete task, Mark task complete
Performance: API response time <200ms for 95% of requests; support 100+ concurrent users
Security: All user data must be protected with JWT authentication; input validation required; all AI actions bound to user context
Quality: All code must pass linting and formatting checks before merge; all AI agents must have clear skill definitions

## Development Workflow

- All changes must be specified before implementation
- Code reviews must verify compliance with spec and plan
- Automated tests must pass before merge
- Performance targets must be met for all features
- All AI agent behaviors must be defined in skill documents
- All AI-driven operations must go through MCP tools for validation

## Governance

This constitution supersedes all other practices. All development must comply with these principles.

Version: 2.0.0 | Ratified: 2026-01-11 | Last Amended: 2026-01-24
