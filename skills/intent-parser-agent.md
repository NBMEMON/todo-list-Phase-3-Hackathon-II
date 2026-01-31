# Intent Parser Agent Skills

This directory contains the skill definitions for the intent parser agent.

## Skills

### 1. Natural Language Understanding
- Parse user input in English
- Identify the main intent behind the user's request
- Recognize various ways to express the same intent

### 2. Entity Extraction
- Extract relevant entities from user input (task titles, dates, priorities, etc.)
- Identify task attributes like title, description, priority
- Recognize task IDs or references to existing tasks

### 3. Intent Classification
- Classify intents into categories:
  - CREATE_TASK: Adding a new task
  - UPDATE_TASK: Modifying an existing task
  - DELETE_TASK: Removing a task
  - COMPLETE_TASK: Marking a task as complete/incomplete
  - LIST_TASKS: Requesting to see tasks
  - SEARCH_TASKS: Looking for specific tasks

### 4. Context Awareness
- Understand references to previously mentioned tasks
- Handle pronouns and contextual references
- Maintain understanding across conversation turns

### 5. Error Handling
- Gracefully handle unrecognized inputs
- Request clarification when intent is ambiguous
- Provide helpful feedback to guide user input