"""
User-specific prompts for the simulation system
Centralizes user persona prompts for different project types
"""

# User Persona Templates
USER_PERSONA_TEMPLATE = """You are a computer science student who wants to build "{project_name}" - {project_description}

Project Vision:
{project_vision}

Key Features for MVP:
{mvp_features}

You're experienced with {tech_experience} but want to build something impactful quickly using proven patterns and existing APIs/libraries rather than reinventing everything.

{conversation_history}

The AI agent just asked: "{agent_question}"

Response Round: {response_count}/15

IMPORTANT: 
- Answer the specific question asked by the agent
- Don't repeat information already provided unless asked
- Be concise and strategic
- Focus on efficient implementation and leveraging existing tools
- Keep responses under 100 words

Provide a direct answer to the agent's question:"""

# Project Definitions
PROJECT_DEFINITIONS = {
    "codementor": {
        "name": "CodeMentor",
        "description": "an AI-powered coding assistant and learning platform to help students learn programming more effectively",
        "vision": """- React frontend with code editor integration (Monaco Editor) 
- FastAPI backend with OpenAI integration for code explanations and help
- User accounts to track progress and save code examples
- Real-time code analysis and suggestions
- Learning paths for different programming languages
- Code challenges with AI-generated hints and explanations
- Community features for sharing and discussing code""",
        "mvp_features": """- Interactive code editor with syntax highlighting
- AI-powered code explanation and error analysis
- User authentication and progress tracking  
- Basic learning modules for Python/JavaScript
- Code challenge system with difficulty levels""",
        "tech_experience": "React and Python"
    },
    "taskflow": {
        "name": "TaskFlow",
        "description": "a collaborative project management tool for remote teams with real-time updates and AI-powered task prioritization",
        "vision": """- React frontend with real-time collaboration features
- Node.js backend with WebSocket support for live updates
- Kanban board with drag-and-drop functionality
- AI-powered task prioritization and time estimation
- Team chat and file sharing integration
- Mobile-responsive design for on-the-go management
- Integration with popular tools like Slack and GitHub""",
        "mvp_features": """- Kanban board with drag-and-drop
- Real-time collaboration with WebSockets
- User authentication and team management
- Basic AI task prioritization
- Mobile-responsive design""",
        "tech_experience": "React and Node.js"
    },
    "healthtracker": {
        "name": "HealthTracker",
        "description": "a comprehensive health and fitness tracking app with AI-powered insights and personalized recommendations",
        "vision": """- React Native mobile app for cross-platform support
- Python backend with machine learning for health insights
- Integration with wearable devices and health APIs
- Personalized workout and nutrition recommendations
- Progress tracking with visual analytics
- Social features for motivation and accountability
- AI-powered goal setting and achievement tracking""",
        "mvp_features": """- Basic health metrics tracking
- Workout logging and progress visualization
- User authentication and profile management
- Simple AI recommendations
- Mobile-responsive web version""",
        "tech_experience": "React Native and Python"
    },
    "gatheryou": {
        "name": "GatherYou",
        "description": "a university club and event mobile application for connecting students with campus activities and social events",
        "vision": """- React Native mobile app for iOS and Android
- Node.js backend with real-time notifications
- Integration with university calendar systems
- Event discovery and recommendation engine
- Social features for event sharing and RSVPs
- Club management tools for organizers
- Location-based event filtering and maps integration
- Push notifications for event reminders and updates""",
        "mvp_features": """- Event browsing and search functionality
- User authentication and profile creation
- Event RSVP and attendance tracking
- Club/organization pages and event creation
- Push notifications for event updates
- Basic location-based event filtering""",
        "tech_experience": "React Native and Node.js"
    }
}

def get_user_persona_prompt(project_type: str = "codementor", conversation_history: str = "", agent_question: str = "", response_count: int = 1) -> str:
    """Get the user persona prompt for a specific project type"""
    project = PROJECT_DEFINITIONS.get(project_type, PROJECT_DEFINITIONS["codementor"])
    
    return USER_PERSONA_TEMPLATE.format(
        project_name=project["name"],
        project_description=project["description"],
        project_vision=project["vision"],
        mvp_features=project["mvp_features"],
        tech_experience=project["tech_experience"],
        conversation_history=conversation_history,
        agent_question=agent_question,
        response_count=response_count
    )

def format_conversation_history(history: list) -> str:
    """Format conversation history for inclusion in prompts"""
    if not history:
        return ""
    
    history_text = "\n".join([
        f"Agent: {msg.get('agent', '')}" for msg in history[-3:]  # Last 3 exchanges
    ])
    
    return f"\n\nPrevious conversation:\n{history_text}"

def get_available_project_types() -> list:
    """Get list of available project types for simulation"""
    return list(PROJECT_DEFINITIONS.keys())
