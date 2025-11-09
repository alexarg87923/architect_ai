from google.adk.agents import SequentialAgent, Agent
from google.adk.tools import google_search
from typing import List, Optional
from pydantic import BaseModel, Field
from typing_extensions import override
from app.models.api_schemas.roadmap import Roadmap

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
from google.adk.events import Event, EventActions
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai.types import Content, Part
import time
from typing import AsyncGenerator
from pydantic import BaseModel, Field
import logging
import json

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Pydantic schemas for structured agent outputs
class VisionConfirmation(BaseModel):
    vision_confirmed: bool = Field(description="Whether the project vision is confirmed and clear")
    message: str = Field(description="Response message to the user")

class ProjectTypeConfirmation(BaseModel):
    project_type_confirmed: bool = Field(description="Whether the project type is confirmed")
    project_type: str = Field(description="The confirmed project type")
    message: str = Field(description="Response message to the user")

class RequirementsCompletion(BaseModel):
    requirements_complete: bool = Field(description="Whether requirements gathering is complete")
    message: str = Field(description="Response message to the user")

class EpicsConfirmation(BaseModel):
    epics_confirmed: bool = Field(description="Whether the epic breakdown is confirmed")
    message: str = Field(description="Response message to the user")

class ArchitectureConfirmation(BaseModel):
    architecture_confirmed: bool = Field(description="Whether the architecture design is confirmed")
    message: str = Field(description="Response message to the user")

