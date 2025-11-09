# Agentic Backend Test Documentation

This directory contains comprehensive tests for the FastAPI-based agentic project management backend. The tests are organized into different categories to validate various aspects of the system.

## Test Structure Overview

```
tests/
├── __init__.py                    # Package initialization
├── test_api.py                    # Component import and initialization tests
├── test_live_api.py              # Live server API endpoint tests
├── test_comprehensive_api.py     # End-to-end workflow tests
├── test_endpoints.py             # Basic endpoint validation tests
├── test_agent.py                 # Legacy agent route tests (deprecated)
├── test_chat.py                  # Legacy chat route tests (deprecated)
├── test_roadmap.py               # Legacy roadmap route tests (deprecated)
└── test_docs.md                  # This documentation file
```

## Active Test Files

### 1. test_api.py - Component Import and Initialization Tests

**Purpose**: Validates that all backend components can be imported and initialized correctly without runtime errors.

**Design**: 
- Tests core imports (AgentService, models, routes, config)
- Validates AgentService initialization with proper API client setup
- Tests ConversationState creation and message handling

**How to Run**:
```bash
cd agentic-backend
python tests/test_api.py
```

**Expected Output**:
```
🧪 Testing Agentic Backend Components

Testing imports...
✅ AgentService import successful
✅ Agent models import successful
✅ Agent routes import successful
✅ Config import successful - Using Agentic Project Management

Testing AgentService initialization...
✅ AgentService initialized successfully
   Client mode: groq  # or openai
   Model: llama3-8b-8192  # or gpt-3.5-turbo
   Max tokens: 1000

Testing ConversationState...
✅ ConversationState created successfully
   Session ID: test-session
   Phase: discovery
   Messages: 1

==================================================
🎉 All tests passed! The backend is ready for testing.
==================================================
```

**Key Features Tested**:
- Import validation for all core modules
- AgentService client mode detection (GROQ vs OpenAI)
- Model configuration validation
- ConversationState and ChatMessage creation

---

### 2. test_live_api.py - Live Server API Endpoint Tests

**Purpose**: Tests the actual running FastAPI server endpoints with real HTTP requests.

**Design**:
- Requires server to be running (`uvicorn app.main:app --reload`)
- Tests health endpoints, chat functionality, and session management
- Validates multi-turn conversation flow

**How to Run**:
```bash
# Terminal 1: Start the server
cd agentic-backend
uvicorn app.main:app --reload

# Terminal 2: Run the tests
python tests/test_live_api.py
```

**Expected Output**:
```
🧪 Live API Testing - Agentic Backend
==================================================
🔍 Testing server health...
✅ Main server health check passed
   Response: {'status': 'healthy', 'message': 'Agentic Backend is running'}
✅ Agent service health check passed
   Client mode: groq
   Model: llama3-8b-8192

🤖 Testing chat endpoint...
✅ Chat endpoint working successfully
   Session ID: abc123-def456-ghi789
   Agent response: Hello! I'd be happy to help you build a task management web application...
   Phase: discovery
   Action button: Continue Discovery

📋 Testing conversation retrieval for session: abc123-def456-ghi789
✅ Conversation retrieval working
   Phase: discovery
   Specifications complete: False
   Messages count: 2

🔄 Testing multi-turn conversation...
   Turn 1: I want to build a task management web app
   ✅ Response: Great! I'd love to help you build a task management web application...
   Phase: discovery

   Turn 2: It should be for small teams of 5-10 people
   ✅ Response: Perfect! A task management app for small teams...
   Phase: discovery
   
   [... continues for all turns ...]

✅ Multi-turn conversation test completed successfully

==================================================
🎉 API testing completed!

📝 Next steps:
   1. Test the edit and expand action types
   2. Implement database persistence
   3. Connect with the React frontend
==================================================
```

**Key Features Tested**:
- Server health and availability
- Agent service configuration
- Chat endpoint functionality
- Session management
- Conversation state persistence
- Multi-turn conversation flow

---

### 3. test_comprehensive_api.py - End-to-End Workflow Tests

**Purpose**: Tests the complete workflow from project discovery through roadmap generation, expansion, and editing.

**Design**:
- Comprehensive discovery phase with multiple user inputs
- Roadmap generation testing
- Roadmap expansion functionality
- Roadmap editing capabilities
- Full agent workflow validation

**How to Run**:
```bash
# Terminal 1: Start the server
cd agentic-backend
uvicorn app.main:app --reload

# Terminal 2: Run the comprehensive tests
python tests/test_comprehensive_api.py
```

**Expected Output**:
```
🎯 Testing Complete Roadmap Generation Flow
==================================================

📝 Discovery Step 1: I want to build a task management web application...
   ✅ Response: Excellent! A task management web application...
   Phase: discovery
   
📝 Discovery Step 2: Let's call it TaskFlow Pro...
   ✅ Response: Great name! TaskFlow Pro sounds professional...
   Phase: discovery

[... continues through all discovery steps ...]

🎯 Generating Roadmap...
✅ Roadmap generated successfully!
   Initial nodes: 8
   Current phase: roadmap_ready
   🔘 Action: Generate Roadmap

🔧 Testing Roadmap Expansion
==============================
✅ Expand mode activated successfully
   Agent response: I'd be happy to help you add a mobile app version...

✅ Roadmap expanded successfully!
   New node count: 10
   Response: Perfect! I've added a React Native mobile app branch...

✏️ Testing Roadmap Editing
==============================
✅ Edit mode activated successfully
   Agent response: I can help you edit the user authentication system...

✅ Roadmap edited successfully!
   Updated nodes: 10
   Response: Great! I've updated the authentication system...

==================================================
🎉 Comprehensive testing completed successfully!

📊 Final Results:
   ✅ Discovery phase: 10 steps completed
   ✅ Roadmap generation: 8 initial nodes
   ✅ Roadmap expansion: +2 nodes added
   ✅ Roadmap editing: 1 node updated
   ✅ All agent tools tested successfully

🚀 The backend is fully functional and ready for production!
==================================================
```

