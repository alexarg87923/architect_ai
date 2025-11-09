# Roadmap AI Backend

This is the backend for Roadmap AI, an intelligent project management assistant built with FastAPI. It uses AI agents to conduct discovery conversations with users, gather detailed project specifications, and generate comprehensive roadmaps with the ability to expand and edit nodes based on user input.

## Project Structure

```
agentic-backend/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI app with only agent router
│   ├── api/
│   │   └── routes/
│   │       └── agent.py           # All main API endpoints
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   └── exceptions.py
│   ├── models/
│   │   └── agent.py               # Canonical models only
│   └── services/
│       ├── agent_service.py       # Core agent logic
│       └── database_service.py    # Session/roadmap/message persistence
├── tests/
│   ├── test_agent.py
│   ├── test_api.py
│   ├── test_comprehensive_api.py  # Enhanced comprehensive test
│   ├── test_endpoints.py
│   └── test_live_api.py
└── requirements.txt
```

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd agentic-backend
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Copy the `.env.example` to `.env` and fill in the required values.

5. **Run the application:**
   ```bash
   uvicorn app.main:app --reload
   ```

## Features

- **AI-Powered Discovery**: Intelligent conversation flow to gather comprehensive project specifications
- **Multi-Phase Workflow**: Discovery → Confirmation → Roadmap Generation → Expansion/Editing
- **Roadmap Generation**: Creates detailed project roadmaps with nodes, subtasks, dependencies, and time estimates
- **Node Expansion**: Add new features or components to existing roadmaps
- **Node Editing**: Modify existing roadmap components and specifications
- **Session Persistence**: All conversations and roadmaps are saved with unique session IDs
- **Dual LLM Support**: Works with OpenAI GPT-4 and GROQ with intelligent fallback parsing
- **RESTful API**: Clean, documented API endpoints for frontend integration

## API Endpoints

All endpoints are under `/api/agent`:

- `POST /chat` - Main conversation endpoint for discovery and interactions
- `GET /roadmap/{session_id}` - Retrieve generated roadmap by session ID
- `POST /expand` - Request roadmap expansion with new features
- `POST /edit` - Edit existing roadmap nodes

## Usage Guidelines

- Access the API documentation at `http://127.0.0.1:8000/docs` after starting the server.
- Use the `/api/agent/chat` endpoint to start conversations and generate roadmaps.
- The agent will guide users through discovery, confirmation, and roadmap generation phases.
- Use expansion and editing endpoints to modify existing roadmaps.
- All data is persisted with session IDs for easy retrieval.

## Testing

Run the comprehensive test suite to verify all functionality:

```bash
# Run all tests
pytest

# Run the comprehensive API test with AI simulation
python tests/test_comprehensive_api.py

# Run specific test files
python tests/test_agent.py
python tests/test_api.py
```

The comprehensive test demonstrates:
- ✅ Realistic multi-round discovery conversations
- ✅ Roadmap generation with detailed specifications  
- ✅ Node expansion with new features
- ✅ Node editing and modifications
- ✅ Session persistence and retrieval
- ✅ LLM-powered user simulation for realistic testing