"""
Conversation Orchestrator - Manages LLM-to-LLM conversation flow
"""
import uuid
from typing import Dict, List, Tuple, Optional
from app.services.agent_service import AgentService
from .user_simulator import UserSimulator
from .project_prompts import get_available_project_types

class ConversationOrchestrator:
    """Orchestrates the conversation between agent and simulated user"""
    
    def __init__(self):
        self.agent_service = AgentService()
        self.user_simulator = UserSimulator()
    
    async def run_simulation(self, user_id: int, project_type: str = "codementor") -> Dict:
        """Run the complete LLM-to-LLM conversation simulation"""
        
        session_id = str(uuid.uuid4())
        conversation_state = None
        context = {
            'response_count': 0,
            'conversation_history': [],
            'project_type': project_type
        }
        max_discovery_rounds = 15
        
        # Get project definition for initial message
        from .project_prompts import PROJECT_DEFINITIONS
        project = PROJECT_DEFINITIONS.get(project_type, PROJECT_DEFINITIONS["codementor"])
        initial_message = f"I want to build {project['name']}, {project['description']}"
        
        # Create initial conversation state
        from app.models.api_schemas import ConversationState
        initial_conversation_state = ConversationState(
            session_id=session_id,
            user_id=user_id,
            phase="discovery",
            specifications_complete=False,
            project_specification=None,
            current_roadmap=None,
            messages=[]
        )
        
        # Send initial message to agent
        agent_response, updated_state, action_button = await self.agent_service.process_message(
            user_message=initial_message,
            conversation_state=initial_conversation_state,
            action_type="chat"
        )
        
        conversation_state = updated_state
        
        # Add initial conversation to history
        context['conversation_history'].append({
            'agent': agent_response,
            'user': initial_message
        })
        
        conversation_messages = [
            {
                "role": "user",
                "content": initial_message,
                "timestamp": "2023-01-01T00:00:00"
            },
            {
                "role": "assistant", 
                "content": agent_response,
                "timestamp": "2023-01-01T00:01:00"
            }
        ]
        
        # Discovery conversation loop
        for round_num in range(max_discovery_rounds):
            context['response_count'] = round_num + 1
            
            # Check if ready for roadmap generation
            current_phase = conversation_state.phase
            if action_button == 'generate_roadmap' or current_phase == 'confirmation':
                break
                
            if 'roadmap' in agent_response.lower() and 'generate' in agent_response.lower():
                break
            
            # Simulate user response
            user_response = self.user_simulator.simulate_user_response(agent_response, context)
            
            # Update conversation history
            context['conversation_history'].append({
                'agent': agent_response,
                'user': user_response
            })
            
            # Send user response to agent
            agent_response, updated_state, action_button = await self.agent_service.process_message(
                user_message=user_response,
                conversation_state=conversation_state,
                action_type="chat"
            )
            
            conversation_state = updated_state
            conversation_messages.extend([
                {
                    "role": "user",
                    "content": user_response,
                    "timestamp": "2023-01-01T00:02:00"
                },
                {
                    "role": "assistant",
                    "content": agent_response,
                    "timestamp": "2023-01-01T00:03:00"
                }
            ])
        
        # Trigger roadmap generation
        if current_phase == 'confirmation':
            generation_message = "Perfect! Please generate the detailed roadmap for CodeMentor now."
        else:
            generation_message = "That covers everything. Please generate an efficient roadmap for CodeMentor."
        
        # Send final generation message
        final_agent_response, final_state, final_action = await self.agent_service.process_message(
            user_message=generation_message,
            conversation_state=conversation_state,
            action_type="chat"
        )
        
        conversation_messages.extend([
            {
                "role": "user",
                "content": generation_message,
                "timestamp": "2023-01-01T00:04:00"
            },
            {
                "role": "assistant",
                "content": final_agent_response,
                "timestamp": "2023-01-01T00:05:00"
            }
        ])
        
        return {
            "session_id": session_id,
            "conversation_state": final_state,
            "messages": conversation_messages,
            "roadmap": final_state.current_roadmap if final_state else None,
            "total_rounds": context['response_count']
        } 