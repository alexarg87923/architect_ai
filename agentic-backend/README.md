# Agentic Application

This project is an agentic application built with FastAPI that interacts with users to gather project specifications, generate roadmaps in JSON format, and includes functionalities to expand and edit roadmap nodes based on user input.

## Project Structure

```
agentic-backend
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── api
│   │   ├── __init__.py
│   │   ├── routes
│   │   │   ├── __init__.py
│   │   │   ├── agent.py
│   │   │   ├── roadmap.py
│   │   │   └── chat.py
│   │   └── dependencies.py
│   ├── core
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── exceptions.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── roadmap.py
│   │   ├── chat.py
│   │   └── agent.py
│   ├── services
│   │   ├── __init__.py
│   │   ├── agent_service.py
│   │   ├── roadmap_service.py
│   │   └── chat_service.py
│   └── utils
│       ├── __init__.py
│       ├── json_helpers.py
│       └── validators.py
├── tests
│   ├── __init__.py
│   ├── test_agent.py
│   ├── test_roadmap.py
│   └── test_chat.py
├── requirements.txt
├── .env.example
└── README.md
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

## Usage Guidelines

- Access the API documentation at `http://127.0.0.1:8000/docs` after starting the server.
- Use the `/agent` endpoints to interact with the agent for gathering project specifications and generating roadmaps.
- Use the `/roadmap` endpoints to manage and modify roadmaps.
- Use the `/chat` endpoints for chat interactions with the agent.

## Testing

To run the tests, use the following command:

```bash
pytest
```

This will execute all unit tests defined in the `tests` directory.