**Key Features Tested**:
- Complete discovery workflow (10+ conversation turns)
- Roadmap generation with proper node structure
- Roadmap expansion with new features/branches
- Roadmap editing and content updates
- Action button functionality
- Phase transitions (discovery → roadmap_ready → edit/expand)
- Agent tool selection and execution

---

### 4. test_endpoints.py - Basic Endpoint Validation Tests

**Purpose**: Simple endpoint validation to ensure all routes are accessible and return expected status codes.

**Design**:
- Basic GET/POST requests to all endpoints
- Status code validation
- JSON response structure validation

**How to Run**:
```bash
# Terminal 1: Start the server
cd agentic-backend
uvicorn app.main:app --reload

# Terminal 2: Run the endpoint tests
python tests/test_endpoints.py
```

**Expected Output**:
```
🚀 Testing Agentic Backend API Endpoints
==================================================

1️⃣ Testing Health Endpoints
📡 GET /
   Status: 200
   ✅ Success

📡 GET /health
   Status: 200
   ✅ Success

2️⃣ Testing Agent Endpoints
📡 GET /api/agent/health
   Status: 200
   ✅ Success

📡 POST /api/agent/chat
   Status: 200
   ✅ Success

[... continues for all endpoints ...]
```

**Key Features Tested**:
- All endpoint accessibility
- Proper HTTP status codes
- Basic response structure

---

## Legacy Test Files (Deprecated)

The following test files were created for the original API structure but are now deprecated due to the unified agent endpoint design:

### test_agent.py
- **Status**: Deprecated
- **Reason**: Tests old `/api/agent/specifications`, `/api/agent/generate_roadmap` endpoints that have been replaced by the unified `/api/agent/chat` endpoint

### test_chat.py  
- **Status**: Deprecated
- **Reason**: Tests old chat routes that have been consolidated into the main agent service

### test_roadmap.py
- **Status**: Deprecated
- **Reason**: Tests old roadmap-specific routes that are now handled through the agent chat interface

## Test Environment Setup

### Prerequisites
1. **Python Environment**: Ensure you have the correct Python environment activated
2. **Dependencies**: Install requirements via `pip install -r requirements.txt`
3. **Environment Variables**: Set up `.env` file with API keys:
   ```
   GROQ_KEY=your_groq_api_key
   OPENAI_API_KEY=your_openai_api_key
   ```

### Running All Tests

To run the complete test suite:

```bash
# 1. Start the FastAPI server
uvicorn app.main:app --reload

# 2. In a new terminal, run all tests in sequence
cd agentic-backend/tests

# Component tests (no server needed)
python test_api.py

# Live API tests (server required)
python test_live_api.py
python test_comprehensive_api.py
python test_endpoints.py
```

## Test Design Principles

### 1. **Layered Testing Approach**
- **Unit Level**: Component imports and initialization (`test_api.py`)
- **Integration Level**: Live API endpoints (`test_live_api.py`, `test_endpoints.py`)
- **System Level**: End-to-end workflows (`test_comprehensive_api.py`)

### 2. **Real-World Simulation**
- Tests use realistic conversation flows
- Multi-turn conversations simulate actual user interactions
- Comprehensive project scenarios (task management app)

### 3. **Error Handling Validation**
- Network connection failures
- Server availability checks
- API response validation
- Timeout handling for LLM calls

### 4. **State Management Testing**
- Session persistence across requests
- Conversation state continuity
- Roadmap state updates and persistence

## Expected Test Results Summary

When all tests pass successfully, you should see:

✅ **Component Tests**: All imports work, AgentService initializes with correct client mode
✅ **Live API Tests**: Server responds to health checks, chat endpoints work, sessions persist
✅ **Comprehensive Tests**: Full discovery→roadmap→edit/expand workflow functions correctly
✅ **Endpoint Tests**: All routes accessible with proper status codes

## Troubleshooting Common Issues

### Server Connection Errors
```
❌ Server not running or not accessible
   Please start the server with: uvicorn app.main:app --reload
```
**Solution**: Start the FastAPI server before running live tests

### API Key Issues
```
❌ AgentService initialization failed: No API key provided
```
**Solution**: Check your `.env` file has either `GROQ_KEY` or `OPENAI_API_KEY` set

### Import Errors
```
❌ AgentService import failed: No module named 'app'
```
**Solution**: Ensure you're running tests from the correct directory and Python path is set up properly

### Timeout Errors
```
❌ Chat test failed: Request timeout
```
**Solution**: LLM API calls can be slow; ensure stable internet connection and consider increasing timeout values

## Integration with CI/CD

These tests are designed to be easily integrated into continuous integration pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run Component Tests
  run: python tests/test_api.py
  
- name: Start Server
  run: uvicorn app.main:app --host 0.0.0.0 --port 8000 &
  
- name: Wait for Server
  run: sleep 10
  
- name: Run Live API Tests  
  run: python tests/test_live_api.py
```

## Next Steps

1. **Database Persistence**: Implement actual database storage for conversations and roadmaps
2. **Authentication Tests**: Add tests for user authentication and authorization
3. **Performance Tests**: Add load testing for concurrent users and large roadmaps
4. **Frontend Integration**: Create tests for React frontend API integration
5. **Production Deployment**: Add tests for deployment configurations and health monitoring
