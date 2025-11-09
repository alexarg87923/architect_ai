#!/usr/bin/env python3
"""
Debug roadmap generation to identify the JSON parsing issue
"""
import asyncio
import json
from app.services.agent_service import AgentService
from app.models.agent import ConversationState, ChatMessage

async def debug_roadmap_generation():
    """Test roadmap generation with debugging"""
    
    # Initialize agent service
    agent_service = AgentService()
    
    # Create a more comprehensive conversation state
    conversation_state = ConversationState(
        session_id="debug-session",
        user_id=1,
        phase="confirmation", 
        specifications_complete=True,
        project_specification=None,
        current_roadmap=None,
        messages=[
            ChatMessage(
                role="user",
                content="I want to build TaskFlow Pro, a comprehensive task management web application for small development teams",
                timestamp="2023-01-01T00:00:00",
                action_type="chat"
            ),
            ChatMessage(
                role="assistant",
                content="What specific problem does TaskFlow Pro aim to solve for small development teams?",
                timestamp="2023-01-01T00:01:00",
                action_type="chat"
            ),
            ChatMessage(
                role="user",
                content="TaskFlow Pro should help teams organize projects, assign tasks, track progress with Kanban boards, and enable team collaboration through comments and file sharing.",
                timestamp="2023-01-01T00:02:00", 
                action_type="chat"
            ),
            ChatMessage(
                role="assistant",
                content="Ok I think I fully understand your project's specifications. Building TaskFlow Pro, a comprehensive task management web application for small development teams.",
                timestamp="2023-01-01T00:03:00",
                action_type="specifications_complete"
            )
        ]
    )
    
    print("🔍 Testing roadmap generation with debugging...")
    print(f"Phase: {conversation_state.phase}")
    print(f"Specifications complete: {conversation_state.specifications_complete}")
    
    try:
        # Call the agent
        response, updated_state, action = await agent_service.process_message(
            "Please generate the detailed roadmap for TaskFlow Pro now.",
            conversation_state,
            action_type="chat"
        )
        
        print(f"\n✅ Response: {response}")
        print(f"Updated phase: {updated_state.phase}")
        print(f"Action button: {action}")
        
        if updated_state.current_roadmap:
            roadmap = updated_state.current_roadmap
            print(f"\n📋 Roadmap generated:")
            print(f"  Project: {roadmap.project_specification.title}")
            print(f"  Nodes: {len(roadmap.nodes)}")
            for i, node in enumerate(roadmap.nodes, 1):
                print(f"    {i}. {node.title} (Subtasks: {len(node.subtasks)})")
                for j, subtask in enumerate(node.subtasks, 1):
                    print(f"       {j}. {subtask.title}")
        else:
            print("\n❌ No roadmap found in response")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_roadmap_generation())