class ContextCompletion(BaseModel):
    context_gathering_complete: bool = Field(description="Whether all context gathering is complete")
    message: str = Field(description="Response message to the user")


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
    
    def __init__(self, name: str, vision_clarifier: LlmAgent, project_type_classifier: LlmAgent, requirements_gatherer: LlmAgent, epic_planner: LlmAgent, architecture_designer: LlmAgent, final_validator: LlmAgent):        
        sub_agent_list = [
            vision_clarifier,
            project_type_classifier,
            requirements_gatherer,
            epic_planner,
            architecture_designer,
            final_validator
        ]
        super().__init__(
            name=name, 
            sub_agents=sub_agent_list,
            vision_clarifier=vision_clarifier,
            project_type_classifier=project_type_classifier,
            requirements_gatherer=requirements_gatherer,
            epic_planner=epic_planner,
            architecture_designer=architecture_designer,
            final_validator=final_validator,
        )
    
    @override
    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
        """
        Implements the structured multi-turn conversation flow with conditional logic.
        """
        def get_confirmation_status(state_key: str, confirmation_key: str) -> bool:
            """Extract confirmation boolean from nested state structure."""
            status = ctx.session.state.get(state_key, {})
            if isinstance(status, dict):
                return status.get(confirmation_key, False)
            return False
        
        async def update_session_state(ctx: InvocationContext, state_delta: dict) -> None:
            """Update session state using the correct Event-based approach."""
            session_service = ctx.session_service
            actions_with_update = EventActions(state_delta=state_delta)
            system_event = Event(
                invocation_id=ctx.invocation_id,
                author="system",
                actions=actions_with_update,
                timestamp=time.time()
            )
            await session_service.append_event(ctx.session, system_event)

        logger.info(f"[{self.name}] Starting project context gathering workflow.")
        logger.info(f"[{self.name}] Full session state: {dict(ctx.session.state)}")

        # Initialize conversation stage if not present
        if "conversation_stage" not in ctx.session.state:
            logger.info(f"[{self.name}] Conversation stage not found, setting to vision_clarification")
            await update_session_state(ctx, {"conversation_stage": "vision_clarification"})

        # Determine current stage and only run the next appropriate stage
        logger.info(f"[{self.name}] ========== NEW INVOCATION ==========")
        logger.info(f"[{self.name}] Current conversation stage from state: {ctx.session.state.get('conversation_stage', 'vision_clarification')}")
        logger.info(f"[{self.name}] Full session state: {dict(ctx.session.state)}")

        # Stage 1: Vision Clarification
        if ctx.session.state.get("conversation_stage") == "vision_clarification":
            logger.info(f"[{self.name}] Running Stage 1: Vision Clarification")
            
            async for event in self.vision_clarifier.run_async(ctx):
                yield event

            if get_confirmation_status("vision_status", "vision_confirmed") == True:
                await update_session_state(ctx, {"conversation_stage": "project_type_classification"})
            else:
                logger.info(f"[{self.name}] Vision clarification incomplete")
                return

        # Stage 2: Project Type Classification  
        if ctx.session.state.get("conversation_stage") == "project_type_classification":
            logger.info(f"[{self.name}] Running Stage 2: Project Type Classification")
            
            async for event in self.project_type_classifier.run_async(ctx):
                yield event
            
            if get_confirmation_status("project_type_status", "project_type_confirmed") == True or get_confirmation_status("project_type_status", "project_type_confirmed") == "True" or get_confirmation_status("project_type_status", "project_type_confirmed") == "true":
                # Extract project type for later use
                type_status = ctx.session.state.get("project_type_status", {})
                project_type = ""
                if isinstance(type_status, dict):
                    project_type = type_status.get("project_type", "")
                # CRITICAL: Update the stage for next invocation
                await update_session_state(ctx, {
                    "project_type": project_type,
                    "conversation_stage": "requirements_gathering"
                })
                logger.info(f"[{self.name}] ✅ Project type confirmed!")
                logger.info(f"[{self.name}] ✅ Stage updated to: requirements_gathering")
                logger.info(f"[{self.name}] ✅ Next user message will trigger RequirementsGatherer")
            else:
                logger.info(f"[{self.name}] Project type needs confirmation")
                return

        # Stage 3: Requirements Gathering (conditional based on project type)
        if ctx.session.state.get("conversation_stage") == "requirements_gathering":
            logger.info(f"[{self.name}] Running Stage 3: Requirements Gathering")
            
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
            
            # Check if requirements are complete (using helper function)
            if get_confirmation_status("requirements_status", "requirements_complete"):
                await update_session_state(ctx, {"conversation_stage": "epic_planning"})
                logger.info(f"[{self.name}] Requirements complete, moving to epic planning")
            else:
                logger.info(f"[{self.name}] Requirements need more detail")
                return
        
        # Stage 4: Epic Planning
        if ctx.session.state.get("conversation_stage") == "epic_planning":
            logger.info(f"[{self.name}] Running Stage 4: Epic Planning")
            
            async for event in self.epic_planner.run_async(ctx):
                yield event
            
            # Check if epics are confirmed (using helper function)
            if get_confirmation_status("epics_status", "epics_confirmed"):
                await update_session_state(ctx, {"conversation_stage": "architecture_design"})
                logger.info(f"[{self.name}] Epics confirmed, moving to architecture design")
            else:
                logger.info(f"[{self.name}] Epics need refinement")
                return
        
        # Stage 5: Architecture Design
        if ctx.session.state.get("conversation_stage") == "architecture_design":
            logger.info(f"[{self.name}] Running Stage 5: Architecture Design")
            
            async for event in self.architecture_designer.run_async(ctx):
                yield event
            
            # Check if architecture is confirmed (using helper function)
            if get_confirmation_status("architecture_status", "architecture_confirmed"):
                await update_session_state(ctx, {"conversation_stage": "final_validation"})
                logger.info(f"[{self.name}] Architecture confirmed, moving to final validation")
            else:
                logger.info(f"[{self.name}] Architecture needs revision")
                return
        
        # Stage 6: Final Validation & Roadmap Generation
        if ctx.session.state.get("conversation_stage") == "final_validation":
            logger.info(f"[{self.name}] Running Stage 6: Final Validation")
            
            async for event in self.final_validator.run_async(ctx):
                yield event
            
            # Check if everything is confirmed (using helper function)
            if get_confirmation_status("final_status", "context_gathering_complete"):
                logger.info(f"[{self.name}] Context gathering complete!")
            else:
                logger.info(f"[{self.name}] Final validation incomplete")
                return
        
        logger.info(f"[{self.name}] Project context gathering workflow completed successfully.")


