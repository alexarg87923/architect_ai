#!/usr/bin/env python3
"""
Roadmap Generation Test - Focus on generating a complete roadmap for frontend visualization testing
This script generates a roadmap and associates it with John Doe's Sample Project 1
"""
import requests
import json
import time
import os
import sqlite3
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

BASE_URL = "http://127.0.0.1:8000"

# Initialize OpenAI client for simulating user responses
try:
    groq_key = os.getenv('GROQ_KEY')
    openai_key = os.getenv('OPENAI_API_KEY')
    
    if groq_key:
        user_simulator = OpenAI(api_key=groq_key, base_url="https://api.groq.com/openai/v1")
        user_model = "llama3-70b-8192"
        print("🤖 Using GROQ for user simulation")
    elif openai_key:
        user_simulator = OpenAI(api_key=openai_key)
        user_model = "gpt-3.5-turbo"
        print("🤖 Using OpenAI for user simulation")
    else:
        print("⚠️ No API key found for user simulation - falling back to static responses")
        user_simulator = None
        user_model = None
except Exception as e:
    print(f"⚠️ Failed to initialize user simulator: {e} - falling back to static responses")
    user_simulator = None
    user_model = None

def check_backend_health():
    """Check if the backend server is running"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend server is running")
            return True
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to backend server: {e}")
        print("   Make sure to start the backend with: cd agentic-backend && python -m uvicorn app.main:app --reload")
        return False

def setup_test_project():
    """Setup test project by ensuring John Doe exists and cleaning up any existing Sample Project 1"""
    print("� Setting up test project...")
    try:
        # Connect to the database
        db_path = "/Users/henriquepitta/Desktop/Roadmap/agentic-backend/roadmap.db"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if John Doe user exists
        cursor.execute("SELECT id FROM users WHERE email = 'johndoe@example.com'")
        user_result = cursor.fetchone()
        
        if user_result:
            user_id = user_result[0]
            print(f"✅ Found existing John Doe user (ID: {user_id})")
        else:
            # Create John Doe user
            cursor.execute("""
                INSERT INTO users (email, first_name, last_name, is_active, created_at, updated_at) 
                VALUES ('johndoe@example.com', 'John', 'Doe', 1, datetime('now'), datetime('now'))
            """)
            user_id = cursor.lastrowid
            print(f"✅ Created John Doe user (ID: {user_id})")
        
        # Clean up any existing "Sample Project 1" for this user
        cursor.execute("""
            SELECT id FROM projects 
            WHERE user_id = ? AND name = 'Sample Project 1'
        """, (user_id,))
        existing_project = cursor.fetchone()
        
        if existing_project:
            project_id = existing_project[0]
            print(f"🗑️ Cleaning up existing Sample Project 1 (ID: {project_id})")
            
            # Delete related roadmaps and conversations for this project
            cursor.execute("DELETE FROM roadmaps WHERE user_id = ?", (user_id,))
            cursor.execute("""
                DELETE FROM messages WHERE conversation_id IN (
                    SELECT id FROM conversations WHERE user_id = ?
                )
            """, (user_id,))
            cursor.execute("DELETE FROM conversations WHERE user_id = ?", (user_id,))
            cursor.execute("DELETE FROM projects WHERE id = ?", (project_id,))
        
        # Create fresh Sample Project 1
        cursor.execute("""
            INSERT INTO projects (user_id, name, description, status, created_at, updated_at)
            VALUES (?, 'Sample Project 1', 'CodeMentor - AI-powered coding assistant and learning platform', 'active', datetime('now'), datetime('now'))
        """, (user_id,))
        project_id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        
        print(f"✅ Sample Project 1 setup complete (ID: {project_id})")
        
    except Exception as e:
        print(f"❌ Test project setup failed: {e}")
        return False
    return True

def simulate_user_response(agent_question: str, context: dict) -> str:
    """Simulate a realistic user response to an agent's question"""
    
    if not user_simulator:
        return get_fallback_response(agent_question, context)
    
    try:
        user_prompt = f"""You are a computer science student who wants to build "CodeMentor" - an AI-powered coding assistant and learning platform to help students learn programming more effectively.

Project Vision:
- React frontend with code editor integration (Monaco Editor) 
- FastAPI backend with OpenAI integration for code explanations and help
- User accounts to track progress and save code examples
- Real-time code analysis and suggestions
- Learning paths for different programming languages
- Code challenges with AI-generated hints and explanations
- Community features for sharing and discussing code

Key Features for MVP:
- Interactive code editor with syntax highlighting
- AI-powered code explanation and error analysis
- User authentication and progress tracking  
- Basic learning modules for Python/JavaScript
- Code challenge system with difficulty levels

You're experienced with React and Python but want to build something impactful quickly using proven patterns and existing APIs/libraries rather than reinventing everything.

The AI agent asked: "{agent_question}"

Response Round: {context.get('response_count', 1)}/15

Provide a strategic answer focused on efficient implementation and leveraging existing tools. Keep responses under 150 words."""

        response = user_simulator.chat.completions.create(
            model=user_model,
            messages=[{"role": "user", "content": user_prompt}],
            max_tokens=200,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        print(f"⚠️ LLM simulation failed: {e}")
        return get_fallback_response(agent_question, context)

def get_fallback_response(agent_question: str, context: dict) -> str:
    """Fallback responses when LLM is not available"""
    
    response_round = context.get('response_count', 1)
    
    fallback_responses = [
        "I want to build CodeMentor, an AI-powered coding assistant and learning platform to help students learn programming more effectively. It should have an interactive code editor, AI explanations for code and errors, user progress tracking, and learning challenges.",
        
        "The main features for the MVP are: interactive code editor with Monaco Editor, AI-powered code explanations using OpenAI API, user authentication for progress tracking, basic learning modules for Python and JavaScript, and a code challenge system with difficulty levels.",
        
        "For tech stack, I'm experienced with React and Python, so I'd like React frontend with FastAPI backend. I want to use existing solutions like Monaco Editor for the code editor and OpenAI API for AI features rather than building everything from scratch.",
        
        "The MVP should focus on core functionality: code editor integration, AI code analysis and explanations, user accounts with simple authentication, basic learning paths, and a few code challenges. I can add community features and advanced learning paths later.",
        
        "I'm a CS student with good programming experience but limited time. I want to build something impressive for my portfolio that could actually help other students. I prefer using proven libraries and APIs to move quickly.",
        
        "For efficiency, I'm thinking Monaco Editor for the code editor, Clerk or Supabase for authentication, OpenAI API for code analysis, and deploy on Vercel for frontend and Railway for backend. This should minimize setup time and focus on core features.",
        
        "Timeline goal is 6-8 weeks to have a working MVP that I can demonstrate and potentially use to help other students. I want to focus on getting the AI code explanation feature working first since that's the main value proposition.",
        
        "That covers the main vision. I think we have enough detail to create an efficient roadmap for CodeMentor. Please generate the roadmap now, focusing on proven patterns and rapid development."
    ]
    
    if response_round <= len(fallback_responses):
        return fallback_responses[response_round - 1]
    else:
        return "That covers everything I need. Please generate an efficient roadmap for CodeMentor now."

def test_roadmap_generation_for_visualization():
    """Generate a complete roadmap for frontend visualization testing"""
    print("🎯 Generating Roadmap for Frontend Visualization Testing")
    print("="*60)
    
    session_id = None
    conversation_state = None
    context = {'response_count': 0}
    max_discovery_rounds = 15
    
    # Get the user_id for John Doe
    try:
        db_path = "/Users/henriquepitta/Desktop/Roadmap/agentic-backend/roadmap.db"
        import sqlite3
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE email = 'johndoe@example.com'")
        user_result = cursor.fetchone()
        if not user_result:
            print("❌ John Doe user not found")
            return None, None, None
        user_id = user_result[0]
        conn.close()
        print(f"   ✅ Found user ID: {user_id}")
    except Exception as e:
        print(f"❌ Failed to get user ID: {e}")
        return None, None, None
    
    try:
        # Initial project description
        initial_message = "I want to build CodeMentor, an AI-powered coding assistant and learning platform to help students learn programming more effectively"
        
        print(f"\n📝 Initial Message: {initial_message}")
        
        # Generate a session ID for the initial request
        import uuid
        initial_session_id = str(uuid.uuid4())
        
        # Create initial conversation state with user_id
        initial_conversation_state = {
            "session_id": initial_session_id,
            "user_id": user_id,
            "phase": "discovery",
            "specifications_complete": False,
            "project_specification": None,
            "current_roadmap": None,
            "messages": []
        }
        
        chat_data = {
            "message": initial_message,
            "action_type": "chat",
            "session_id": None,  # Let the API generate or use the one from conversation_state
            "conversation_state": initial_conversation_state
        }
        
        response = requests.post(f"{BASE_URL}/api/agent/chat", json=chat_data, timeout=30)
        
        if response.status_code != 200:
            print(f"❌ Initial message failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None, None, None
        
        data = response.json()
        session_id = data.get('session_id')
        conversation_state = data.get('conversation_state')
        
        # Ensure conversation_state has user_id for subsequent calls
        if conversation_state and not conversation_state.get('user_id'):
            conversation_state['user_id'] = user_id
        
        print(f"   ✅ Session started: {session_id}")
        print(f"   ✅ Agent Response: {data.get('agent_response')[:120]}...")
        
        # Discovery conversation loop
        for round_num in range(max_discovery_rounds):
            context['response_count'] = round_num + 1
            
            # Get agent's last question
            agent_question = data.get('agent_response', '')
            
            # Check if ready for roadmap generation
            current_phase = conversation_state.get('phase')
            action_button = data.get('action_button')
            
            if action_button == 'generate_roadmap' or current_phase == 'confirmation':
                print(f"\n🎯 READY FOR ROADMAP GENERATION! (Phase: {current_phase})")
                break
                
            if 'roadmap' in agent_question.lower() and 'generate' in agent_question.lower():
                print(f"\n🎯 Agent is ready to generate roadmap!")
                break
            
            # Simulate user response
            user_response = simulate_user_response(agent_question, context)
            print(f"\n📝 Discovery Round {round_num + 1}:")
            print(f"   Agent: {agent_question[:100]}...")
            print(f"   User: {user_response[:100]}...")
            
            # Send user response
            chat_data = {
                "message": user_response,
                "action_type": "chat", 
                "session_id": session_id,
                "conversation_state": conversation_state
            }
            
            # Ensure conversation_state has user_id
            if conversation_state and not conversation_state.get('user_id'):
                conversation_state['user_id'] = user_id
            
            response = requests.post(f"{BASE_URL}/api/agent/chat", json=chat_data, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                conversation_state = data.get('conversation_state')
                current_phase = conversation_state.get('phase')
                print(f"   ✅ Phase: {current_phase}")
            else:
                print(f"   ❌ Failed: {response.status_code}")
                return None, None, None
        
        # Trigger roadmap generation
        print(f"\n🚀 Triggering roadmap generation...")
        
        if current_phase == 'confirmation':
            generation_message = "Perfect! Please generate the detailed roadmap for CodeMentor now."
        else:
            generation_message = "That covers everything. Please generate an efficient roadmap for CodeMentor."
        
        chat_data = {
            "message": generation_message,
            "action_type": "chat",
            "session_id": session_id,
            "conversation_state": conversation_state
        }
        
        # Ensure conversation_state has user_id
        if conversation_state and not conversation_state.get('user_id'):
            conversation_state['user_id'] = user_id
        
        response = requests.post(f"{BASE_URL}/api/agent/chat", json=chat_data, timeout=120)  # Increased timeout for full generation
        
        if response.status_code == 200:
            data = response.json()
            conversation_state = data.get('conversation_state')
            roadmap = conversation_state.get('current_roadmap') if conversation_state else None
            
            if roadmap:
                print("✅ ROADMAP GENERATED SUCCESSFULLY!")
                print(f"   Project: {roadmap.get('project_specification', {}).get('title')}")
                print(f"   Nodes: {len(roadmap.get('nodes', []))}")
                print(f"   Total weeks: {roadmap.get('total_estimated_weeks')}")
                print(f"   Total hours: {roadmap.get('total_estimated_hours')}")
                
                # Print detailed roadmap with subtasks
                print("   📋 Detailed Roadmap:")
                for i, node in enumerate(roadmap.get('nodes', []), 1):
                    subtasks = node.get('subtasks', [])
                    print(f"     {i}. {node.get('title')} - {len(subtasks)} subtasks")
                    for j, subtask in enumerate(subtasks, 1):
                        estimated_hours = subtask.get('estimated_hours', 0)
                        print(f"        {j}. {subtask.get('title')} ({estimated_hours}h)")
                
                # Print project overview if available
                setup_node = None
                for node in roadmap.get('nodes', []):
                    if 'setup' in node.get('tags', []) or 'setup' in node.get('title', '').lower() or 'environment' in node.get('title', '').lower():
                        setup_node = node
                        break
                
                if setup_node and setup_node.get('overview'):
                    print("\n   🎯 Project Overview (Setup Node):")
                    print(f"     Node: {setup_node.get('title')}")
                    overview_steps = setup_node.get('overview', [])
                    for i, step in enumerate(overview_steps, 1):
                        print(f"     {i}. {step}")
                else:
                    print("   ⚠️  No project overview found in setup node")
                
                return session_id, conversation_state, roadmap
            else:
                print("❌ Roadmap not found in response")
                return session_id, conversation_state, None
        else:
            print(f"❌ Roadmap generation failed: {response.status_code}")
            return None, None, None
            
    except Exception as e:
        print(f"❌ Roadmap generation test failed: {e}")
        return None, None, None

def link_roadmap_to_project(session_id, roadmap_data):
    """Link the generated roadmap to John Doe's Sample Project 1"""
    print(f"\n🔗 Linking roadmap to Sample Project 1...")
    
    try:
        # Connect to database and update project with roadmap
        db_path = "/Users/henriquepitta/Desktop/Roadmap/agentic-backend/roadmap.db"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Find John Doe user ID
        cursor.execute("SELECT id FROM users WHERE email = 'johndoe@example.com'")
        user_result = cursor.fetchone()
        if not user_result:
            print("❌ John Doe user not found")
            conn.close()
            return False
        
        user_id = user_result[0]
        
        # Find Sample Project 1 for this user
        cursor.execute("""
            SELECT id FROM projects 
            WHERE user_id = ? AND name = 'Sample Project 1'
        """, (user_id,))
        project_result = cursor.fetchone()
        if not project_result:
            print("❌ Sample Project 1 not found for John Doe")
            conn.close()
            return False
        
        project_id = project_result[0]
        
        # Update project with roadmap data
        roadmap_json = json.dumps(roadmap_data)
        cursor.execute("""
            UPDATE projects 
            SET roadmap_data = ?, updated_at = datetime('now')
            WHERE id = ? AND user_id = ?
        """, (roadmap_json, project_id, user_id))
        
        # Also create a roadmap record
        cursor.execute("""
            INSERT INTO roadmaps (user_id, roadmap_data, created_at, updated_at)
            VALUES (?, ?, datetime('now'), datetime('now'))
        """, (user_id, roadmap_json))
        
        conn.commit()
        conn.close()
        
        print(f"✅ Roadmap linked to Sample Project 1 successfully! (User ID: {user_id}, Project ID: {project_id})")
        return True
        
    except Exception as e:
        print(f"❌ Failed to link roadmap to project: {e}")
        return False

def main():
    """Run the roadmap generation test for visualization development"""
    print("🚀 Starting Roadmap Generation Test for Frontend Visualization")
    print("="*70)
    
    # Step 0: Check if backend is running
    if not check_backend_health():
        return
    
    # Step 1: Setup test project
    if not setup_test_project():
        return
    
    # Step 2: Generate roadmap through simulated conversation
    session_id, conversation_state, roadmap = test_roadmap_generation_for_visualization()
    
    if not roadmap:
        print("❌ Failed to generate roadmap - cannot proceed")
        return
    
    # Step 3: Link roadmap to John Doe's project
    if link_roadmap_to_project(session_id, roadmap):
        print("\n🎉 SUCCESS! Roadmap generation test completed!")
        print("\n📋 Next Steps for Frontend Testing:")
        print("   1. Start the backend server: cd agentic-backend && python -m uvicorn app.main:app --reload")
        print("   2. Start the frontend: cd frontend && npm run dev")
        print("   3. Login as John Doe (johndoe@example.com)")
        print("   4. Select 'Sample Project 1' to view the generated roadmap")
        print("   5. Test and refine the Canvas/ReactFlow visualization")
        print(f"\n📊 Generated Roadmap Summary:")
        print(f"   • Project: {roadmap.get('project_specification', {}).get('title', 'CodeMentor')}")
        print(f"   • Nodes: {len(roadmap.get('nodes', []))}")
        print(f"   • Timeline: {roadmap.get('total_estimated_weeks', 'N/A')} weeks")
        print(f"   • Session ID: {session_id}")
    else:
        print("❌ Failed to link roadmap to project")

if __name__ == "__main__":
    main()
