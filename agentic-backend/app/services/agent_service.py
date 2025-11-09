from typing import List, Dict, Any, Tuple, Optional
import openai
from openai import AsyncOpenAI
import os
from fastapi import HTTPException
from app.core.config import settings
from app.models.agent import (
    ProjectSpecification, RoadmapNode, Roadmap, 
    ChatMessage, ConversationState, SubTask, ProjectTag
)
import json
import uuid
from datetime import datetime

class AgentService:
    """Main agent service for handling project roadmap conversations using function calling"""
    
    def __init__(self):
        # Initialize client with GROQ/OpenAI fallback logic
        groq_key = settings.GROQ_KEY
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
            raise ValueError("No valid API key found. Please provide either GROQ_KEY or OPENAI_API_KEY in environment variables or config.")
            
        self.tools = self._define_tools()
    
    def _define_tools(self):
        """Define all available tools for the agent"""
        return [
            {
                "type": "function",
                "function": {
                    "name": "ask_clarifying_question",
                    "description": "Ask a focused question to gather more project information",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "question": {
                                "type": "string",
                                "description": "A concise, focused question about the project"
                            },
                            "category": {
                                "type": "string",
                                "enum": ["title", "description", "goals", "timeline", "tech_stack", "experience", "deployment", "auth", "audience", "commercial"],
                                "description": "What category of information this question is gathering"
                            }
                        },
                        "required": ["question", "category"]
                    }
                }
            },
            {
                "type": "function", 
                "function": {
                    "name": "confirm_specifications_complete",
                    "description": "Confirm that all project specifications have been gathered",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "summary": {
                                "type": "string",
                                "description": "A brief summary of the project specifications gathered"
                            }
                        },
                        "required": ["summary"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "generate_project_roadmap",
                    "description": "Generate a structured roadmap for the project",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "project_title": {"type": "string"},
                            "project_description": {"type": "string"},
                            "nodes": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "id": {"type": "string"},
                                        "title": {"type": "string"},
                                        "description": {"type": "string"},
                                        "subtasks": {
                                            "type": "array",
                                            "items": {
                                                "type": "object",
                                                "properties": {
                                                    "id": {"type": "string"},
                                                    "title": {"type": "string"},
                                                    "description": {"type": "string"},
                                                    "estimated_hours": {"type": "number"}
                                                },
                                                "required": ["id", "title", "description"]
                                            }
                                        },
                                        "estimated_days": {"type": "integer"},
                                        "estimated_hours": {"type": "number"},
                                        "tags": {
                                            "type": "array",
                                            "items": {
                                                "type": "string",
                                                "enum": ["setup", "mvp", "frontend", "backend", "auth", "database", "deployment", "testing", "documentation", "design", "api", "integration", "optimization", "security"]
                                            }
                                        },
                                        "dependencies": {
                                            "type": "array",
                                            "items": {"type": "string"}
                                        },
                                        "deliverables": {
                                            "type": "array",
                                            "items": {"type": "string"}
                                        },
                                        "success_criteria": {
                                            "type": "array",
                                            "items": {"type": "string"}
                                        }
                                    },
                                    "required": ["id", "title", "description", "estimated_days", "estimated_hours", "tags"]
                                }
                            }
                        },
                        "required": ["project_title", "project_description", "nodes"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "expand_roadmap_node",
                    "description": "Add new roadmap nodes that branch from an existing node to expand project scope. ONLY use this after gathering specific details about what to expand and which node to branch from.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "base_node_id": {
                                "type": "string", 
                                "description": "The ID of the existing node to expand from"
                            },
                            "expansion_reason": {
                                "type": "string",
                                "description": "Why this expansion is needed (e.g., 'add authentication', 'new dashboard feature')"
                            },
                            "new_nodes": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "id": {"type": "string"},
                                        "title": {"type": "string"},
                                        "description": {"type": "string"},
                                        "subtasks": {
                                            "type": "array",
                                            "items": {
                                                "type": "object",
                                                "properties": {
                                                    "id": {"type": "string"},
                                                    "title": {"type": "string"},
                                                    "description": {"type": "string"},
                                                    "estimated_hours": {"type": "number"}
                                                },
                                                "required": ["id", "title", "description"]
                                            }
                                        },
                                        "estimated_days": {"type": "integer"},
                                        "estimated_hours": {"type": "number"},
                                        "tags": {
                                            "type": "array",
                                            "items": {
                                                "type": "string",
                                                "enum": ["setup", "mvp", "frontend", "backend", "auth", "database", "deployment", "testing", "documentation", "design", "api", "integration", "optimization", "security"]
                                            }
                                        },
                                        "dependencies": {
                                            "type": "array",
                                            "items": {"type": "string"}
                                        },
                                        "deliverables": {
                                            "type": "array",
                                            "items": {"type": "string"}
                                        },
                                        "success_criteria": {
                                            "type": "array",
                                            "items": {"type": "string"}
                                        }
                                    },
                                    "required": ["id", "title", "description", "estimated_days", "estimated_hours", "tags"]
                                }
                            }
                        },
                        "required": ["base_node_id", "expansion_reason", "new_nodes"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "add_subtasks_to_node",
                    "description": "Add more detailed subtasks to an existing roadmap node",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "node_id": {"type": "string"},
                            "additional_subtasks": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "id": {"type": "string"},
                                        "title": {"type": "string"},
                                        "description": {"type": "string"},
                                        "estimated_hours": {"type": "number"}
                                    },
                                    "required": ["id", "title", "description"]
                                }
                            },
                            "updated_total_hours": {"type": "number"}
                        },
                        "required": ["node_id", "additional_subtasks"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "edit_roadmap_node", 
                    "description": "Modify an existing roadmap node. ONLY use this after gathering specific details about which node to edit and what changes to make.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "node_id": {"type": "string"},
                            "updated_fields": {
                                "type": "object",
                                "properties": {
                                    "title": {"type": "string"},
                                    "description": {"type": "string"},
                                    "estimated_days": {"type": "integer"},
                                    "estimated_hours": {"type": "number"},
                                    "tags": {"type": "array", "items": {"type": "string"}},
                                    "deliverables": {"type": "array", "items": {"type": "string"}},
                                    "success_criteria": {"type": "array", "items": {"type": "string"}}
                                }
                            }
                        },
                        "required": ["node_id", "updated_fields"]
                    }
                }
            }
        ]
    
    
    async def process_message(
        self, 
        user_message: str, 
        conversation_state: ConversationState,
        action_type: str = "chat"
    ) -> Tuple[str, ConversationState, Optional[str]]:
        """
        Process user message using function calling with explicit action type
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
        
        # Create system prompt based on current phase and action type
        system_prompt = self._get_system_prompt(actual_phase, action_type)
        
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
                tools=self._get_available_tools(action_type, conversation_state),
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
                # Regular text response
                agent_response = message.content.strip()
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
    
    def _get_system_prompt(self, phase: str, action_type: str = "chat") -> str:
        """Get appropriate system prompt based on conversation phase and action type"""
        
        if phase == "discovery":
            if action_type in ["edit", "expand"]:
                return """You cannot edit or expand a roadmap that doesn't exist yet. 