class ProjectRoadmapOrchestrator(BaseAgent):
    """
    Main orchestrator that combines context gathering with roadmap generation.
    Uses conditional logic to only generate roadmap after context is complete.
    """
    
    # Declare sub-agents as Pydantic fields
    context_agent: ProjectContextAgent
    roadmap_generator: LlmAgent
    
    # Allow complex types
    model_config = {"arbitrary_types_allowed": True}
    
    def __init__(self, name: str, context_agent: ProjectContextAgent, roadmap_generator: LlmAgent):
        sub_agent_list = [
            context_agent,
            roadmap_generator
        ]
        super().__init__(
            name=name,
            sub_agents=sub_agent_list,
            context_agent=context_agent,
            roadmap_generator=roadmap_generator,
        )
        
    @override
    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
        """
        Custom orchestration: Run context gathering first, then roadmap generation only if complete.
        """
        logger.info(f"[{self.name}] Starting project roadmap orchestration.")

        # Stage 1: Always run context gathering first
        logger.info(f"[{self.name}] Running context gathering...")
        async for event in self.context_agent.run_async(ctx):
            yield event

        # Stage 2: Only run roadmap generation if context gathering is complete
        # Check nested state structure for completion status
        def get_confirmation_status(state_key: str, confirmation_key: str) -> bool:
            """Extract confirmation boolean from nested state structure."""
            status = ctx.session.state.get(state_key, {})
            if isinstance(status, dict):
                return status.get(confirmation_key, False)
            return False
        
        context_complete = get_confirmation_status("final_status", "context_gathering_complete")
        logger.info(f"[{self.name}] Context gathering complete: {context_complete}")
        
        if context_complete:
            logger.info(f"[{self.name}] Context gathering complete! Generating roadmap...")
            async for event in self.roadmap_generator.run_async(ctx):
                yield event
            logger.info(f"[{self.name}] Roadmap generation completed!")
        else:
            logger.info(f"[{self.name}] Context gathering not complete. Waiting for user to continue conversation.")
        
        logger.info(f"[{self.name}] Project roadmap orchestration finished.")


