# Data Model: AI-Powered Conversational Todo System

## 1. Task Entity (Extended from existing model)

### 1.1 Fields
- **id**: String (Primary Key)
  - Unique identifier for the task
  - Auto-generated UUID
  - Required

- **title**: String
  - Task title or description
  - Max length: 200 characters
  - Required

- **description**: String (Optional)
  - Detailed task description
  - Max length: 1000 characters
  - Optional

- **completed**: Boolean
  - Indicates if the task is completed
  - Default: false
  - Required

- **priority**: Integer
  - Task priority level (1-5, 1 being highest)
  - Default: 3
  - Optional

- **due_date**: DateTime (Optional)
  - Deadline for the task
  - Format: ISO 8601
  - Optional

- **recurrence_pattern**: String (Optional)
  - Recurrence pattern for recurring tasks
  - Values: "daily", "weekly", "monthly", "custom", null
  - Optional

- **tags**: Array<String> (Optional)
  - Tags associated with the task
  - Max: 10 tags per task
  - Optional

- **user_id**: String (Foreign Key)
  - Links the task to a user
  - References User.id
  - Required

- **created_at**: DateTime
  - Timestamp of task creation
  - Auto-generated
  - Required

- **updated_at**: DateTime
  - Timestamp of last update
  - Auto-generated and updated
  - Required

### 1.2 Validation Rules
- Title must be between 1 and 200 characters
- Priority must be between 1 and 5 (inclusive)
- Due date must be a valid future date
- Recurrence pattern must be one of the allowed values
- User_id must reference an existing user

### 1.3 Relationships
- Belongs to: User (Many-to-One)
- User has many Tasks

## 2. Conversation Thread Entity (New)

### 2.1 Fields
- **id**: String (Primary Key)
  - Unique identifier for the conversation thread
  - Auto-generated UUID
  - Required

- **user_id**: String (Foreign Key)
  - Links the conversation to a user
  - References User.id
  - Required

- **session_id**: String
  - Unique identifier for the conversation session
  - Used to group related messages
  - Required

- **messages**: JSON
  - Array of message objects containing:
    - role: "user" or "assistant"
    - content: string content of the message
    - timestamp: ISO 8601 formatted datetime
    - language: "en" or "ur" (detected language)
  - Required

- **context**: JSON
  - Current conversation context/state
  - Contains information like:
    - Active task ID (if any)
    - Current intent being processed
    - User preferences
  - Optional

- **language_preference**: String
  - Preferred language for the conversation
  - Values: "en", "ur", "auto" (detect from input)
  - Default: "auto"

- **created_at**: DateTime
  - Timestamp of conversation creation
  - Auto-generated
  - Required

- **updated_at**: DateTime
  - Timestamp of last update
  - Auto-generated and updated
  - Required

### 2.2 Validation Rules
- User_id must reference an existing user
- Messages array must not exceed 1000 messages
- Each message content must be between 1 and 10000 characters
- Session_id must be unique per user

### 2.3 Relationships
- Belongs to: User (Many-to-One)
- User has many Conversation Threads

## 3. User Entity (Existing, referenced)

### 3.1 Relevant Fields
- **id**: String (Primary Key)
- **email**: String (Unique)
- **name**: String (Optional)

## 4. State Transitions

### 4.1 Task State Transitions
- `pending` → `completed`: When task is marked as complete
- `completed` → `pending`: When task is marked as incomplete

### 4.2 Conversation Context Transitions
- `idle` → `awaiting_details`: When user provides partial information requiring clarification
- `awaiting_details` → `idle`: When user provides requested details
- `idle` → `processing`: When AI is processing user request
- `processing` → `idle`: When AI completes processing and responds

## 5. Indexes

### 5.1 Task Entity
- Index on (user_id, created_at) for efficient retrieval of user's tasks ordered by creation date
- Index on (user_id, completed) for efficient filtering by completion status
- Index on (user_id, priority) for efficient filtering by priority

### 5.2 Conversation Thread Entity
- Index on (user_id, session_id) for efficient retrieval of specific conversation sessions
- Index on (user_id, updated_at) for efficient retrieval of recent conversations