You need to create a roadmap first by gathering project specifications. Ask clarifying questions to understand the project requirements, then generate the initial roadmap.

Use the ask_clarifying_question function to gather project information."""
            
            return """You are a concise project planning agent. Your job is to gather project specifications through targeted questions.

You need to understand:
- Project title and description
- Main goals and objectives  
- Timeline expectations (in weeks)
- Tech stack preferences
- User's experience level (beginner/intermediate/advanced)
- Whether they need deployment/auth
- If it's for portfolio or commercial use
- Target audience

Use the ask_clarifying_question function to ask ONE focused question at a time. Be concise and direct.

When you have enough information, use confirm_specifications_complete function."""
            
        elif phase == "confirmation":
            return """The user has provided project specifications. Confirm understanding and prepare for roadmap generation.

Use confirm_specifications_complete to summarize what you've learned."""
            
        elif phase == "generation":
            if action_type in ["edit", "expand"]:
                return """You cannot edit or expand a roadmap that doesn't exist yet.

First, generate the initial roadmap based on the project specifications that have been gathered.

Use generate_project_roadmap function to create 4-8 actionable milestone nodes."""
            
            return """Generate a detailed project roadmap based on the gathered specifications.

Use generate_project_roadmap function to create 4-8 actionable milestone nodes."""
            
        elif phase == "editing":
            if action_type == "expand":
                return """The user wants to EXPAND the roadmap by adding new features or scope.

IMPORTANT: You must ask clarifying questions first to understand:
- What new feature/functionality they want to add
- Which existing node it should branch from
- Any specific requirements or constraints

Only use expand_roadmap_node function after you have gathered enough details about the expansion.
Do NOT expand immediately - ask questions first to ensure you understand their requirements."""
                
            elif action_type == "edit":
                return """The user wants to EDIT an existing roadmap node.

IMPORTANT: You must ask clarifying questions first to understand:
- Which specific node they want to edit
- What aspects they want to change (title, description, timeline, deliverables, etc.)
- The specific changes they want to make

Only use edit_roadmap_node function after you have gathered enough details about the edits.
Do NOT edit immediately - ask questions first to ensure you understand their requirements."""
                
            else:  # action_type == "chat" or default
                return """You are in general chat mode. Help the user with questions about their roadmap, provide guidance, or clarify their needs.

If they mention wanting to expand or edit something, remind them to use the appropriate action mode (Expand or Edit) from the dropdown for those operations.

You can use add_subtasks_to_node if they want to break down existing work into more detailed steps."""
            
        return "I'm here to help you plan your project roadmap."
    
    async def _handle_function_calls(
        self, 
        tool_calls, 
        conversation_state: ConversationState,
        action_type: str = "chat"
    ) -> Tuple[str, ConversationState, Optional[str]]:
        """Process function calls from the LLM"""
        
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            if function_name == "ask_clarifying_question":
                return await self._handle_clarifying_question(function_args, conversation_state, action_type)
                
            elif function_name == "confirm_specifications_complete":
                return await self._handle_specifications_complete(function_args, conversation_state)
                
            elif function_name == "generate_project_roadmap":
                return await self._handle_roadmap_generation(function_args, conversation_state)
                
            elif function_name == "expand_roadmap_node":
                return await self._handle_node_expansion(function_args, conversation_state)
                
            elif function_name == "add_subtasks_to_node":
                return await self._handle_add_subtasks(function_args, conversation_state)
                
            elif function_name == "edit_roadmap_node":
                return await self._handle_node_editing(function_args, conversation_state)
        
        return "I'm not sure how to help with that.", conversation_state, None
    
    async def _handle_clarifying_question(
        self, 
        function_args: Dict, 
        conversation_state: ConversationState,
        action_type: str = "chat"
    ) -> Tuple[str, ConversationState, Optional[str]]:
        """Handle clarifying question function call"""
        
        question = function_args["question"]
        category = function_args["category"]
        
        # Add context about what action we're clarifying for
        if action_type == "expand":
            question_with_context = f"[Expansion Planning] {question}"
        elif action_type == "edit":
            question_with_context = f"[Node Editing] {question}"
        else:
            question_with_context = question
        
        conversation_state.messages.append(
            ChatMessage(
                role="assistant",
                content=question_with_context,
                timestamp=datetime.now().isoformat(),
                action_type="clarifying_question"
            )
        )
        
        return question_with_context, conversation_state, None
    
    async def _handle_specifications_complete(
        self, 
        function_args: Dict, 
        conversation_state: ConversationState
    ) -> Tuple[str, ConversationState, Optional[str]]:
        """Handle specifications complete confirmation"""
        
        summary = function_args["summary"]
        
        conversation_state.phase = "confirmation"
        conversation_state.specifications_complete = True
        
        response = "Ok I think I fully understand your project's specifications\n\n" + summary
        
        conversation_state.messages.append(
            ChatMessage(
                role="assistant",
                content=response,
                timestamp=datetime.now().isoformat(),
                action_type="specifications_complete"
            )
        )
        
        return response, conversation_state, "generate_roadmap"
    
    async def _handle_roadmap_generation(
        self, 
        function_args: Dict, 
        conversation_state: ConversationState
    ) -> Tuple[str, ConversationState, Optional[str]]:
        """Handle roadmap generation function call"""
        
        try:
            # Extract project specifications
            project_spec = ProjectSpecification(
                title=function_args["project_title"],
                description=function_args["project_description"],
                goals=["Build the project", "Deploy successfully"],  # Could extract from conversation
                timeline_weeks=4,  # Default
                tech_stack=[],  # Could extract from conversation
                user_experience_level="beginner",
                deployment_needed=True,
                auth_needed=False,
                commercialization_goal=False,
                target_audience="General users",
                similar_projects_built=False
            )
            
            # Create roadmap nodes
            nodes = []
            for node_data in function_args["nodes"]:
                # Create subtasks
                subtasks = []
                for subtask_data in node_data.get("subtasks", []):
                    subtasks.append(SubTask(
                        id=subtask_data["id"],
                        title=subtask_data["title"],
                        description=subtask_data["description"],
                        completed=False,
                        estimated_hours=subtask_data.get("estimated_hours")
                    ))
                
                # Create node
                node = RoadmapNode(
                    id=node_data["id"],
                    title=node_data["title"],
                    description=node_data["description"],
                    subtasks=subtasks,
                    estimated_days=node_data["estimated_days"],
                    estimated_hours=node_data["estimated_hours"],
                    tags=[ProjectTag(tag) for tag in node_data["tags"]],
                    dependencies=node_data.get("dependencies", []),
                    status="pending",
                    completion_percentage=0,
                    deliverables=node_data.get("deliverables", []),
                    success_criteria=node_data.get("success_criteria", [])
                )
                nodes.append(node)
            
            # Create complete roadmap
            roadmap = Roadmap(
                project_specification=project_spec,
                nodes=nodes,
                total_estimated_weeks=self._calculate_total_weeks([n.dict() for n in nodes]),
                total_estimated_hours=sum(node.estimated_hours for node in nodes)
            )
            
            conversation_state.current_roadmap = roadmap
            conversation_state.phase = "editing"
            
            response = f"I've generated a roadmap for '{project_spec.title}' with {len(nodes)} main milestones. You can now expand or edit any nodes as needed."
            
            conversation_state.messages.append(
                ChatMessage(
                    role="assistant",
                    content=response,
                    timestamp=datetime.now().isoformat(),
                    action_type="roadmap_generated"
                )
            )
            
            return response, conversation_state, None
            
        except Exception as e:
            return f"Failed to generate roadmap: {str(e)}", conversation_state, None
    
    async def _handle_node_expansion(
        self, 
        function_args: Dict, 
        conversation_state: ConversationState
    ) -> Tuple[str, ConversationState, Optional[str]]:
        """Handle roadmap expansion - adding new nodes that branch from existing node"""
        
        base_node_id = function_args["base_node_id"]
        expansion_reason = function_args["expansion_reason"]
        new_nodes_data = function_args["new_nodes"]
        
        if not conversation_state.current_roadmap:
            return "No roadmap available to expand.", conversation_state, None
        
        # Verify base node exists
        base_node = None
        for node in conversation_state.current_roadmap.nodes:
            if node.id == base_node_id:
                base_node = node
                break
        
        if not base_node:
            return f"Base node '{base_node_id}' not found in current roadmap.", conversation_state, None
        
        # Create new roadmap nodes
        new_nodes = []
        for node_data in new_nodes_data:
            # Create subtasks
            subtasks = []
            for subtask_data in node_data.get("subtasks", []):
                subtasks.append(SubTask(
                    id=subtask_data["id"],
                    title=subtask_data["title"],
                    description=subtask_data["description"],
                    completed=False,
                    estimated_hours=subtask_data.get("estimated_hours")
                ))
            
            # Create new node with dependency on base node
            dependencies = node_data.get("dependencies", [])
            if base_node_id not in dependencies:
                dependencies.append(base_node_id)  # Ensure new nodes depend on base node
            
            new_node = RoadmapNode(
                id=node_data["id"],
                title=node_data["title"],
                description=node_data["description"],
                subtasks=subtasks,
                estimated_days=node_data["estimated_days"],
                estimated_hours=node_data["estimated_hours"],
                tags=[ProjectTag(tag) for tag in node_data["tags"]],
                dependencies=dependencies,
                status="pending",
                completion_percentage=0,
                deliverables=node_data.get("deliverables", []),
                success_criteria=node_data.get("success_criteria", [])
            )
            new_nodes.append(new_node)
        
        # Add new nodes to roadmap
        conversation_state.current_roadmap.nodes.extend(new_nodes)
        
        # Update total estimates
        total_hours = sum(node.estimated_hours for node in conversation_state.current_roadmap.nodes)
        conversation_state.current_roadmap.total_estimated_hours = total_hours
        conversation_state.current_roadmap.total_estimated_weeks = self._calculate_total_weeks(
            [node.dict() for node in conversation_state.current_roadmap.nodes]
        )
        
        response = f"Expanded roadmap with {len(new_nodes)} new nodes for '{expansion_reason}'. These branch from '{base_node.title}' and add {sum(n.estimated_hours for n in new_nodes):.1f} hours to the project."
        
        conversation_state.messages.append(
            ChatMessage(
                role="assistant",
                content=response,
                timestamp=datetime.now().isoformat(),
                action_type="roadmap_expanded"
            )
        )
        
        return response, conversation_state, None
    
    async def _handle_add_subtasks(
        self, 
        function_args: Dict, 
        conversation_state: ConversationState
    ) -> Tuple[str, ConversationState, Optional[str]]:
        """Handle adding subtasks to an existing node"""
        
        node_id = function_args["node_id"]
        additional_subtasks = function_args["additional_subtasks"]
        
        # Find and update the node in current roadmap
        if conversation_state.current_roadmap:
            for node in conversation_state.current_roadmap.nodes:
                if node.id == node_id:
                    # Add new subtasks
                    for subtask_data in additional_subtasks:
                        new_subtask = SubTask(
                            id=subtask_data["id"],
                            title=subtask_data["title"],
                            description=subtask_data["description"],
                            completed=False,
                            estimated_hours=subtask_data.get("estimated_hours")
                        )
                        node.subtasks.append(new_subtask)
                    
                    # Update estimated hours if provided
                    if "updated_total_hours" in function_args:
                        node.estimated_hours = function_args["updated_total_hours"]
                    
                    response = f"Added {len(additional_subtasks)} additional subtasks to '{node.title}'."
                    break
            else:
                response = f"Node '{node_id}' not found in current roadmap."
        else:
            response = "No roadmap available to modify."
        
        conversation_state.messages.append(
            ChatMessage(
                role="assistant",
                content=response,
                timestamp=datetime.now().isoformat(),
                action_type="subtasks_added"
            )
        )
        
        return response, conversation_state, None
    
    async def _handle_node_editing(
        self, 
        function_args: Dict, 
        conversation_state: ConversationState
    ) -> Tuple[str, ConversationState, Optional[str]]:
        """Handle node editing function call"""
        
        node_id = function_args["node_id"]
        updated_fields = function_args["updated_fields"]
        
        # Find and update the node in current roadmap
        if conversation_state.current_roadmap:
            for node in conversation_state.current_roadmap.nodes:
                if node.id == node_id:
                    # Update fields
                    for field, value in updated_fields.items():
                        if hasattr(node, field):
                            if field == "tags":
                                setattr(node, field, [ProjectTag(tag) for tag in value])
                            else:
                                setattr(node, field, value)
                    
                    response = f"Updated '{node.title}' with new specifications."
                    break
            else:
                response = f"Node '{node_id}' not found in current roadmap."
        else:
            response = "No roadmap available to edit."
        
        conversation_state.messages.append(
            ChatMessage(
                role="assistant",
                content=response,
                timestamp=datetime.now().isoformat(),
                action_type="node_edited"
            )
        )
        
        return response, conversation_state, None
    
    def _get_conversation_summary(self, conversation_state: ConversationState) -> str:
        """Get a summary of the conversation for context"""
        messages = conversation_state.messages[-10:]  # Last 10 messages
        return "\n".join([f"{msg.role}: {msg.content}" for msg in messages])
    
    def _calculate_total_weeks(self, nodes: List[Dict]) -> int:
        """Calculate total estimated weeks from nodes"""
        total_days = sum(node.get("estimated_days", 0) for node in nodes)
        return max(1, (total_days + 6) // 7)  # Round up to nearest week
    
    def _get_available_tools(self, action_type: str, conversation_state: ConversationState):
        """Get tools available for the specific action type and phase"""
        
        # If no roadmap exists, only allow discovery and generation tools
        if not conversation_state.current_roadmap:
            return [tool for tool in self.tools 
                   if tool["function"]["name"] in ["ask_clarifying_question", "confirm_specifications_complete", "generate_project_roadmap"]]
        
        # If roadmap exists, filter by action type
        if action_type == "expand":
            # For expansion: only allow clarifying questions and expansion function
            return [tool for tool in self.tools 
                   if tool["function"]["name"] in ["ask_clarifying_question", "expand_roadmap_node"]]
                   
        elif action_type == "edit":
            # For editing: only allow clarifying questions and edit function
            return [tool for tool in self.tools 
                   if tool["function"]["name"] in ["ask_clarifying_question", "edit_roadmap_node"]]
                   
        else:  # action_type == "chat" or default
            # For chat: allow all tools except expand and edit (those need explicit action selection)
            return [tool for tool in self.tools 
                   if tool["function"]["name"] not in ["expand_roadmap_node", "edit_roadmap_node"]]
    
    def _determine_phase(self, conversation_state: ConversationState, action_type: str) -> str:
        """Determine the actual phase based on conversation state and action type"""
        
        # If no roadmap exists, we must go through discovery -> generation first
        if not conversation_state.current_roadmap:
            if not conversation_state.specifications_complete:
                return "discovery"
            else:
                return "generation"
        
        # If roadmap exists, we're in editing phase (unless explicitly generating)
        if conversation_state.current_roadmap and action_type != "generate":
            return "editing"
        
        # Default to the stored phase
        return conversation_state.phase or "discovery"
    
    # Legacy methods for backward compatibility - now use function calling instead
    async def generate_roadmap(self, conversation_state: ConversationState) -> Roadmap:
        """Legacy method - roadmap generation now handled via function calling"""
        if conversation_state.current_roadmap:
            return conversation_state.current_roadmap
        raise HTTPException(status_code=400, detail="No roadmap generated yet")
    
    async def expand_node(self, node_id: str, expansion_details: str, roadmap: Roadmap) -> List[RoadmapNode]:
        """Legacy method - node expansion now handled via function calling"""
        raise HTTPException(status_code=501, detail="Use chat interface for node expansion")
    
    async def edit_node(self, node_id: str, edit_instructions: str, roadmap: Roadmap) -> RoadmapNode:
        """Legacy method - node editing now handled via function calling"""
        raise HTTPException(status_code=501, detail="Use chat interface for node editing")