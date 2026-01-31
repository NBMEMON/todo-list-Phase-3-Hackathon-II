# Data Model for FlowForge Todo Application

## Task Entity

### Fields
- **id**: UUID (primary key)
  - Type: UUID
  - Constraints: Primary key, not nullable, auto-generated
  - Description: Unique identifier for each task

- **user_id**: UUID (foreign key)
  - Type: UUID
  - Constraints: Foreign key to User.id, not nullable
  - Description: Links the task to the authenticated user who owns it

- **title**: String
  - Type: String (max 255 characters)
  - Constraints: Not nullable
  - Description: Brief title of the task

- **description**: Text
  - Type: Text (unlimited length)
  - Constraints: Nullable
  - Description: Detailed description of the task

- **completed**: Boolean
  - Type: Boolean
  - Constraints: Not nullable, default: false
  - Description: Flag indicating whether the task is completed

- **created_at**: DateTime
  - Type: DateTime
  - Constraints: Not nullable, auto-generated
  - Description: Timestamp of when the task was created

- **updated_at**: DateTime
  - Type: DateTime
  - Constraints: Not nullable, auto-generated, updates on change
  - Description: Timestamp of when the task was last modified

### Relationships
- Task belongs to one User (many-to-one relationship)
- User has many Tasks (one-to-many relationship)

### Validation Rules
- Title must be between 1 and 255 characters
- User_id must correspond to an existing user
- Completed status can only be true or false

### State Transitions
- New task: completed = false
- Task completed: completed = true
- Task uncompleted: completed = false

## User Entity (via Better Auth)

### Fields
- **id**: UUID (primary key)
  - Type: UUID
  - Constraints: Primary key, not nullable, auto-generated
  - Description: Unique identifier for each user

- **email**: String
  - Type: String
  - Constraints: Unique, not nullable
  - Description: User's email address for authentication

- **name**: String
  - Type: String
  - Constraints: Nullable
  - Description: User's display name

- **created_at**: DateTime
  - Type: DateTime
  - Constraints: Not nullable, auto-generated
  - Description: Timestamp of account creation

- **updated_at**: DateTime
  - Type: DateTime
  - Constraints: Not nullable, auto-generated
  - Description: Timestamp of last account update

### Relationships
- User has many Tasks (one-to-many relationship)
- Task belongs to one User (many-to-one relationship)

### Validation Rules
- Email must be unique across all users
- Email must be a valid email format
- Name, if provided, must be between 1 and 255 characters