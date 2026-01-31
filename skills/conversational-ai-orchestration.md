# Conversational AI Orchestration Skills

This directory contains the skill definitions for the main conversational AI orchestrator agent.

## Skills

### 1. Interpret Natural Language Input
- Parse user messages in English
- Extract intent and entities from natural language
- Handle various phrasings for the same action

### 2. Maintain Conversation Context
- Track conversation history
- Remember previous interactions
- Manage context across multiple turns

### 3. Agent/Tool Selection
- Determine which agent or tool to invoke based on user intent
- Route requests to appropriate specialized agents
- Handle fallback mechanisms when primary agent fails

### 4. Coordinate Multi-step Execution
- Chain multiple agent invocations when needed
- Manage dependencies between different operations
- Handle sequential and parallel task execution

### 5. Manage Conversation State
- Track the current state of the conversation
- Handle interruptions and context switching
- Resume conversations appropriately

### 6. Generate Coherent Responses
- Synthesize information from multiple sources
- Format responses in a natural, helpful way
- Handle errors gracefully in conversation flow