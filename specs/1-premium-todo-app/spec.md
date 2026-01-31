# FlowForge – Todo Full-Stack Web Application Specification v2.0 (Phase II – Premium Edition)

## 1. Project Overview & Vision

FlowForge is a premium productivity application designed to elevate the traditional todo list into a sophisticated, visually stunning task management experience. The name represents the fusion of "flow" (representing seamless, productive work experiences) and "forge" (representing the creation and shaping of tasks into accomplishments). This application aims to provide the same level of polish and user experience found in premium productivity tools like Notion, Todoist, Linear, and Superhuman.

The application will be a multi-user, authenticated todo list with advanced UI/UX features, responsive design, and enterprise-grade security. Built with modern web technologies, FlowForge will offer a delightful user experience with smooth animations, premium visual design, and intuitive interactions.

## 2. Color Theme, Typography & Design System

### Color Palette
- **Primary Dark**: Deep Navy (#0f172a) - Used as the main background for dark mode
- **Accent Cyan**: Electric Cyan (#06b6d4) - Used for primary actions, highlights, and success states
- **Accent Purple**: Royal Purple (#7c3aed) - Used for secondary actions and important indicators
- **Text Colors**: Soft white (#f1f5f9) and various gray contrasts for readability
- **Light Mode**: Light grays and whites with the same accent colors for consistency

### Typography
- **Primary Font**: Inter or Manrope - Modern, clean sans-serif for all UI elements
- **Code Font**: JetBrains Mono - For code-like elements and technical displays
- **Font Hierarchy**: Clear sizing and weight distinctions for headings, body text, and captions

### Spacing & Shadows
- **Spacing Scale**: 4px, 8px, 12px, 16px, 24px, 32px, 48px, 64px
- **Shadow System**: Subtle depth for cards and elevated elements using rgba values
- **Border Radius**: Large rounded corners (lg) for premium feel

### Animation System
- **Framer Motion**: Smooth transitions for all interactive elements
- **Micro-interactions**: Hover effects, scale transforms, and subtle movements
- **Loading States**: Skeleton screens with shimmer effects
- **Success Feedback**: Confetti animations on task completion

## 3. Data Model

### Task Entity
The core data model consists of a Task entity with the following attributes:
- **id**: Unique identifier for each task (UUID or auto-incrementing integer)
- **user_id**: Foreign key linking to the authenticated user who owns the task
- **title**: String representing the task title (required, max 255 characters)
- **description**: Text field for detailed task description (optional, unlimited length)
- **completed**: Boolean flag indicating task completion status (default: false)
- **created_at**: Timestamp of when the task was created
- **updated_at**: Timestamp of when the task was last modified

### User Entity (via Better Auth)
- **id**: Unique identifier for each user
- **email**: User's email address (unique, required)
- **name**: User's display name (optional)
- **created_at**: Timestamp of account creation
- **updated_at**: Timestamp of last account update

## 4. Authentication Flow

### User Registration/Login
1. Users access the application and see a clean, branded login screen
2. Users can register with email/password or sign in with existing credentials
3. Better Auth handles credential validation and JWT token issuance
4. JWT tokens are stored securely in browser storage with proper security flags

### Session Management
1. JWT tokens are sent with every authenticated request in the Authorization header
2. FastAPI middleware validates tokens on protected endpoints
3. Access tokens follow the policy defined in the implementation plan (15 minutes) with refresh tokens (7 days)
4. Automatic logout occurs on token expiration or invalidation

### Protected Routes
1. All task-related endpoints require valid JWT authentication
2. Middleware enforces 401 Unauthorized responses for invalid tokens
3. User ownership is validated for all task operations

## 5. API Endpoints

| Method | Path | Description | Auth Required | Example |
|--------|------|-------------|---------------|---------|
| POST | `/api/{user_id}/tasks` | Create a new task | Yes | `{title: "New Task", description: "Task details"}` |
| GET | `/api/{user_id}/tasks` | Retrieve user's tasks | Yes | `[{id: 1, title: "Task 1", completed: false}]` |
| GET | `/api/{user_id}/tasks/{task_id}` | Retrieve specific task | Yes | `{id: 1, title: "Task 1", completed: false}` |
| PUT | `/api/{user_id}/tasks/{task_id}` | Update task details | Yes | `{title: "Updated Task", description: "Updated details"}` |
| DELETE | `/api/{user_id}/tasks/{task_id}` | Delete a task | Yes | `204 No Content` |
| PATCH | `/api/{user_id}/tasks/{task_id}/complete` | Toggle task completion | Yes | `{completed: true}` |

## 6. Frontend Architecture & Pages/Components

### Next.js App Router Structure
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
```

### Core Components
- **Header Component**: Navigation bar with logo, user profile, and dark/light mode toggle
- **Sidebar Component**: Collapsible navigation with task filters and user options
- **Task List Component**: Grid/list view of premium glassmorphic task cards
- **Task Card Component**: Individual task display with status indicator, title, description, and action buttons
- **Add Task Form**: Floating action button that opens modal/form for new tasks
- **Auth Form**: Login/registration interface with validation

### Theme Provider
- Context provider managing dark/light mode state
- Smooth transitions between themes
- Persists user preference in localStorage

## 7. UI/UX Flow & Animations

### Dashboard Experience
1. **Page Load**: Smooth fade-in animation as content loads
2. **Task Cards**: Slide-in animation from bottom as they appear
3. **Hover Effects**: Subtle lift and shadow enhancement on task card hover
4. **Task Completion**: Electric cyan checkmark animation with success confetti
5. **Loading States**: Skeleton screens with shimmer effect during data fetch
6. **Notifications**: Toast notifications for all user actions (success, error, warning) appearing at top-right of screen

### Task Management Flows
1. **Add Task**: Floating action button expands to reveal form with smooth transition
2. **Edit Task**: Clicking task opens inline editor with morphing animation
3. **Delete Task**: Confirmation dialog with slide-in animation before deletion
4. **Filter Tasks**: Animated transitions when applying filters or changing views
5. **Load More Tasks**: Infinite scroll with smooth loading animation when approaching bottom of task list

### Responsive Behavior
1. **Mobile**: Stacked layout with hamburger menu for navigation
2. **Tablet**: Optimized two-column layout with collapsible sidebar
3. **Desktop**: Full-featured three-column layout with persistent sidebar

## 8. Monorepo Structure

```
flowforge-todo/
├── README.md
├── package.json
├── tsconfig.json
├── .env.example
├── .gitignore
├── specs/
│   └── 1-premium-todo-app/
│       └── spec.md
├── .specify/
│   ├── memory/
│   ├── scripts/
│   └── templates/
├── backend/
│   ├── main.py (FastAPI app entry)
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py (SQLModel definitions)
│   ├── api/
│   │   ├── __init__.py
│   │   └── tasks.py (Task endpoints)
│   ├── auth/
│   │   ├── __init__.py
│   │   └── middleware.py (JWT validation)
│   └── database/
│       ├── __init__.py
│       └── session.py (Database session management)
├── frontend/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── dashboard/
│   │   │   ├── page.tsx
│   │   │   └── layout.tsx
│   │   ├── login/
│   │   │   └── page.tsx
│   │   └── providers/
│   │       └── theme-provider.tsx
│   ├── components/
│   │   ├── header.tsx
│   │   ├── sidebar.tsx
│   │   ├── task-card.tsx
│   │   ├── task-list.tsx
│   │   └── floating-action-button.tsx
│   ├── lib/
│   │   ├── auth.ts (Authentication utilities)
│   │   └── api.ts (API client)
│   ├── styles/
│   │   └── globals.css
│   ├── public/
│   │   ├── favicon.ico
│   │   └── icons/
│   └── package.json
├── docker-compose.yml
└── docs/
    └── architecture.md
```

## 9. Edge Cases & Security

### Data Retention Policy
- User tasks are retained indefinitely unless explicitly deleted by the user
- Deleted tasks are permanently removed from the system after 30-day grace period
- User account deletion triggers removal of all associated tasks

### Authentication Edge Cases
- Token expiration during active session
- Concurrent sessions across multiple devices
- Password reset and account recovery
- Invalid token handling with graceful redirects

### Authorization Edge Cases
- Attempting to access another user's tasks
- Modifying/deleting tasks that don't belong to the user
- Creating tasks for a different user ID than authenticated
- Bulk operations limited to authenticated user's tasks only

### Security Measures
- JWT token validation on all protected endpoints
- Input sanitization to prevent injection attacks
- Rate limiting to prevent abuse
- HTTPS enforcement for all production traffic
- Proper CORS configuration limiting origins
- Secure storage of sensitive data

### Error Handling
- 401 Unauthorized for invalid/missing tokens
- 403 Forbidden for unauthorized access attempts
- 404 Not Found for non-existent resources
- 500 Internal Server Error with appropriate logging

## 10. Acceptance Criteria

### Premium UI Feel
- [ ] Glassmorphic task cards with subtle transparency and blur effects
- [ ] Smooth Framer Motion animations for all interactive elements
- [ ] Electric cyan accent on complete button and success states
- [ ] Dark/light mode toggle with seamless transition
- [ ] Loading skeletons with shimmer effect during data operations
- [ ] Success confetti animation when tasks are marked complete

### Multi-User Functionality
- [ ] Users can register and authenticate securely
- [ ] Each user sees only their own tasks
- [ ] Users cannot access or modify other users' tasks
- [ ] Proper session management with JWT tokens

### Persistence & Data Integrity
- [ ] Tasks are saved to Neon PostgreSQL database
- [ ] Data persists across browser sessions
- [ ] All CRUD operations work reliably
- [ ] Task completion status is preserved

### Responsiveness
- [ ] Application works seamlessly on mobile devices
- [ ] Layout adapts appropriately to different screen sizes
- [ ] Touch interactions work smoothly on mobile
- [ ] Performance remains consistent across devices

### Animations & Interactions
- [ ] All animations perform smoothly without jank
- [ ] Hover effects respond immediately and consistently
- [ ] Loading states provide clear feedback
- [ ] Success feedback is visually satisfying

## Clarifications

### Session 2026-01-11

- Q: Should we define specific performance targets for response times and concurrent users? → A: Yes, define specific performance targets
- Q: What should be the JWT token expiration policy? → A: Access tokens expire in 15 minutes with refresh tokens valid for 7 days (see implementation plan for details)
- Q: How should the application handle large task lists? → A: Use infinite scroll instead of traditional pagination
- Q: What notification system should be used for user feedback? → A: Implement toast notifications for all user actions
- Q: What should be the data retention policy for user tasks? → A: Retain user tasks indefinitely unless explicitly deleted by the user

## 12. Non-Functional Quality Attributes (Updated)

### Performance Targets
- API response time: <200ms for 95% of requests
- Support up to 100 concurrent users in free tier, 1000+ for paid tiers
- Page load time: <3 seconds for initial load, <1 second for subsequent navigation
- Handle minimum 10,000 tasks per user without performance degradation

### Other Quality Attributes
- Scalability: Horizontal scaling capability for user growth
- Reliability: 99.9% uptime target with automatic failover
- Availability: Graceful degradation during service disruptions
- Observability: Structured logging, performance metrics, and alerting
- Security: OWASP Top 10 compliance, encrypted data at rest and in transit

## 12. Bonus Touchpoints

### Reusable Subagents
- [ ] Component architecture designed for future extensibility
- [ ] API endpoints structured to support additional features
- [ ] Authentication system ready for role-based permissions
- [ ] Data models prepared for advanced task properties (priority, tags, due dates)

### Dark Mode Excellence
- [ ] Carefully crafted color palette for optimal contrast in dark mode
- [ ] Adaptive text colors that maintain readability
- [ ] Subtle gradients and shadows that enhance depth without eye strain

### Future-Ready Design
- [ ] Task cards designed with space for priority badges and tags
- [ ] API endpoints structured to accommodate additional task properties
- [ ] Component architecture allowing for drag-and-drop reordering
- [ ] Notification system foundation for reminders and updates