import asyncio
from backend.agents.main_orchestrator import process_conversation_turn

async def test_complete_user_flow():
    """
    Test the complete user flow: add/view/complete tasks via AI assistant
    """
    print("Testing complete user flow: add/view/complete tasks via AI assistant")
    
    # Simulate a user ID
    user_id = "test_user_123"
    
    # Test 1: Add a task
    print("\n1. Testing add task:")
    add_result = await process_conversation_turn(
        user_input="Add a task to buy groceries",
        user_id=user_id
    )
    print(f"Response: {add_result['response']}")
    print(f"Action taken: {add_result['action_taken']}")
    
    # Test 2: View tasks
    print("\n2. Testing view tasks:")
    view_result = await process_conversation_turn(
        user_input="Show me my tasks",
        user_id=user_id
    )
    print(f"Response: {view_result['response']}")
    print(f"Action taken: {view_result['action_taken']}")
    
    # Test 3: Complete a task
    print("\n3. Testing complete task:")
    complete_result = await process_conversation_turn(
        user_input="Mark the groceries task as complete",
        user_id=user_id
    )
    print(f"Response: {complete_result['response']}")
    print(f"Action taken: {complete_result['action_taken']}")
    
    # Test 4: Try an invalid command
    print("\n4. Testing invalid command:")
    invalid_result = await process_conversation_turn(
        user_input="Fly to the moon",
        user_id=user_id
    )
    print(f"Response: {invalid_result['response']}")
    print(f"Action taken: {invalid_result['action_taken']}")
    
    print("\nComplete user flow test finished.")

if __name__ == "__main__":
    asyncio.run(test_complete_user_flow())