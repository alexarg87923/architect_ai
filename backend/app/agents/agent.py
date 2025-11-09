from google.adk.agents import SequentialAgent, Agent
from google.adk.tools import google_search
from typing import List, Optional
from pydantic import BaseModel, Field

# There should be a multi-turn conversation for the LLM to understand the user's project intent and requirements.

"""
FIRST NODE SHOULD always be:
- quickstart project and environment setup
"""

"""
IMPORTANT must-knows for accurate project roadmap generation:

1. User would first describe their vision for the project and what they want to build.
- Then confirm with the user if you have understood their vision correctly.

2. Ask the user what type of project it would be.
OPTIONS:
- Web Application
- Mobile Application
- Desktop Application
- API
- Library
- Tool
- Other
THEN confirm with the user if you have understood the project more accurately.

2. Then dive into the details of the project:
- PUSH THIS BACK UNTIL THE EPICS ARE PROPOSED AND CONFIRMED. The tech stack that the user intends to use (if not specified, recommend tech stack that would be best suited for the project then confirm with the user)
- The project's core features and functionality
- The project's target users and their needs (could be just for yourself (personal projects) or for a specific audience).
THEN Propose Epics for the project then confirm with the user and break down the Epics into Stories (these would be the nodes of the roadmap).
- Identify the priority of Epics (what should be built first, what should be built next, etc.).

3. Create a system architecture diagram for the project in Mermaid syntax.
POTENTIAL COMPONENTS:
- Frontend
- Backend
- Database
- API
- Library
- Tool
- Other
(Add connections between components signaling the data flow and dependencies between them.)
THEN confirm with the user if you have understood the system architecture correctly.

***** This should be saved in an artifact file which is updated by the LLM as the conversation progresses (displayed on the Roadmap AI UI). *****

3. Once you have a clear understanding of the project, generate a roadmap for the project stored in JSON format.
- The roadmap should be a list of Epics and their respective Stories.
EXAMPLE JSON FORMAT for a todo list project:
"""

"""
LAST NODE SHOULD always be:
- Consolidation of the project --> deployment and launch or demo. Or potential roadmap expansion (adding more features i.e. Epics and Stories)
"""

# Goal of the roadmap is to give the user clarity on the project implementation, allowing the user to focus on implementation while consulting the roadmap plan.

from google.adk.agents import BaseAgent, LlmAgent, LoopAgent, SequentialAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event
from typing import AsyncGenerator
import logging

logger = logging.getLogger(__name__)

