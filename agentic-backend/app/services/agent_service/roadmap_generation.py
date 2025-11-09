"""
Roadmap generation handler for the agent service.
Handles the discovery, confirmation, and initial roadmap generation phases.
"""

import json
import uuid
from datetime import datetime
from typing import Dict, Tuple, Optional
from openai import AsyncOpenAI

from app.models.agent import (
    ProjectSpecification, RoadmapNode, Roadmap, 
    ChatMessage, ConversationState, SubTask, ProjectTag
)


class RoadmapGenerationHandler:
    """Handles roadmap generation workflow: discovery → confirmation → generation"""
    
    def __init__(self, client: AsyncOpenAI, client_mode: str, model: str, max_tokens: int, temperature: float, tools: list):
        self.client = client
        self.client_mode = client_mode
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.tools = tools
    
    def get_system_prompt(self, phase: str, conversation_state: ConversationState = None) -> str:
        """Get system prompt for roadmap generation phases"""
        
        if phase == "discovery":
            # Check if we have enough comprehensive information
            message_count = len(conversation_state.messages) if conversation_state.messages else 0
            
            # Look for sufficient detail in the conversation - need more than just basic info
            conversation_text = " ".join([msg.content.lower() for msg in conversation_state.messages if msg.role == "user"])
            
            # Check for key information areas
            has_features = any(keyword in conversation_text for keyword in ["feature", "function", "capability", "workflow", "user can", "should allow", "will have"])
            has_goals = any(keyword in conversation_text for keyword in ["goal", "purpose", "objective", "solve", "help", "problem"])
            has_users = any(keyword in conversation_text for keyword in ["user", "audience", "customer", "team", "people"])
            has_tech_details = any(keyword in conversation_text for keyword in ["react", "python", "database", "api", "backend", "frontend"])
            
            # Only move to confirmation if we have substantial information (12+ messages AND key details)
            if message_count >= 16 and has_features and has_goals and has_users:  # More thorough discovery
                return """You have gathered comprehensive project information through detailed questioning. 

IMPORTANT: You must now use the confirm_specifications_complete function to summarize what you've learned and move to roadmap generation.

Include a detailed summary covering:
- The core problem/purpose of the project
- Key features and functionality
- Target users and their needs
- Technical approach and requirements
- Timeline and scope

Do NOT ask more questions. Use confirm_specifications_complete with a comprehensive summary."""
            
            return """You are an efficiency-focused project planning agent. Your job is to help students build ambitious projects by removing friction and maximizing development speed.

FOCUS ON EFFICIENCY & SPEED:
- Students have limited time but can build complex projects with the right approach
- Emphasize rapid iteration and quick wins to maintain momentum
- Remove setup friction - suggest proven, fast-to-implement patterns
- Focus on getting a working prototype fast, then iterate
- Prioritize features that provide maximum learning and portfolio value

You MUST gather information about:

**Project Vision & MVP Strategy:**
- What's the core value proposition of this project?
- What are the 3-4 features that would make this genuinely useful?
- What's the fastest way to prove the concept works?
- How can we get to a "demo-able" version quickly?

**Development Efficiency & Tech Stack:**
- What's their experience level and preferred technologies?
- Are there existing tools/libraries that can accelerate development?
- What's the fastest database/auth setup for their needs?
- Should they use templates/boilerplates to skip repetitive setup?
- Which APIs/services can replace custom development?

**Smart Implementation Patterns:**
- Which feature should they build FIRST to see immediate progress?
- How can they leverage existing APIs/services instead of building from scratch?
- What's the quickest deployment strategy? (Vercel, Railway, Heroku, or their preference)
- For auth: Use Clerk/Supabase/Firebase or simple demo users?
- What essential libraries will speed up development?

**Momentum & Learning:**
- How can they break work into focused 2-4 hour sessions?
- What sequence builds the most momentum?
- Which parts offer the best learning opportunities?
- How can they validate ideas quickly before investing more time?

IMPORTANT: Pay special attention to tech stack preferences as this will determine the "Project Setup & Environment" recommendations (always the first milestone). If they're unsure about tech stack, suggest React + FastAPI as a proven, beginner-friendly combination.

Ask strategic questions that help them build something impressive efficiently. Focus on smart shortcuts, proven patterns, and maintaining development momentum.

Use the ask_clarifying_question function to ask ONE focused question at a time."""
            
        elif phase == "confirmation":
            return """The user has confirmed they want to proceed with roadmap generation.

IMPORTANT: Use the generate_high_level_roadmap function to create an EFFICIENCY-FOCUSED roadmap structure.

CRITICAL: Always start with a "Project Setup & Environment" node as the first milestone.

EFFICIENCY-FOCUSED PROJECT REQUIREMENTS:
- 4-6 milestone nodes total (including mandatory setup node)
- Node 1: ALWAYS "Project Setup & Environment" (2-4 hours, same day setup)
- Nodes 2-5: Feature milestones (10-25 hours each)
- Total timeline: 4-8 weeks (setup doesn't add extra time)
- Focus on rapid prototyping and iterative development
- Each milestone builds toward a functional, portfolio-worthy project

Node 1 "Project Setup & Environment" should include:
- Quick frontend setup (user's preferred stack or React + Vite if unsure)
- Quick backend setup (user's preferred stack or FastAPI if unsure)
- Essential dev tools only (Git init, basic .env template)
- Core dependencies for immediate productivity
- Basic project structure and README template
- Deploy-ready configuration (platform based on their preference)
- Get coding ASAP - polish later

Nodes 2-6 should be feature milestones that:
- Build on the solid foundation from Node 1
- Are demo-able working features
- Use the tools and structure established in setup
- Progress logically toward a complete MVP

Generate the high-level roadmap structure now - subtasks will be added in the next step."""
            
        elif phase == "generation":
            return """Generate an efficiency-focused project roadmap based on the gathered specifications.

IMPORTANT: Focus on creating strategic, momentum-building milestones that maximize development speed.

CRITICAL: Always start with a "Project Setup & Environment" node as milestone #1.

EFFICIENCY-FOCUSED PROJECT GUIDELINES:
- 4-6 milestone nodes total (including mandatory setup)
- Node 1: "Project Setup & Environment" (2-4 hours, same day)
- Nodes 2-5: Feature milestones (10-25 hours each, 1-2 weeks)
- Total timeline: 4-8 weeks (setup adds minimal overhead)
- Focus on rapid prototyping and iterative improvement
- Leverage existing tools, libraries, and services

Use generate_high_level_roadmap function to create milestones:

**Node 1 - "Project Setup & Environment" (MANDATORY - 1-2 hours):**
- Lightning-fast frontend setup (user's preferred stack/framework)
- Quick backend setup (user's preferred backend technology)
- Essential dev environment (Git, .env, basic configs)
- Core libraries for immediate productivity
- Basic project structure to start coding immediately
- Deploy-ready configs (focus on speed, not perfection)

**Nodes 2-5 - Feature Development:**
- Build on the solid foundation from Node 1
- Each milestone delivers complete working functionality
- Use proven tech stacks and patterns for speed
- Emphasize learning while building portfolio value
- Can be accomplished with focused, time-boxed effort

Examples of efficient feature milestones:
- "Core functionality prototype" (prove the concept works)
- "User authentication & data persistence"
- "Main feature implementation" (complete the primary use case)
- "Polish, testing & production deployment"

Subtasks will be generated in a separate step to avoid rate limiting."""
            
        elif phase == "overview_generation":
            return """Generate a high-level development strategy overview for the project setup node.

You now have the complete roadmap structure. Create a comprehensive overview that shows students the complete journey from setup to deployment.

IMPORTANT: Use the generate_project_overview function to create a step-by-step development strategy.

The overview should:
- Show the logical progression from setup through all milestones to deployment
- Help students understand how each phase builds on the previous one
- Include specific pages, features, and integrations that will be built
- Focus on the core user journey and main functionality
- Be inspiring and actionable, showing a clear path to success

Create 5-10 strategic steps that outline:
1. Project setup and environment configuration
2. Core pages and authentication system  
3. Main feature development and functionality
4. User experience and interface polish
5. Testing, deployment, and iteration

Each step should be clear, specific, and show how it contributes to the final product."""
            
        elif phase == "subtask_generation":
            # Get the next node that needs subtasks
            if hasattr(conversation_state, 'nodes_needing_subtasks') and conversation_state.nodes_needing_subtasks:
                next_node_id = conversation_state.nodes_needing_subtasks[0]
                next_node = None
                if conversation_state.current_roadmap:
                    next_node = next((n for n in conversation_state.current_roadmap.nodes if n.id == next_node_id), None)
                
                if next_node:
                    # Check if this is a setup node for special handling
                    is_setup_node = "setup" in next_node.tags if hasattr(next_node, 'tags') else False
                    setup_guidance = ""
                    
                    if is_setup_node or "setup" in next_node.title.lower() or "environment" in next_node.title.lower():
                        setup_guidance = """

SETUP NODE SPECIAL REQUIREMENTS:
This is a QUICK project setup node (2-4 hours max). Focus on speed and getting to coding ASAP:
- Frontend: Use their preferred stack (React/Vue/Angular/Next.js) with fastest setup
- Backend: Use their preferred stack (FastAPI/Express/Django/Flask) with minimal config
- Dev tools: Git init, basic .env template, minimal configs for their stack
- Focus on essentials only - no over-engineering
- Get to working "Hello World" endpoints/pages quickly
- Detailed setup and polish can happen later during development"""
                    
                    return f"""Generate efficient, actionable subtasks for the roadmap node: "{next_node.title}"

IMPORTANT: Use the generate_node_subtasks function immediately to create EFFICIENCY-FOCUSED subtasks for node ID "{next_node_id}".

Node Description: {next_node.description}
Estimated Hours: {next_node.estimated_hours}{setup_guidance}

Create 3-4 focused subtasks optimized for rapid development:
- Subtask titles: Max 40 characters, action-oriented
- Subtask descriptions: Max 60 characters, specific outcomes
- Time estimates: 2-8 hours each (focused work sessions)
- Emphasize speed and momentum over perfection

EFFICIENCY PATTERNS:
- "Set up [X] with [proven tool/template]" instead of "Design [X] from scratch"
- "Implement core [feature] using [library/service]" - leverage existing solutions
- "Deploy to [platform] and test" instead of "Configure complex infrastructure"
- "Add basic [functionality]" then "Enhance [functionality]" - iterate quickly

Focus on actionable steps that remove friction and maintain development momentum."""
            
            return """Generate efficient, actionable subtasks for roadmap nodes.

The high-level roadmap structure has been created. Now generate specific subtasks that maximize development speed and minimize friction.

EFFICIENCY-FOCUSED SUBTASK GUIDELINES:
- 3-4 subtasks per node maximum
- 2-8 hours each (focused work sessions)
- Subtask titles: Max 40 characters, action-oriented
- Subtask descriptions: Max 60 characters, specific outcomes  
- Emphasize rapid iteration and proven patterns

Use generate_node_subtasks function to create actionable tasks that leverage existing tools, remove setup friction, and maintain momentum."""
        
        return "I'm here to help you plan your project roadmap."
    
    def get_available_tools(self, phase: str):
        """Get tools available for roadmap generation phases"""
        
        if phase == "discovery":
            return [tool for tool in self.tools 
                   if tool["function"]["name"] in ["ask_clarifying_question", "confirm_specifications_complete"]]
        
        elif phase in ["confirmation", "generation"]:
            return [tool for tool in self.tools 
                   if tool["function"]["name"] in ["generate_high_level_roadmap"]]
        
        elif phase == "overview_generation":
            return [tool for tool in self.tools 
                   if tool["function"]["name"] in ["generate_project_overview"]]
        
        elif phase == "subtask_generation":
            return [tool for tool in self.tools 
                   if tool["function"]["name"] in ["generate_node_subtasks"]]
        
        return []
    
    async def handle_clarifying_question(
        self, 
        function_args: Dict, 
        conversation_state: ConversationState
    ) -> Tuple[str, ConversationState, Optional[str]]:
        """Handle clarifying question function call"""
        
        question = function_args["question"]
        category = function_args["category"]
        
        conversation_state.messages.append(
            ChatMessage(
                role="assistant",
                content=question,
                timestamp=datetime.now().isoformat(),
                action_type="clarifying_question"
            )
        )
        
        return question, conversation_state, None
    
    async def handle_specifications_complete(
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
    
    async def handle_high_level_roadmap_generation(
        self, 
        function_args: Dict, 
        conversation_state: ConversationState
    ) -> Tuple[str, ConversationState, Optional[str]]:
        """Handle high-level roadmap generation (Step 1 of 2-step process)"""
        
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
            
            # Create roadmap nodes WITHOUT subtasks initially
            nodes = []
            for node_data in function_args["nodes"]:
                node = RoadmapNode(
                    id=node_data["id"],
                    title=node_data["title"],
                    description=node_data["description"],
                    subtasks=[],  # Empty initially - will be populated in step 2
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
            conversation_state.phase = "overview_generation"
            
            # Store which nodes still need subtasks (will be used after overview generation)
            conversation_state.nodes_needing_subtasks = [node.id for node in nodes]
            
            # Find the setup node for overview generation
            setup_node = None
            for node in nodes:
                if "setup" in node.tags or "setup" in node.title.lower() or "environment" in node.title.lower():
                    setup_node = node
                    break
            
            if setup_node:
                # Generate overview for the setup node
                return await self.auto_generate_overview(conversation_state, setup_node.id)
            else:
                # No setup node found, skip to subtask generation
                conversation_state.phase = "subtask_generation"
                return await self.auto_generate_next_subtasks(conversation_state)
            
        except Exception as e:
            return f"Failed to generate high-level roadmap: {str(e)}", conversation_state, None
    
    async def handle_project_overview_generation(
        self, 
        function_args: Dict, 
        conversation_state: ConversationState
    ) -> Tuple[str, ConversationState, Optional[str]]:
        """Handle project overview generation for the setup node"""
        
        try:
            setup_node_id = function_args["setup_node_id"]
            overview_steps = function_args["overview"]
            
            if not conversation_state.current_roadmap:
                return "No roadmap available to add overview to.", conversation_state, None
            
            # Find the setup node to update
            setup_node = None
            for node in conversation_state.current_roadmap.nodes:
                if node.id == setup_node_id:
                    setup_node = node
                    break
            
            if not setup_node:
                return f"Setup node '{setup_node_id}' not found in current roadmap.", conversation_state, None
            
            # Add overview to the setup node
            setup_node.overview = overview_steps
            
            # Move to subtask generation phase
            conversation_state.phase = "subtask_generation"
            
            response = f"Added project overview to '{setup_node.title}' with {len(overview_steps)} strategic steps.\n\nNow generating detailed subtasks for all milestones..."
            
            conversation_state.messages.append(
                ChatMessage(
                    role="assistant",
                    content=response,
                    timestamp=datetime.now().isoformat(),
                    action_type="overview_generated"
                )
            )
            
            # Automatically start generating subtasks for the first node
            return await self.auto_generate_next_subtasks(conversation_state)
            
        except Exception as e:
            return f"Failed to generate project overview: {str(e)}", conversation_state, None
    
    async def auto_generate_overview(
        self, 
        conversation_state: ConversationState,
        setup_node_id: str
    ) -> Tuple[str, ConversationState, Optional[str]]:
        """Automatically generate overview for the setup node"""
        
        if not conversation_state.current_roadmap:
            return "No roadmap available for overview generation.", conversation_state, None
        
        # Get all roadmap nodes for context
        roadmap_context = []
        for node in conversation_state.current_roadmap.nodes:
            roadmap_context.append(f"- {node.title}: {node.description}")
        
        roadmap_summary = "\n".join(roadmap_context)
        
        system_prompt = f"""Generate a comprehensive project overview for the setup node that shows the complete development journey.

ROADMAP CONTEXT:
The complete roadmap contains these milestones:
{roadmap_summary}

PROJECT DETAILS:
- Title: {conversation_state.current_roadmap.project_specification.title}
- Description: {conversation_state.current_roadmap.project_specification.description}

IMPORTANT: Use the generate_project_overview function immediately to create a strategic overview.

Create 5-10 development steps that show:
1. How the project setup enables rapid development
2. The logical progression through each milestone
3. Key pages, features, and integrations that will be built
4. How each phase builds toward the final product
5. The complete user journey from concept to deployment

Focus on making students understand the big picture and feel excited about what they're building."""
        
        # Prepare messages for LLM
        messages = [{"role": "system", "content": system_prompt}]
        messages.append({"role": "user", "content": f"Generate a project overview for the setup node '{setup_node_id}'"})
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=[tool for tool in self.tools if tool["function"]["name"] == "generate_project_overview"],
                tool_choice={"type": "function", "function": {"name": "generate_project_overview"}},
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            # Process the response
            message = response.choices[0].message
            
            if message.tool_calls:
                # Handle the overview generation function call
                for tool_call in message.tool_calls:
                    if tool_call.function.name == "generate_project_overview":
                        try:
                            function_args = json.loads(tool_call.function.arguments)
                            return await self.handle_project_overview_generation(function_args, conversation_state)
                        except json.JSONDecodeError as e:
                            return f"Error parsing overview generation arguments: {str(e)}", conversation_state, None
            
            # If no tool calls, try to parse GROQ text format
            if self.client_mode == "groq" and message.content:
                # Import here to avoid circular import
                from .orchestrator import AgentOrchestrator
                return await AgentOrchestrator.parse_groq_function_call(message.content, conversation_state, "chat", self)
            
            return "Error: Could not generate overview automatically.", conversation_state, None
            
        except Exception as e:
            return f"Error in automatic overview generation: {str(e)}", conversation_state, None
    
    async def handle_node_subtasks_generation(
        self, 
        function_args: Dict, 
        conversation_state: ConversationState
    ) -> Tuple[str, ConversationState, Optional[str]]:
        """Handle subtask generation for a specific node (Step 2 of 2-step process)"""
        
        try:
            node_id = function_args["node_id"]
            subtasks_data = function_args["subtasks"]
            
            if not conversation_state.current_roadmap:
                return "No roadmap available to add subtasks to.", conversation_state, None
            
            # Find the node to update
            target_node = None
            for node in conversation_state.current_roadmap.nodes:
                if node.id == node_id:
                    target_node = node
                    break
            
            if not target_node:
                return f"Node '{node_id}' not found in current roadmap.", conversation_state, None
            
            # Create subtasks
            subtasks = []
            for subtask_data in subtasks_data:
                subtasks.append(SubTask(
                    id=subtask_data["id"],
                    title=subtask_data["title"],
                    description=subtask_data["description"],
                    completed=False,
                    estimated_hours=subtask_data["estimated_hours"]
                ))
            
            # Add subtasks to the node
            target_node.subtasks = subtasks
            
            # Update total estimated hours based on subtasks
            total_subtask_hours = sum(st.estimated_hours for st in subtasks if st.estimated_hours)
            if total_subtask_hours > 0:
                target_node.estimated_hours = total_subtask_hours
            
            # Remove this node from the nodes_needing_subtasks list
            if hasattr(conversation_state, 'nodes_needing_subtasks') and node_id in conversation_state.nodes_needing_subtasks:
                conversation_state.nodes_needing_subtasks.remove(node_id)
            
            # Check if all nodes have subtasks
            remaining_nodes = getattr(conversation_state, 'nodes_needing_subtasks', [])
            
            if remaining_nodes:
                # More nodes need subtasks - automatically generate the next one
                next_node_id = remaining_nodes[0]
                next_node = next((n for n in conversation_state.current_roadmap.nodes if n.id == next_node_id), None)
                next_node_title = next_node.title if next_node else "next milestone"
                
                response = f"Added {len(subtasks)} subtasks to '{target_node.title}'.\n\nGenerating subtasks for '{next_node_title}'..."
                
                conversation_state.messages.append(
                    ChatMessage(
                        role="assistant",
                        content=response,
                        timestamp=datetime.now().isoformat(),
                        action_type="subtasks_generated"
                    )
                )
                
                # Automatically generate subtasks for the next node
                return await self.auto_generate_next_subtasks(conversation_state)
            else:
                # All nodes have subtasks - roadmap is complete
                conversation_state.phase = "editing"
                
                # Update total roadmap estimates
                total_hours = sum(node.estimated_hours for node in conversation_state.current_roadmap.nodes)
                conversation_state.current_roadmap.total_estimated_hours = total_hours
                conversation_state.current_roadmap.total_estimated_weeks = self._calculate_total_weeks(
                    [node.dict() for node in conversation_state.current_roadmap.nodes]
                )
                
                response = f"Perfect! I've completed your roadmap with detailed subtasks for all {len(conversation_state.current_roadmap.nodes)} milestones.\n\nTotal estimated time: {total_hours:.1f} hours across {conversation_state.current_roadmap.total_estimated_weeks} weeks.\n\nYou can now expand or edit any nodes as needed!"
                
                conversation_state.messages.append(
                    ChatMessage(
                        role="assistant",
                        content=response,
                        timestamp=datetime.now().isoformat(),
                        action_type="roadmap_completed"
                    )
                )
                
                return response, conversation_state, None
            
        except Exception as e:
            return f"Failed to generate subtasks: {str(e)}", conversation_state, None
    
    async def auto_generate_next_subtasks(
        self, 
        conversation_state: ConversationState
    ) -> Tuple[str, ConversationState, Optional[str]]:
        """Automatically generate subtasks for the next node in the queue"""
        
        if not hasattr(conversation_state, 'nodes_needing_subtasks') or not conversation_state.nodes_needing_subtasks:
            # All subtasks have been generated - roadmap is complete
            conversation_state.phase = "editing"
            
            if conversation_state.current_roadmap:
                total_hours = sum(node.estimated_hours for node in conversation_state.current_roadmap.nodes)
                conversation_state.current_roadmap.total_estimated_hours = total_hours
                conversation_state.current_roadmap.total_estimated_weeks = self._calculate_total_weeks(
                    [node.dict() for node in conversation_state.current_roadmap.nodes]
                )
                
                response = f"Perfect! I've completed your roadmap with detailed subtasks for all {len(conversation_state.current_roadmap.nodes)} milestones.\n\nTotal estimated time: {total_hours:.1f} hours across {conversation_state.current_roadmap.total_estimated_weeks} weeks.\n\nYou can now expand or edit any nodes as needed!"
            else:
                response = "Roadmap generation completed."
            
            conversation_state.messages.append(
                ChatMessage(
                    role="assistant",
                    content=response,
                    timestamp=datetime.now().isoformat(),
                    action_type="roadmap_completed"
                )
            )
            
            return response, conversation_state, None
        
        # Get the next node that needs subtasks
        next_node_id = conversation_state.nodes_needing_subtasks[0]
        next_node = None
        if conversation_state.current_roadmap:
            next_node = next((n for n in conversation_state.current_roadmap.nodes if n.id == next_node_id), None)
        
        if not next_node:
            return "Error: Could not find next node for subtask generation.", conversation_state, None
        
        # Create system prompt for subtask generation
        # Check if this is a setup node for special handling
        is_setup_node = "setup" in next_node.tags if hasattr(next_node, 'tags') else False
        setup_guidance = ""
        
        if is_setup_node or "setup" in next_node.title.lower() or "environment" in next_node.title.lower():
            setup_guidance = """

SETUP NODE SPECIAL REQUIREMENTS:
This is a QUICK project setup node (2-4 hours max). Focus on speed and getting to coding ASAP:
- Frontend: Use their preferred stack (React/Vue/Angular/Next.js) with fastest setup
- Backend: Use their preferred stack (FastAPI/Express/Django/Flask) with minimal config
- Dev tools: Git init, basic .env template, minimal configs for their stack
- Focus on essentials only - no over-engineering
- Get to working "Hello World" endpoints/pages quickly
- Detailed setup and polish can happen later during development"""
        
        system_prompt = f"""Generate efficient, actionable subtasks for the roadmap node: "{next_node.title}"

IMPORTANT: Use the generate_node_subtasks function immediately to create EFFICIENCY-FOCUSED subtasks for node ID "{next_node_id}".

Node Description: {next_node.description}
Estimated Hours: {next_node.estimated_hours}{setup_guidance}

Create 3-4 focused subtasks optimized for rapid development:
- Subtask titles: Max 40 characters, action-oriented
- Subtask descriptions: Max 60 characters, specific outcomes
- Time estimates: 2-8 hours each (focused work sessions)
- Emphasize speed and momentum over perfection

EFFICIENCY PATTERNS:
- "Set up [X] with [proven tool/template]" instead of "Design [X] from scratch"
- "Implement core [feature] using [library/service]" - leverage existing solutions
- "Deploy to [platform] and test" instead of "Configure complex infrastructure"
- "Add basic [functionality]" then "Enhance [functionality]" - iterate quickly

Focus on actionable steps that remove friction and maintain development momentum."""
        
        # Prepare messages for LLM
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add a user message to trigger the generation
        messages.append({"role": "user", "content": f"Generate subtasks for '{next_node.title}'"})
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=[tool for tool in self.tools if tool["function"]["name"] == "generate_node_subtasks"],
                tool_choice={"type": "function", "function": {"name": "generate_node_subtasks"}},
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            # Process the response
            message = response.choices[0].message
            
            if message.tool_calls:
                # Handle the subtask generation function call
                for tool_call in message.tool_calls:
                    if tool_call.function.name == "generate_node_subtasks":
                        try:
                            function_args = json.loads(tool_call.function.arguments)
                            return await self.handle_node_subtasks_generation(function_args, conversation_state)
                        except json.JSONDecodeError as e:
                            return f"Error parsing subtask generation arguments: {str(e)}", conversation_state, None
            
            # If no tool calls, try to parse GROQ text format
            if self.client_mode == "groq" and message.content:
                # Import here to avoid circular import
                from .orchestrator import AgentOrchestrator
                return await AgentOrchestrator.parse_groq_function_call(message.content, conversation_state, "chat", self)
            
            return "Error: Could not generate subtasks automatically.", conversation_state, None
            
        except Exception as e:
            return f"Error in automatic subtask generation: {str(e)}", conversation_state, None
    
    def _calculate_total_weeks(self, nodes) -> int:
        """Calculate total estimated weeks from nodes"""
        total_days = sum(node.get("estimated_days", 0) for node in nodes)
        return max(1, (total_days + 6) // 7)  # Round up to nearest week