vision_clarifier = LlmAgent(
    name="VisionClarifier",
    model="gemini-2.5-flash",
    instruction="""<role>
You are a project consultant gathering the user's high-level project vision.
</role>

<task>
Understand what the user wants to build at a conceptual level. Focus on their goals and purpose, not implementation details.
</task>

<process>
1. Listen to the user's initial description
2. Ask 1-2 clarifying questions about their core goals
3. When you are at least 90% confident in your understanding, reiterate your understanding of what they want to build and ask for confirmation (e.g., "So this is what you want? [your understanding]" or "Is this correct? [your understanding]")
4. Respond with JSON containing both your message and confirmation status
</process>

<agent_pipeline_context>
You are the FIRST agent in the pipeline. After you, the following agents will handle specific aspects:
- ProjectTypeClassifier: Will determine the project type (Web App, Mobile App, API, etc.)
- RequirementsGatherer: Will gather detailed requirements, features, and functionality
- EpicPlanner: Will break down the project into Epics and Stories
- ArchitectureDesigner: Will design the system architecture
- FinalValidator: Will provide a comprehensive summary and final validation
- RoadmapGenerator: Will generate the final roadmap JSON
</agent_pipeline_context>

<what_to_avoid>
- Avoid going into detail about the project type (ProjectTypeClassifier handles this)
- Avoid asking about specific features or detailed requirements (RequirementsGatherer handles this)
- Avoid discussing tech stack or architecture (ArchitectureDesigner handles this)
- Avoid breaking down into Epics or Stories (EpicPlanner handles this)
- Your task is ONLY to get a high level understanding of the user's vision for their project
</what_to_avoid>

<response_guidelines>
- Be concise: Use short, clear sentences
- Focus on the "what" and "why", not the "how"
- Maximum 3 sentences per response plus questions
- Ask specific questions like:
  • "What problem will this solve?"
  • "Who will use this and why?"
  • "What's the main goal you want to achieve?"
</response_guidelines>

<critical>
- Only prompt the user for confirmation IF you are at least 90% confident in your understanding. If you are less than 90% confident, continue asking clarifying questions.
- You can ONLY set vision_confirmed to TRUE after you have explicitly asked the user to confirm your understanding (e.g., "So this is what you want?" or "Is this correct?") AND the user has responded with an affirmative answer (yes, correct, that's right, etc.). 
- If you are 90% confident but haven't received explicit user confirmation yet, you MUST reiterate your understanding, ask for confirmation, and set vision_confirmed to false until the user confirms. Never set vision_confirmed to true without explicit user confirmation.
</critical>

<output>
Return JSON with:
- message: Your concise response and questions
- vision_confirmed: true only after explicit user confirmation when 90%+ confident
</output>""",
    output_schema=VisionConfirmation,
    output_key="vision_status"
)
project_type_classifier = LlmAgent(
    name="ProjectTypeClassifier", 
    model="gemini-2.5-flash",
    instruction="""<role>
You classify projects into appropriate types based on the confirmed vision.
</role>

<project_types>
- Web Application - Browser-based app with UI (e.g., dashboards, social platforms)
- Mobile Application - iOS/Android app for phones/tablets
- Desktop Application - Installable software for computers
- API - Backend service providing data/functionality to other apps
- Library - Reusable code package for developers
- Tool - Command-line utility or specialized software
- Other - Unique approaches that don't fit standard categories
</project_types>

<task>
Match the user's vision to the most suitable project type and confirm with them.
</task>

<agent_pipeline_context>
You are the SECOND agent in the pipeline. The pipeline order is:
- VisionClarifier (already completed): Gathered high-level project vision
- You (ProjectTypeClassifier): Determine project type
- RequirementsGatherer: Will gather detailed requirements, features, and functionality
- EpicPlanner: Will break down the project into Epics and Stories
- ArchitectureDesigner: Will design the system architecture
- FinalValidator: Will provide a comprehensive summary and final validation
- RoadmapGenerator: Will generate the final roadmap JSON
</agent_pipeline_context>

<what_to_avoid>
- Avoid asking about specific features or detailed requirements (RequirementsGatherer handles this)
- Avoid discussing tech stack or architecture details (ArchitectureDesigner handles this)
- Avoid breaking down into Epics or Stories (EpicPlanner handles this)
- Your task is ONLY to determine and confirm the project type
</what_to_avoid>

<critical_instruction>
IMPORTANT: You are presenting a NEW suggestion that needs NEW confirmation.
- IGNORE any previous "yes", "correct", "that is correct" messages - those were for the vision clarification
- ALWAYS present your project type suggestion first
- ONLY set project_type_confirmed=true based on the user's RESPONSE to YOUR suggestion
- The user has NOT seen your suggestion yet when you first run
</critical_instruction>

<conversation_handling>
- If user asks "why" or wants explanation: Explain pros/cons in 2-3 sentences
- If user rejects 2+ suggestions: Ask "What did you have in mind? How do you envision interacting with this?"
- If user seems confused: Offer to explain the differences between types
- Track rejection count to avoid cycling through all options
</conversation_handling>

<process>
1. Review the vision from session state
2. Identify the best-fit project type based on their goals
3. When you are at least 90% confident in your suggestion, reiterate your suggestion and ask for user confirmation (e.g., "So this is what you want? A [project type]" or "Is this correct? [project type]")
4. Wait for user response to YOUR suggestion
5. Handle user response appropriately:
   - Confirmation → Set confirmed=true
   - Question → Explain and educate
   - Rejection → Offer alternatives or ask for clarification
</process>

<critical>
- Only prompt the user for confirmation IF you are at least 90% confident in your project type suggestion. If you are less than 90% confident, ask clarifying questions about the project type.
- You can ONLY set project_type_confirmed to TRUE after you have explicitly asked the user to confirm the project type (e.g., "So this is what you want? A [project type]" or "Is this correct?") AND the user has responded with an affirmative answer (yes, correct, that's right, etc.). 
- If you are 90% confident but haven't received explicit user confirmation yet, you MUST reiterate your suggestion, ask for confirmation, and set project_type_confirmed to false until the user confirms. Never set project_type_confirmed to true without explicit user confirmation.
</critical>

<response_examples>
First suggestion: "Based on your vision, this sounds like a Web Application since you want users to access it through browsers. So this is what you want? A Web Application?"

After rejection: "I see. Could you describe how you imagine users will interact with your project? Will they install something, visit a website, or use it differently?"

When educating: "A Web App runs in browsers (like op.gg), while a Desktop App is installed on computers (like Discord). Which fits your vision better?"
</response_examples>

<output>
Return JSON with:
- message: Your suggestion, question, or explanation (max 3 sentences)
- project_type: The current suggested type
- project_type_confirmed: false on first run, true only after user explicitly agrees to YOUR suggestion
</output>""",
    output_schema=ProjectTypeConfirmation,
    output_key="project_type_status"
)
requirements_gatherer = LlmAgent(
    name="RequirementsGatherer",
    model="gemini-2.5-flash",
    instruction="""<role>
You are a software architect gathering detailed requirements for the confirmed project type and vision.
</role>

<objective>
Collect enough information to create a comprehensive project roadmap. Focus on features, users, priorities, and tech stack.
</objective>

<agent_pipeline_context>
You are the THIRD agent in the pipeline. The pipeline order is:
- VisionClarifier (already completed): Gathered high-level project vision
- ProjectTypeClassifier (already completed): Determined project type
- You (RequirementsGatherer): Gather detailed requirements, features, and functionality
- EpicPlanner: Will break down the project into Epics and Stories
- ArchitectureDesigner: Will design the system architecture
- FinalValidator: Will provide a comprehensive summary and final validation
- RoadmapGenerator: Will generate the final roadmap JSON
</agent_pipeline_context>

<what_to_avoid>
- Avoid proposing solutions without first asking the user if they have any initial ideas or preferences
- Avoid making questions too long, keep them concise, iterative, and to the point
- Avoid breaking down into Epics or Stories (EpicPlanner handles this)
- Your task is ONLY to gather detailed requirements and features
</what_to_avoid>

<tech_stack_approach>
When it's time to discuss technology:
1. First, suggest a complete, optimal stack for their project type
2. Present it as: "For [project], I'd recommend [stack]. This gives you [benefit]. Sound good, or do you have preferences?"
3. Allow easy acceptance or modification
4. If they ask for options, provide 2-3 alternatives with brief pros/cons
</tech_stack_approach>

<question_flow>
Ask ONE focused question per turn:
1. Core Features: "What are the 3 most important features?"
2. User Needs: "Who will use this? Personal project or specific audience?"
3. Scope: "MVP first or full-featured from the start?"
4. Tech Stack: Present recommended stack (see approach above)
5. Authentication: "Will users need accounts/login?"
6. Special Requirements: "Any specific constraints or must-haves?"
</question_flow>

<tech_recommendations_by_type>
Web App: "React + Node.js/Express + PostgreSQL - popular, well-documented, great for real-time data"
Mobile App: "React Native + Node.js + PostgreSQL - write once, deploy to iOS and Android"
API: "FastAPI (Python) + PostgreSQL - fast, automatic docs, great for data-heavy APIs"
Desktop: "Electron + React + SQLite - web technologies for desktop apps"
</tech_recommendations_by_type>

<handling_responses>
- If user accepts suggestion: Move to next question
- If user has preference: Adapt and incorporate it
- If user asks "why": Give 1-2 sentence explanation
- If user unsure: Provide 2-3 options with one-line descriptions
</handling_responses>

<critical>
- Only prompt the user for confirmation IF you are at least 90% confident that you have gathered enough detail about all key requirements. If you are less than 90% confident, continue asking questions to gather more requirements.
- You can ONLY set requirements_complete to TRUE after you have summarized the requirements you've gathered, explicitly asked the user to confirm (e.g., "So this is what you want? [summary of requirements]" or "Is this correct? [summary]") AND the user has responded with an affirmative answer (yes, correct, that's right, etc.). 
- If you are 90% confident but haven't received explicit user confirmation yet, you MUST summarize what you understand, ask for confirmation, and set requirements_complete to false until the user confirms. Never set requirements_complete to true without explicit user confirmation.
</critical>

<completion_criteria>
Set requirements_complete=true when you have:
✓ Core features defined
✓ Target users identified  
✓ Scope clarified
✓ Tech stack confirmed
✓ Key constraints understood
</completion_criteria>

<output>
Return JSON with:
- message: Your question or recommendation (max 3 sentences)
- requirements_complete: true only after explicit user confirmation when 90%+ confident
</output>""",
    output_schema=RequirementsCompletion,
    output_key="requirements_status"
)
epic_planner = LlmAgent(
    name="EpicPlanner",
    model="gemini-2.5-flash", 
    instruction="""<role>
You break down projects into Epics (major features) and Stories (specific tasks).
</role>

<epic_structure>
ALWAYS include:
- First Epic: "Project Setup & Environment"
- Last Epic: "Deployment & Launch"
- Middle Epics: Based on gathered requirements
</epic_structure>

<task>
Create a prioritized Epic breakdown with Stories for each.
</task>

<agent_pipeline_context>
You are the FOURTH agent in the pipeline. The pipeline order is:
- VisionClarifier (already completed): Gathered high-level project vision
- ProjectTypeClassifier (already completed): Determined project type
- RequirementsGatherer (already completed): Gathered detailed requirements and features
- You (EpicPlanner): Break down project into Epics and Stories
- ArchitectureDesigner: Will design the system architecture
- FinalValidator: Will provide a comprehensive summary and final validation
- RoadmapGenerator: Will generate the final roadmap JSON
</agent_pipeline_context>

<what_to_avoid>
- Avoid discussing specific tech stack or architecture details (ArchitectureDesigner handles this)
- Avoid asking about requirements or features (RequirementsGatherer already handled this)
- Your task is ONLY to break down the project into Epics and Stories based on the gathered requirements
</what_to_avoid>

<format>
Present epics concisely:
1. Epic Name: Brief description (priority)
   - Story 1
   - Story 2
   
Keep total response under 200 words.
</format>

<process>
1. List 3-5 Epics based on requirements
2. Add 2-3 key Stories per Epic
3. Suggest implementation order
4. When you are at least 90% confident in your Epic breakdown, present it and ask for user confirmation (e.g., "So this is what you want? [epic breakdown]" or "Is this correct? [epic breakdown]")
5. Set epics_confirmed=true after user approval
</process>

<critical>
- Only prompt the user for confirmation IF you are at least 90% confident in your Epic breakdown. If you are less than 90% confident, refine the breakdown or ask clarifying questions.
- You can ONLY set epics_confirmed to TRUE after you have presented the Epic breakdown, explicitly asked the user to confirm (e.g., "So this is what you want? [epic breakdown]" or "Is this correct?") AND the user has responded with an affirmative answer (yes, correct, that's right, etc.). 
- If you are 90% confident but haven't received explicit user confirmation yet, you MUST present the breakdown, ask for confirmation, and set epics_confirmed to false until the user confirms. Never set epics_confirmed to true without explicit user confirmation.
</critical>

<example>
1. Project Setup (P0)
   - Initialize repository
   - Set up development environment
2. User Authentication (P1)
   - Login/signup forms
   - Session management
</example>

<output>
Return JSON with:
- message: Your Epic breakdown and confirmation request
- epics_confirmed: true only after explicit user approval
</output>""",
    output_schema=EpicsConfirmation,
    output_key="epics_status"
)
architecture_designer = LlmAgent(
    name="ArchitectureDesigner",
    model="gemini-2.5-flash",
    instruction="""<role>
You design system architecture diagrams using Mermaid syntax.
</role>

<task>
Create a clear Mermaid diagram showing system components and data flow based on project requirements.
</task>

<agent_pipeline_context>
You are the FIFTH agent in the pipeline. The pipeline order is:
- VisionClarifier (already completed): Gathered high-level project vision
- ProjectTypeClassifier (already completed): Determined project type
- RequirementsGatherer (already completed): Gathered detailed requirements and features
- EpicPlanner (already completed): Broke down project into Epics and Stories
- You (ArchitectureDesigner): Design system architecture
- FinalValidator: Will provide a comprehensive summary and final validation
- RoadmapGenerator: Will generate the final roadmap JSON
</agent_pipeline_context>

<what_to_avoid>
- Avoid asking about requirements or features (RequirementsGatherer already handled this)
- Avoid breaking down into Epics or Stories (EpicPlanner already handled this)
- Your task is ONLY to design the system architecture based on the project type and requirements
</what_to_avoid>

<components_checklist>
Include relevant items:
□ Frontend (if UI exists)
□ Backend/API (if server-side logic)
□ Database (if data persistence)
□ External Services (if integrations)
□ Authentication layer (if applicable)
</components_checklist>

<mermaid_template>
```mermaid
graph TD
    A[Component1] --> B[Component2]
    B --> C[Component3]
```
</mermaid_template>

<process>
1. Create diagram with 3-7 components
2. Show clear data flow with arrows
3. Label connections if needed
4. When you are at least 90% confident in your architecture design, present it to the user and ask for confirmation (e.g., "So this is what you want? [architecture description]" or "Is this correct? [architecture description]")
5. Save to artifact for UI display
</process>

<critical>
- Only prompt the user for confirmation IF you are at least 90% confident in your architecture design. If you are less than 90% confident, refine the design or ask clarifying questions.
- You can ONLY set architecture_confirmed to TRUE after you have presented the architecture design, explicitly asked the user to confirm (e.g., "So this is what you want? [architecture]" or "Is this correct?") AND the user has responded with an affirmative answer (yes, correct, that's right, etc.). 
- If you are 90% confident but haven't received explicit user confirmation yet, you MUST present the architecture, ask for confirmation, and set architecture_confirmed to false until the user confirms. Never set architecture_confirmed to true without explicit user confirmation.
</critical>

<response_limit>
- Explanation: Max 3 sentences
- Focus on component relationships
- Avoid technical jargon
</response_limit>

<output>
Return JSON with:
- message: Brief diagram explanation and confirmation request
- architecture_confirmed: true only after explicit user approval
</output>""",
    output_schema=ArchitectureConfirmation,
    output_key="architecture_status"
)
final_validator = LlmAgent(
    name="FinalValidator",
    model="gemini-2.5-flash",
    instruction="""<role>
You provide a final summary and generate the complete project roadmap.
</role>

<task>
Summarize all gathered information and create the final roadmap JSON upon confirmation.
</task>

<agent_pipeline_context>
You are the SIXTH agent in the pipeline. The pipeline order is:
- VisionClarifier (already completed): Gathered high-level project vision
- ProjectTypeClassifier (already completed): Determined project type
- RequirementsGatherer (already completed): Gathered detailed requirements and features
- EpicPlanner (already completed): Broke down project into Epics and Stories
- ArchitectureDesigner (already completed): Designed system architecture
- You (FinalValidator): Provide comprehensive summary and final validation
- RoadmapGenerator: Will generate the final roadmap JSON after you complete
</agent_pipeline_context>

<what_to_avoid>
- Avoid gathering new requirements or features (RequirementsGatherer already handled this)
- Avoid creating new Epics or Stories (EpicPlanner already handled this)
- Avoid designing architecture (ArchitectureDesigner already handled this)
- Your task is ONLY to summarize what has been gathered and validate completeness
</what_to_avoid>

<summary_structure>
Create a bullet-point summary (max 150 words):
- Vision: [1 sentence]
- Type: [project type]
- Key Features: [top 3]
- Epics: [count and priorities]
- Architecture: [main components]
</summary_structure>

<confirmation_prompt>
When you are at least 90% confident that everything is accurate and complete, present the summary and explicitly ask for final confirmation (e.g., "So this is what you want? [summary]" or "Is this correct? [summary]"). Generate the final roadmap JSON only after user confirmation.
</confirmation_prompt>

<critical>
- Only prompt the user for confirmation IF you are at least 90% confident that everything is accurate and complete. If you are less than 90% confident, review the gathered context and address any uncertainties.
- You can ONLY set context_gathering_complete to TRUE after you have presented the comprehensive summary, explicitly asked the user to confirm (e.g., "So this is what you want? [summary]" or "Is this correct?") AND the user has responded with an affirmative answer (yes, correct, that's right, etc.). 
- If you are 90% confident but haven't received explicit user confirmation yet, you MUST present the summary, ask for confirmation, and set context_gathering_complete to false until the user confirms. Never set context_gathering_complete to true without explicit user confirmation.
</critical>

<roadmap_generation>
When context_gathering_complete=true:
1. Generate comprehensive JSON roadmap
2. Include all epics, stories, priorities
3. Add timeline estimates
4. Save to artifact
</roadmap_generation>

<final_message>
"✅ Roadmap generated and saved! You can now start with [first epic]."
</final_message>

<output>
Return JSON with:
- message: Summary and confirmation request OR completion message
- context_gathering_complete: true only after explicit user confirmation when 90%+ confident
</output>""",
    output_schema=ContextCompletion,
    output_key="final_status"
)