class ProjectContextAgent(BaseAgent):
    """
    Custom agent for gathering project context through structured multi-turn conversation.
    Uses conditional logic to ask follow-up questions based on user responses.
    
    Conversation Flow:
    1. Vision Clarification - Understand what the user wants to build
    2. Project Type Classification - Determine the type of project
    3. Requirements Gathering - Collect detailed requirements based on project type
    4. Epic & Story Planning - Break down project into manageable pieces
    5. Architecture Design - Create system architecture
    6. Final Confirmation - Validate complete understanding
    """
    
    # Declare sub-agents as Pydantic fields
    vision_clarifier: LlmAgent
    project_type_classifier: LlmAgent
    requirements_gatherer: LlmAgent
    epic_planner: LlmAgent
    architecture_designer: LlmAgent
    final_validator: LlmAgent
    
    # Allow complex types like LlmAgent
    model_config = {"arbitrary_types_allowed": True}
    
    def __init__(self, name: str = "ProjectContextAgent", **kwargs):
        # Create sub-agents for different conversation stages
        vision_clarifier = LlmAgent(
            name="VisionClarifier",
            model="gemini-2.0-flash-exp",
            instruction="""You are a project consultant helping users define their project vision.
            
            Your task:
            1. Listen to the user's project description
            2. Ask 1-2 clarifying questions to better understand their vision
            3. Confirm your understanding of what they want to build
            4. Set vision_confirmed to 'true' in your response if the vision is clear
            
            Be conversational and helpful. Focus on understanding the core purpose and goals of their project.""",
            output_key="vision_status"
        )
        
        project_type_classifier = LlmAgent(
            name="ProjectTypeClassifier", 
            model="gemini-2.0-flash-exp",
            instruction="""Based on the project vision, help determine the project type.
            
            Available options:
            - Web Application
            - Mobile Application  
            - Desktop Application
            - API
            - Library
            - Tool
            - Other
            
            Your task:
            1. Analyze the project vision from session state
            2. Suggest the most appropriate project type
            3. Ask for user confirmation
            4. Set project_type_confirmed to 'true' when confirmed
            
            Explain why you think this project type fits their vision.""",
            output_key="project_type_status"
        )
        
        requirements_gatherer = LlmAgent(
            name="RequirementsGatherer",
            model="gemini-2.0-flash-exp",
            instruction="""Gather detailed project requirements based on the confirmed project type and vision.
            
            Focus on:
            - Core features and functionality
            - Target users and their needs
            - Technical preferences (if any)
            - Priority and scope
            
            Adapt your questions based on the project type:
            - Web App: Frontend/backend needs, user auth, deployment
            - Mobile App: Platform choice, app store requirements
            - API: Endpoints, data models, authentication
            - Library/Tool: Use cases, interfaces, distribution
            
            Set requirements_complete to 'true' when you have sufficient detail.""",
            output_key="requirements_status"
        )
        
        epic_planner = LlmAgent(
            name="EpicPlanner",
            model="gemini-2.0-flash-exp", 
            instruction="""Based on the gathered requirements, propose Epics for the project.
            
            Your task:
            1. Break down the project into logical Epics (major feature areas)
            2. Suggest priority order for implementation
            3. For each Epic, outline the main Stories (specific features/tasks)
            4. Get user confirmation on the Epic breakdown
            
            Remember: First Epic should always be "Project Setup & Environment"
            Last Epic should always be "Deployment & Launch"
            
            Set epics_confirmed to 'true' when user approves the breakdown.""",
            output_key="epics_status"
        )
        
        architecture_designer = LlmAgent(
            name="ArchitectureDesigner",
            model="gemini-2.0-flash-exp",
            instruction="""Create a system architecture diagram for the project using Mermaid syntax.
            
            Based on project type and requirements, include relevant components:
            - Frontend (if applicable)
            - Backend (if applicable) 
            - Database (if needed)
            - API layers
            - External services
            - Libraries/Tools
            
            Show data flow and dependencies between components.
            Save the Mermaid diagram to an artifact for UI display.
            
            Set architecture_confirmed to 'true' when user approves the design.""",
            output_key="architecture_status"
        )
        
        final_validator = LlmAgent(
            name="FinalValidator",
            model="gemini-2.0-flash-exp",
            instruction="""Provide a comprehensive summary of the project context gathered.
            
            Include:
            - Project vision and goals
            - Project type and rationale
            - Key requirements and features
            - Epic breakdown with priorities
            - System architecture overview
            
            Ask for final confirmation that everything is accurate and complete.
            Generate the final roadmap JSON when confirmed.
            
            Set context_gathering_complete to 'true' when everything is confirmed.""",
            output_key="final_status"
        )
        
        super().__init__(
            name=name, 
            sub_agents=[
                vision_clarifier,
                project_type_classifier, 
                requirements_gatherer,
                epic_planner,
                architecture_designer,
                final_validator
            ],
            vision_clarifier=vision_clarifier,
            project_type_classifier=project_type_classifier,
            requirements_gatherer=requirements_gatherer,
            epic_planner=epic_planner,
            architecture_designer=architecture_designer,
            final_validator=final_validator,
            **kwargs
        )
    
    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
        """
        Implements the structured multi-turn conversation flow with conditional logic.
        """
        logger.info(f"[{self.name}] Starting project context gathering workflow.")
        
        # Initialize conversation state if not present
        if "conversation_stage" not in ctx.session.state:
            ctx.session.state["conversation_stage"] = "vision_clarification"
            ctx.session.state["vision_confirmed"] = False
            ctx.session.state["project_type_confirmed"] = False
            ctx.session.state["requirements_complete"] = False
            ctx.session.state["epics_confirmed"] = False
            ctx.session.state["architecture_confirmed"] = False
            ctx.session.state["context_gathering_complete"] = False
        
        # Stage 1: Vision Clarification
        if not ctx.session.state.get("vision_confirmed", False):
            logger.info(f"[{self.name}] Stage 1: Vision Clarification")
            ctx.session.state["conversation_stage"] = "vision_clarification"
            
            async for event in self.vision_clarifier.run_async(ctx):
                yield event
            
            # Check if vision is confirmed
            vision_status = ctx.session.state.get("vision_status", "")
            if "vision_confirmed" in vision_status and "true" in vision_status.lower():
                ctx.session.state["vision_confirmed"] = True
                logger.info(f"[{self.name}] Vision confirmed, moving to project type classification")
            else:
                logger.info(f"[{self.name}] Vision needs more clarification")
                return
        
        # Stage 2: Project Type Classification  
        if ctx.session.state.get("vision_confirmed") and not ctx.session.state.get("project_type_confirmed", False):
            logger.info(f"[{self.name}] Stage 2: Project Type Classification")
            ctx.session.state["conversation_stage"] = "project_type_classification"
            
            async for event in self.project_type_classifier.run_async(ctx):
                yield event
            
            # Check if project type is confirmed
            type_status = ctx.session.state.get("project_type_status", "")
            if "project_type_confirmed" in type_status and "true" in type_status.lower():
                ctx.session.state["project_type_confirmed"] = True
                logger.info(f"[{self.name}] Project type confirmed, moving to requirements gathering")
            else:
                logger.info(f"[{self.name}] Project type needs confirmation")
                return
        
        # Stage 3: Requirements Gathering (conditional based on project type)
        if (ctx.session.state.get("project_type_confirmed") and 
            not ctx.session.state.get("requirements_complete", False)):
            logger.info(f"[{self.name}] Stage 3: Requirements Gathering")
            ctx.session.state["conversation_stage"] = "requirements_gathering"
            
            # Customize requirements gathering based on project type
            project_type = ctx.session.state.get("project_type", "").lower()
            if "web application" in project_type:
                self.requirements_gatherer.instruction += "\n\nFocus especially on: Frontend framework preferences, backend technology, database needs, user authentication, hosting/deployment preferences."
            elif "mobile application" in project_type:
                self.requirements_gatherer.instruction += "\n\nFocus especially on: Platform choice (iOS/Android/Cross-platform), app store requirements, offline functionality, push notifications."
            elif "api" in project_type:
                self.requirements_gatherer.instruction += "\n\nFocus especially on: REST/GraphQL preference, authentication methods, rate limiting, documentation needs, versioning strategy."
            
            async for event in self.requirements_gatherer.run_async(ctx):
                yield event
            
            # Check if requirements are complete
            req_status = ctx.session.state.get("requirements_status", "")
            if "requirements_complete" in req_status and "true" in req_status.lower():
                ctx.session.state["requirements_complete"] = True
                logger.info(f"[{self.name}] Requirements complete, moving to epic planning")
            else:
                logger.info(f"[{self.name}] Requirements need more detail")
                return
        
        # Stage 4: Epic Planning
        if (ctx.session.state.get("requirements_complete") and 
            not ctx.session.state.get("epics_confirmed", False)):
            logger.info(f"[{self.name}] Stage 4: Epic Planning")
            ctx.session.state["conversation_stage"] = "epic_planning"
            
            async for event in self.epic_planner.run_async(ctx):
                yield event
            
            # Check if epics are confirmed
            epics_status = ctx.session.state.get("epics_status", "")
            if "epics_confirmed" in epics_status and "true" in epics_status.lower():
                ctx.session.state["epics_confirmed"] = True
                logger.info(f"[{self.name}] Epics confirmed, moving to architecture design")
            else:
                logger.info(f"[{self.name}] Epics need refinement")
                return
        
        # Stage 5: Architecture Design
        if (ctx.session.state.get("epics_confirmed") and 
            not ctx.session.state.get("architecture_confirmed", False)):
            logger.info(f"[{self.name}] Stage 5: Architecture Design")
            ctx.session.state["conversation_stage"] = "architecture_design"
            
            async for event in self.architecture_designer.run_async(ctx):
                yield event
            
            # Check if architecture is confirmed
            arch_status = ctx.session.state.get("architecture_status", "")
            if "architecture_confirmed" in arch_status and "true" in arch_status.lower():
                ctx.session.state["architecture_confirmed"] = True
                logger.info(f"[{self.name}] Architecture confirmed, moving to final validation")
            else:
                logger.info(f"[{self.name}] Architecture needs revision")
                return
        
        # Stage 6: Final Validation & Roadmap Generation
        if (ctx.session.state.get("architecture_confirmed") and 
            not ctx.session.state.get("context_gathering_complete", False)):
            logger.info(f"[{self.name}] Stage 6: Final Validation")
            ctx.session.state["conversation_stage"] = "final_validation"
            
            async for event in self.final_validator.run_async(ctx):
                yield event
            
            # Check if everything is confirmed
            final_status = ctx.session.state.get("final_status", "")
            if "context_gathering_complete" in final_status and "true" in final_status.lower():
                ctx.session.state["context_gathering_complete"] = True
                logger.info(f"[{self.name}] Context gathering complete!")
            else:
                logger.info(f"[{self.name}] Final validation incomplete")
                return
        
        logger.info(f"[{self.name}] Project context gathering workflow completed successfully.")


class ProjectRoadmapOrchestrator(SequentialAgent):
    """
    Main orchestrator that combines context gathering with roadmap generation.
    """
    
    def __init__(self, name: str = "ProjectRoadmapOrchestrator", **kwargs):
        context_agent = ProjectContextAgent()
        
        roadmap_generator = LlmAgent(
            name="RoadmapGenerator",
            model="gemini-2.0-flash-exp",
            instruction="""Generate a comprehensive project roadmap in JSON format based on the gathered context.
            
            Use the information from session state to create a structured roadmap with:
            - Project overview (vision, type, key requirements)
            - Epics with priorities and descriptions
            - Stories for each Epic with acceptance criteria
            - Estimated timeline and dependencies
            - System architecture reference
            
            Save the roadmap JSON to an artifact for the UI to display.
            
            Follow the JSON format specified in the agent comments.""",
            output_key="final_roadmap"
        )
        
        super().__init__(
            name=name,
            sub_agents=[context_agent, roadmap_generator],
            **kwargs
        )

# For ADK Web compatibility, the root agent must be named `root_agent`
root_agent = ProjectRoadmapOrchestrator()