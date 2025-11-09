# Roadmap AI Backend

This is the backend for Roadmap AI, an intelligent project management assistant built with FastAPI. It uses AI agents to conduct discovery conversations with users, gather detailed project specifications, and generate comprehensive roadmaps with the ability to expand and edit nodes based on user input.


## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── core/                      # Core configuration and infrastructure
│   │   ├── config.py
│   │   └── database.py
│   ├── models/                    # Data models and schemas
│   │   ├── database/              # SQLAlchemy models (database layer)
│   │   │   ├── base.py
│   │   │   ├── user.py
│   │   │   ├── project.py
│   │   │   ├── task.py
│   │   │   ├── conversation.py
│   │   │   ├── message.py
│   │   │   ├── roadmap.py
│   │   │   └── feedback.py
│   │   └── api_schemas/           # Pydantic models (API layer)
│   │       ├── user.py
│   │       ├── project.py
│   │       ├── task.py
│   │       ├── conversation.py
│   │       ├── roadmap.py
│   │       └── feedback.py
│   ├── api/                       # API layer
│   │   ├── dependencies.py
│   │   └── routes/                # API endpoints
│   │       ├── auth.py
│   │       ├── projects.py
│   │       ├── tasks.py
│   │       ├── agent.py
│   │       ├── feedback.py
│   │       ├── admin.py
│   └── services/                  # Business logic layer
│       ├── __init__.py
│       ├── user_service.py
│       ├── project_service.py
│       ├── task_service.py
│       ├── feedback_service.py
│       ├── database_service.py
│       ├── agent_service/         # AI agent services
│       │   ├── orchestrator.py
│       │   ├── roadmap_generation.py
│       │   └── tools.py
├── tests/                         # Test suite
│   ├── test_agent.py
│   ├── test_api.py
│   ├── test_comprehensive_api.py
│   ├── test_endpoints.py
│   └── test_live_api.py
├── scripts/                       # Utility scripts
│   └── seed_database.py
└── requirements.txt
```


## Usage Guidelines

- Access the API documentation at `http://127.0.0.1:8000/docs` after starting the server.
- Use the `/api/agent/chat` endpoint to start conversations and generate roadmaps.
- The agent will guide users through discovery, confirmation, and roadmap generation phases.
- Use expansion and editing endpoints to modify existing roadmaps.
- All data is persisted with session IDs for easy retrieval.


## Development

### **Database Seeding**
```bash
# Seed the database with sample data
python scripts/seed_database.py
```

### **Environment Variables**
Create a `.env` file with:
```env
# LLM Configuration
OPENAI_API_KEY=your_openai_key
GROQ_API_KEY=your_groq_key

# Database
DATABASE_URL=sqlite:///./roadmap.db

# Security
SECRET_KEY=your_secret_key
```