"""
Agent orchestrator - main entry point for the agent service.
Routes requests to appropriate handlers based on phase and action type.
"""

import re
import json
from typing import Dict, Any, Tuple, Optional
from openai import AsyncOpenAI
from datetime import datetime

from app.core.config import settings
from app.models.api_schemas import ChatMessage, ConversationState
from .tools import get_agent_tools
from .roadmap_generation import RoadmapGenerationHandler


class AgentOrchestrator:
    """Main orchestrator for agent conversations - routes to appropriate handlers"""
    
    def __init__(self):
        # Initialize client with GROQ/OpenAI fallback logic
        groq_key = settings.GROQ_API_KEY
        openai_key = settings.OPENAI_API_KEY
        
        if groq_key and groq_key != "":
            self.client = AsyncOpenAI(api_key=groq_key, base_url="https://api.groq.com/openai/v1")
            self.client_mode = "groq"
            self.model = settings.GROQ_MODEL
            self.max_tokens = 8000  # GROQ token limit
            self.temperature = 0.1  # Lower temperature for more consistent responses
            print("⚡️ Using GROQ API key")
        elif openai_key and openai_key != "":
            self.client = AsyncOpenAI(api_key=openai_key)
            self.client_mode = "openai"
            self.model = settings.OPENAI_MODEL
            self.max_tokens = settings.OPENAI_MAX_TOKENS
            self.temperature = settings.OPENAI_TEMPERATURE
            print("⚡️ Using OPENAI API key")
        else:
            raise ValueError("No valid API key found. Please provide either GROQ_API_KEY or OPENAI_API_KEY in environment variables or config.")
            
        self.tools = get_agent_tools()
        
        # Initialize handlers
        self.roadmap_handler = RoadmapGenerationHandler(
            self.client, self.client_mode, self.model, 
            self.max_tokens, self.temperature, self.tools
        )
    
    async def process_message(
        self, 
        user_message: str, 
        conversation_state: ConversationState,
        action_type: str = "chat"
    ) -> Tuple[str, ConversationState, Optional[str]]:
        """
        Main entry point - process user message and route to appropriate handler
        Args:
            user_message: The user's input
            conversation_state: Current conversation state
            action_type: Explicit action type from frontend ("chat", "edit", "expand")
        Returns: (agent_response, updated_state, action_button)
        """
        
        # Add user message to conversation
        conversation_state.messages.append(
            ChatMessage(
                role="user", 
                content=user_message,
                timestamp=datetime.now().isoformat()
            )
        )
        
        # Determine the actual phase based on conversation state
        actual_phase = self._determine_phase(conversation_state, action_type)
        
        # Route to appropriate handler based on phase and action type
        if actual_phase in ["discovery", "confirmation", "generation", "subtask_generation"]:
            return await self._handle_roadmap_generation(user_message, conversation_state, actual_phase, action_type)
        
        elif actual_phase == "editing":
            if action_type == "expand":
                return await self._handle_roadmap_expansion(user_message, conversation_state, action_type)
            elif action_type == "edit":
                return await self._handle_roadmap_editing(user_message, conversation_state, action_type)
            else:
                return await self._handle_general_chat(user_message, conversation_state, action_type)
        
        # Default fallback
        return "I'm here to help you plan your project roadmap.", conversation_state, None
    
    async def _handle_roadmap_generation(
        self, 
        user_message: str, 
        conversation_state: ConversationState, 
        phase: str, 
        action_type: str
    ) -> Tuple[str, ConversationState, Optional[str]]:
        """Handle roadmap generation workflow"""
        
        if action_type in ["edit", "expand"] and not conversation_state.current_roadmap:
            return """You cannot edit or expand a roadmap that doesn't exist yet. 

You need to create a roadmap first by gathering project specifications. Ask clarifying questions to understand the project requirements, then generate the initial roadmap.

Use the ask_clarifying_question function to gather project information.""", conversation_state, None
        
        # Get system prompt from roadmap handler
        system_prompt = self.roadmap_handler.get_system_prompt(phase, conversation_state)
        
        # Get available tools for this phase
        available_tools = self.roadmap_handler.get_available_tools(phase)
        
        # Prepare messages for LLM
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add conversation history (last 10 messages to keep context manageable)
        recent_messages = conversation_state.messages[-10:]
        for msg in recent_messages:
            messages.append({"role": msg.role, "content": msg.content})
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=available_tools,
                tool_choice="auto",
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            # Process the response
            message = response.choices[0].message
            
            if message.tool_calls:
                # Handle function calls
                return await self._handle_function_calls(message.tool_calls, conversation_state, action_type)
            else:
                # Check if GROQ returned function calls as text (fallback parsing)
                agent_response = message.content.strip()
                
                if self.client_mode == "groq" and agent_response.startswith("<function="):
                    # Parse GROQ text-based function calls
                    return await self.parse_groq_function_call(agent_response, conversation_state, action_type, self.roadmap_handler)
                
                # Regular text response
                conversation_state.messages.append(
                    ChatMessage(
                        role="assistant",
                        content=agent_response,
                        timestamp=datetime.now().isoformat(),
                        action_type="chat"
                    )
                )
                return agent_response, conversation_state, None
                
        except Exception as e:
            error_msg = f"Sorry, I encountered an error with {self.client_mode.upper()}: {str(e)}"
            return error_msg, conversation_state, None
    
    async def _handle_roadmap_expansion(
        self, 
        user_message: str, 
        conversation_state: ConversationState, 
        action_type: str
    ) -> Tuple[str, ConversationState, Optional[str]]:
        """Handle roadmap expansion (placeholder for future implementation)"""
        
        return """The user wants to EXPAND the roadmap by adding new features or scope.

IMPORTANT: You must ask clarifying questions first to understand:
- What new feature/functionality they want to add
- Which existing node it should branch from
- Any specific requirements or constraints

Only use expand_roadmap_node function after you have gathered enough details about the expansion.
Do NOT expand immediately - ask questions first to ensure you understand their requirements.""", conversation_state, None
    
    async def _handle_roadmap_editing(
        self, 
        user_message: str, 
        conversation_state: ConversationState, 
        action_type: str
    ) -> Tuple[str, ConversationState, Optional[str]]:
        """Handle roadmap editing (placeholder for future implementation)"""
        
        return """The user wants to EDIT an existing roadmap node.

IMPORTANT: You must ask clarifying questions first to understand:
- Which specific node they want to edit
- What aspects they want to change (title, description, timeline, deliverables, etc.)
- The specific changes they want to make

Only use edit_roadmap_node function after you have gathered enough details about the edits.
Do NOT edit immediately - ask questions first to ensure you understand their requirements.""", conversation_state, None
    
    async def _handle_general_chat(
        self, 
        user_message: str, 
        conversation_state: ConversationState, 
        action_type: str
    ) -> Tuple[str, ConversationState, Optional[str]]:
        """Handle general chat in editing phase (placeholder for future implementation)"""
        
        return """You are in general chat mode. Help the user with questions about their roadmap, provide guidance, or clarify their needs.

If they mention wanting to expand or edit something, remind them to use the appropriate action mode (Expand or Edit) from the dropdown for those operations.

You can use add_subtasks_to_node if they want to break down existing work into more detailed steps.""", conversation_state, None
    
    async def _handle_function_calls(
        self, 
        tool_calls, 
        conversation_state: ConversationState,
        action_type: str = "chat"
    ) -> Tuple[str, ConversationState, Optional[str]]:
        """Process function calls from the LLM"""
        
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            try:
                function_args = json.loads(tool_call.function.arguments)
            except json.JSONDecodeError as e:
                print(f"JSON decode error for {function_name}: {e}")
                print(f"Raw arguments: {tool_call.function.arguments[:1000]}...")
                return f"Sorry, there was an error parsing the function arguments for {function_name}.", conversation_state, None
            
            # Route function calls to appropriate handlers
            if function_name == "ask_clarifying_question":
                return await self.roadmap_handler.handle_clarifying_question(function_args, conversation_state)
                
            elif function_name == "confirm_specifications_complete":
                return await self.roadmap_handler.handle_specifications_complete(function_args, conversation_state)
                
            elif function_name in ["generate_high_level_roadmap", "generate_project_roadmap"]:
                return await self.roadmap_handler.handle_high_level_roadmap_generation(function_args, conversation_state)
                
            elif function_name == "generate_node_subtasks":
                return await self.roadmap_handler.handle_node_subtasks_generation(function_args, conversation_state)
                
            # Future handlers for editing and expansion
            elif function_name == "expand_roadmap_node":
                # TODO: Route to expansion handler
                return "Roadmap expansion functionality coming soon.", conversation_state, None
                
            elif function_name == "add_subtasks_to_node":
                # TODO: Route to editing handler
                return "Add subtasks functionality coming soon.", conversation_state, None
                
            elif function_name == "edit_roadmap_node":
                # TODO: Route to editing handler
                return "Node editing functionality coming soon.", conversation_state, None
        
        return "I'm not sure how to help with that.", conversation_state, None
    
    @staticmethod
    async def parse_groq_function_call(
        response_text: str, 
        conversation_state: ConversationState, 
        action_type: str,
        handler
    ) -> Tuple[str, ConversationState, Optional[str]]:
        """Parse GROQ's text-based function calls when they don't use proper tool calls"""
        
        try:
            # Extract function call using regex
            # Pattern: <function=function_name {"param": "value", ...}
            pattern = r'<function=(\w+)\s*({.*?})'
            match = re.search(pattern, response_text, re.DOTALL)
            
            if not match:
                # If no function pattern found, treat as regular response
                conversation_state.messages.append(
                    ChatMessage(
                        role="assistant",
                        content=response_text,
                        timestamp=datetime.now().isoformat(),
                        action_type="chat"
                    )
                )
                return response_text, conversation_state, None
            
            function_name = match.group(1)
            function_args_str = match.group(2)
            
            # Parse JSON arguments
            function_args = json.loads(function_args_str)
            
            # Handle the function call through the appropriate handler
            if function_name == "ask_clarifying_question":
                return await handler.handle_clarifying_question(function_args, conversation_state)
            elif function_name == "confirm_specifications_complete":
                return await handler.handle_specifications_complete(function_args, conversation_state)
            elif function_name in ["generate_high_level_roadmap", "generate_project_roadmap"]:
                return await handler.handle_high_level_roadmap_generation(function_args, conversation_state)
            elif function_name == "generate_node_subtasks":
                return await handler.handle_node_subtasks_generation(function_args, conversation_state)
            else:
                # Unknown function, treat as regular response
                conversation_state.messages.append(
                    ChatMessage(
                        role="assistant",
                        content=response_text,
                        timestamp=datetime.now().isoformat(),
                        action_type="chat"
                    )
                )
                return response_text, conversation_state, None
                
        except Exception as e:
            # If parsing fails, treat as regular response
            conversation_state.messages.append(
                ChatMessage(
                    role="assistant",
                    content=response_text,
                    timestamp=datetime.now().isoformat(),
                    action_type="chat"
                )
            )
            return response_text, conversation_state, None
    
    def _determine_phase(self, conversation_state: ConversationState, action_type: str) -> str:
        """Determine the actual phase based on conversation state and action type"""
        
        # If no roadmap exists, we must go through discovery -> generation first
        if not conversation_state.current_roadmap:
            if not conversation_state.specifications_complete:
                return "discovery"
            else:
                return "generation"
        
        # If roadmap exists but nodes need subtasks, we're in subtask generation phase
        if (conversation_state.current_roadmap and 
            conversation_state.phase == "subtask_generation" and
            hasattr(conversation_state, 'nodes_needing_subtasks') and 
            conversation_state.nodes_needing_subtasks):
            return "subtask_generation"
        
        # If roadmap exists and complete, we're in editing phase (unless explicitly generating)
        if conversation_state.current_roadmap and action_type != "generate":
            return "editing"
        
        # Default to the stored phase
        return conversation_state.phase or "discovery"
    
    # Legacy methods for backward compatibility
    async def generate_roadmap(self, conversation_state):
        """Legacy method - roadmap generation now handled via function calling"""
        if conversation_state.current_roadmap:
            return conversation_state.current_roadmap
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="No roadmap generated yet")
    
    async def expand_node(self, node_id: str, expansion_details: str, roadmap):
        """Legacy method - node expansion now handled via function calling"""
        from fastapi import HTTPException
        raise HTTPException(status_code=501, detail="Use chat interface for node expansion")
    
    async def edit_node(self, node_id: str, edit_instructions: str, roadmap):
        """Legacy method - node editing now handled via function calling"""
        from fastapi import HTTPException
        raise HTTPException(status_code=501, detail="Use chat interface for node editing")
