#!/usr/bin/env python3
"""
Debug the final roadmap generation step specifically
"""
import asyncio
import json
from app.services.agent_service import AgentService
from app.models.agent import ConversationState, ChatMessage

async def debug_final_generation():
    """Debug the final generation step that's failing"""
    
    agent_service = AgentService()
    
    # Create conversation state that matches the failed test
    conversation_state = ConversationState(
        session_id="final-debug-session",
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
                content="What specific problems do you see small development teams facing that TaskFlow Pro aims to solve?",
                timestamp="2023-01-01T00:01:00",
                action_type="chat"
            ),
            ChatMessage(
                role="user",
                content="Small development teams often struggle with task management due to the lack of a centralized platform for organizing projects, assigning tasks, tracking progress, and enabling team collaboration.",
                timestamp="2023-01-01T00:02:00", 
                action_type="chat"
            ),
            ChatMessage(
                role="assistant",
                content="Ok I think I fully understand your project's specifications\n\nBuilding TaskFlow Pro, a comprehensive task management web application for small development teams with React frontend, PostgreSQL database, user authentication, and core features including project creation, task assignment, Kanban boards, time tracking, team collaboration tools, and responsive design.",
                timestamp="2023-01-01T00:08:00",
                action_type="specifications_complete"
            )
        ]
    )
    
    print("🔍 Testing final roadmap generation step...")
    print(f"Phase: {conversation_state.phase}")
    print(f"Specifications complete: {conversation_state.specifications_complete}")
    print(f"Message count: {len(conversation_state.messages)}")
    
    try:
        # Test the exact message that's failing
        response, updated_state, action = await agent_service.process_message(
            "Perfect! Please generate the detailed roadmap for TaskFlow Pro now.",
            conversation_state,
            action_type="chat"
        )
        
        print(f"\n✅ Response: {response}")
        print(f"Updated phase: {updated_state.phase}")
        print(f"Action button: {action}")
        
        if updated_state.current_roadmap:
            roadmap = updated_state.current_roadmap
            print(f"\n📋 Roadmap generated successfully!")
            print(f"  Project: {roadmap.project_specification.title}")
            print(f"  Nodes: {len(roadmap.nodes)}")
            for i, node in enumerate(roadmap.nodes, 1):
                print(f"    {i}. {node.title} (Subtasks: {len(node.subtasks)})")
                for j, subtask in enumerate(node.subtasks, 1):
                    print(f"       {j}. {subtask.title}")
        else:
            print("\n❌ No roadmap found in response")
            print("Debug: Let me check the conversation state...")
            print(f"Current roadmap: {updated_state.current_roadmap}")
            print(f"Last message: {updated_state.messages[-1].content if updated_state.messages else 'No messages'}")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_final_generation())