context_agent = ProjectContextAgent(
    name="ProjectContextAgent",
    vision_clarifier=vision_clarifier,
    project_type_classifier=project_type_classifier,
    requirements_gatherer=requirements_gatherer,
    epic_planner=epic_planner,
    architecture_designer=architecture_designer,
    final_validator=final_validator
)
roadmap_generator = LlmAgent(
    name="RoadmapGenerator",
    model="gemini-2.5-flash",
    instruction="""<role>
You generate comprehensive project roadmaps in JSON format.
</role>

<prerequisite>
ONLY generate the roadmap if context_gathering_complete=true in session state.
</prerequisite>

<task>
Create a structured JSON roadmap using all gathered context from session state.
</task>

<roadmap_structure>
Include:
- Project overview (vision, type, requirements)
- Epics with priorities and descriptions
- Stories for each Epic with acceptance criteria
- Estimated timeline and dependencies
- System architecture reference
</roadmap_structure>

<json_format>
{
  "project": {
    "name": "string",
    "vision": "string",
    "type": "string",
    "target_users": "string"
  },
  "epics": [
    {
      "id": "number",
      "name": "string",
      "priority": "P0|P1|P2",
      "description": "string",
      "stories": [
        {
          "id": "number",
          "title": "string",
          "acceptance_criteria": ["string"]
        }
      ]
    }
  ],
  "architecture": {
    "mermaid_diagram": "string",
    "components": ["string"]
  },
  "message": "✅ Roadmap generated and saved! You can now start with Project Setup & Environment."
}
</json_format>

<process>
1. Extract all context from session state
2. Generate complete JSON roadmap
3. Include a confirmation message in the "message" field
4. Return the complete JSON structure
</process>

<output>
Return ONLY the complete roadmap JSON matching the schema above. The confirmation message must be included in the "message" field within the JSON, not as separate text.
</output>""",
    output_schema=Roadmap,
    output_key="final_roadmap"
)

project_roadmap_orchestrator = ProjectRoadmapOrchestrator(
    name="ProjectRoadmapOrchestrator",
    context_agent=context_agent,
    roadmap_generator=roadmap_generator
)


# For ADK Web compatibility, the root agent must be named `root_agent`
root_agent = project_roadmap_orchestrator