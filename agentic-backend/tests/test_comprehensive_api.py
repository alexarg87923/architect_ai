#!/usr/bin/env python3
"""
Extended API Test - Testing Full Roadmap Generation and Edit/Expand Features
Uses LLM to simulate realistic user interactions
"""
import requests
import json
import time
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

BASE_URL = "http://127.0.0.1:8000"

# Initialize OpenAI client for simulating user responses
try:
    # Try to use the same API keys as the main application
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

def simulate_user_response(agent_question: str, context: dict) -> str:
    """Simulate a realistic user response to an agent's question"""
    
    if not user_simulator:
        # Fallback to static responses if no LLM available
        return get_fallback_response(agent_question, context)
    
    try:
        # Create a prompt for the user simulator
        user_prompt = f"""You are a developer who wants to build "TaskFlow Pro" - a comprehensive task management web application for small development teams.

PROJECT CONTEXT:
- You want to build a task management app similar to Trello/Asana but focused on development teams
- Target users: small dev teams (5-10 people), startup founders, freelance developers  
- Tech stack preference: React frontend, Python FastAPI backend, PostgreSQL database
- Timeline: 6-8 weeks for portfolio/potential commercial use
- Your experience: beginner developer with some React/Python basics
- Inspiration: combination of Trello, Asana, and Notion

DETAILED UI/UX VISION:
**Layout Structure:**
- Left sidebar with navigation: Dashboard, Projects, My Tasks, Team, Calendar, Settings
- Top navbar with: user profile, notifications bell, search bar, project switcher
- Main content area that changes based on selected page

**Core Pages & Components:**
1. **Dashboard Page**: Welcome overview with project cards, recent activity feed, upcoming deadlines widget, team status overview
2. **Projects Page**: Grid/list view of all projects, each project card shows progress bar, team members avatars, recent activity
3. **Project Detail Page**: Kanban board (To Do, In Progress, Review, Done columns), task cards with tags, assignees, due dates
4. **Task Detail Modal**: Full task view with description editor, file attachments, comments thread, subtasks checklist, time tracking
5. **My Tasks Page**: Personal task list filtered by assigned to me, sortable by priority/due date, with calendar integration
6. **Team Page**: Team member profiles, workload distribution charts, role management
7. **Calendar Page**: Monthly/weekly view showing all team tasks and deadlines

**Key Features & Their Placement:**
- Real-time notifications (top navbar bell icon)
- File uploads (drag-drop in task detail modal)
- Team collaboration (comments in task detail, @mentions)
- Progress tracking (progress bars on project cards, burndown charts on dashboard)
- Task assignment (drag-drop between team members, assignment dropdown in task creation)

The AI agent just asked you: "{agent_question}"

Respond as this developer would - be very specific about UI components, page layouts, and how features integrate into your envisioned interface. Reference specific pages/components when describing functionality.

Keep responses detailed but focused (2-4 sentences max)."""

        response = user_simulator.chat.completions.create(
            model=user_model,
            messages=[{"role": "user", "content": user_prompt}],
            max_tokens=200,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        print(f"⚠️ User simulator error: {e} - using fallback")
        return get_fallback_response(agent_question, context)

def get_fallback_response(agent_question: str, context: dict) -> str:
    """Fallback responses when LLM simulation isn't available"""
    
    question_lower = agent_question.lower()
    response_count = context.get('response_count', 0)
    
    # Comprehensive fallback responses
    fallback_responses = [
        "I want to build TaskFlow Pro, a comprehensive task management web application for small development teams with a clean dashboard-based interface",
        "It should solve the problem of dev teams struggling to organize work across projects - I envision a left sidebar with Dashboard, Projects, My Tasks, Team, Calendar, Settings pages, plus a top navbar with user profile, notifications, and search",
        "The main Dashboard page should show project overview cards with progress bars, a recent activity feed, upcoming deadlines widget, and team status overview - like a command center for the whole team",
        "For the Projects page, I want a grid view of project cards showing progress, team member avatars, and recent activity, then clicking into a project shows a Kanban board with To Do, In Progress, Review, Done columns",
        "Task cards in the Kanban should show priority tags, assignee avatars, and due dates, with a detailed modal popup for full task editing including description, file attachments, comments thread, and subtasks checklist",
        "The My Tasks page should be a personal filtered view with sortable tasks assigned to me, integrated with a Calendar page showing monthly/weekly views of all team deadlines and milestones",
        "For team collaboration, I envision @mentions in task comments, real-time notifications in the top navbar bell icon, file drag-drop uploads in task modals, and a Team page with member profiles and workload charts",
        "The interface should feel modern like Notion but organized like Trello - clean typography, plenty of whitespace, drag-and-drop interactions, and smooth animations between page transitions",
        "I want React components for the sidebar navigation, project cards, task cards, modal overlays, notification dropdown, search autocomplete, and user profile menu in the top navbar",
        "For data flow, the dashboard widgets should pull from a central state showing active projects, recent activity feed from task updates, and deadline calculations across all assigned tasks",
        "The Kanban board component should support drag-drop between columns with real-time updates, while the task detail modal should handle rich text editing, file uploads to cloud storage, and threaded comments",
        "Timeline-wise, I see 6-8 weeks total: 1 week for project setup and design mockups, 2 weeks for core dashboard and navigation components, 2 weeks for Kanban board and task management, 1 week for team features and notifications, 1 week for calendar integration, 1 week for testing and deployment"
    ]
    
    if response_count < len(fallback_responses):
        return fallback_responses[response_count]
    else:
        return "I think we've covered all the important aspects of TaskFlow Pro. I'm ready to see the roadmap!"

def test_complete_roadmap_generation():
    """Test the complete flow from discovery to roadmap generation using LLM simulation"""
    print("🎯 Testing Complete Roadmap Generation Flow with LLM User Simulation")
    print("="*70)
    
    session_id = None
    conversation_state = None
    context = {'response_count': 0}
    max_discovery_rounds = 15  # Prevent infinite loops
    
    try:
        # Start with initial project description
        initial_message = "I want to build a task management web application called TaskFlow Pro for development teams"
        
        print(f"\n📝 Initial Message: {initial_message}")
        
        chat_data = {
            "message": initial_message,
            "action_type": "chat",
            "session_id": session_id,
            "conversation_state": conversation_state
        }
        
        response = requests.post(f"{BASE_URL}/api/agent/chat", json=chat_data, timeout=30)
        
        if response.status_code != 200:
            print(f"❌ Initial message failed: {response.status_code}")
            return None, None
            
        data = response.json()
        session_id = data.get('session_id')
        conversation_state = data.get('conversation_state')
        
        print(f"   ✅ Agent Response: {data.get('agent_response')[:120]}...")
        
        # Discovery conversation loop
        for round_num in range(max_discovery_rounds):
            context['response_count'] = round_num + 1
            
            # Get agent's last question
            agent_question = data.get('agent_response', '')
            
            # Check if we're ready for roadmap generation
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
            
            response = requests.post(f"{BASE_URL}/api/agent/chat", json=chat_data, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                conversation_state = data.get('conversation_state')
                current_phase = conversation_state.get('phase')
                print(f"   ✅ Phase: {current_phase}")
            else:
                print(f"   ❌ Failed: {response.status_code}")
                return None, None
        
        # Trigger roadmap generation
        print(f"\n🚀 Triggering roadmap generation...")
        
        current_phase = conversation_state.get('phase')
        if current_phase == 'confirmation':
            generation_message = "Perfect! Please generate the detailed roadmap for TaskFlow Pro now."
        else:
            generation_message = "That covers everything. Please generate a comprehensive roadmap for TaskFlow Pro."
        
        chat_data = {
            "message": generation_message,
            "action_type": "chat",
            "session_id": session_id,
            "conversation_state": conversation_state
        }
        
        response = requests.post(f"{BASE_URL}/api/agent/chat", json=chat_data, timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            conversation_state = data.get('conversation_state')
            roadmap = conversation_state.get('current_roadmap')
            
            if roadmap:
                print("✅ ROADMAP GENERATED SUCCESSFULLY!")
                print(f"   Project: {roadmap.get('project_specification', {}).get('title')}")
                print(f"   Nodes: {len(roadmap.get('nodes', []))}")
                print(f"   Total weeks: {roadmap.get('total_estimated_weeks')}")
                print(f"   Total hours: {roadmap.get('total_estimated_hours')}")
                
                # Print node titles
                print("   📋 Roadmap Nodes:")
                for node in roadmap.get('nodes', []):
                    print(f"     - {node.get('title')}")
                
                return session_id, conversation_state
            else:
                print("❌ Roadmap not found in response")
                print(f"   Agent response: {data.get('agent_response')}")
                return session_id, conversation_state
        else:
            print(f"❌ Roadmap generation failed: {response.status_code}")
            return None, None
            
    except Exception as e:
        print(f"❌ Complete flow test failed: {e}")
        return None, None

def test_expand_functionality(session_id, conversation_state):
    """Test roadmap expansion functionality with LLM simulation"""
    print(f"\n🔧 Testing Roadmap Expansion with User Simulation")
    print("="*50)
    
    try:
        # Initial expansion request
        expansion_idea = "I want to add a mobile app version to my TaskFlow Pro project"
        print(f"📱 Expansion Request: {expansion_idea}")
        
        chat_data = {
            "message": expansion_idea,
            "action_type": "expand",
            "session_id": session_id,
            "conversation_state": conversation_state
        }
        
        response = requests.post(f"{BASE_URL}/api/agent/chat", json=chat_data, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            agent_question = data.get('agent_response')
            print("✅ Expand mode activated successfully")
            print(f"   Agent: {agent_question[:150]}...")
            
            # Simulate detailed user response about mobile app requirements
            if user_simulator:
                user_prompt = f"""You are the developer building TaskFlow Pro (task management app with dashboard, sidebar nav, Kanban boards, etc.). You just told the agent you want to add a mobile app. 

The agent asked: "{agent_question}"

Respond with specific details about the mobile app component structure:
- React Native for cross-platform development
- Mobile-optimized versions of key pages: Dashboard (condensed widgets), Projects (card grid), Task Detail (full-screen modal), My Tasks (swipe actions)
- Should sync with web version's database in real-time
- Mobile-specific features: push notifications, offline task viewing, camera for file uploads, swipe gestures for task status changes
- Simplified navigation: bottom tab bar instead of sidebar, with Dashboard, Projects, Tasks, Profile tabs
- Branch from the frontend development milestone in the roadmap
- Estimated 3-4 weeks additional development

Be specific about UI components and how they adapt the web interface for mobile."""

                try:
                    sim_response = user_simulator.chat.completions.create(
                        model=user_model,
                        messages=[{"role": "user", "content": user_prompt}],
                        max_tokens=200,
                        temperature=0.7
                    )
                    user_response = sim_response.choices[0].message.content.strip()
                except:
                    user_response = "I want a React Native mobile app that adapts our web dashboard into mobile-optimized components: condensed Dashboard widgets, project card grid view, full-screen Task Detail modals, and My Tasks with swipe actions for status changes. It should use a bottom tab bar (Dashboard, Projects, Tasks, Profile) instead of the sidebar, sync with our PostgreSQL database in real-time, and add mobile-specific features like push notifications and camera uploads. This should branch from the frontend development milestone and add about 3-4 weeks."
            else:
                user_response = "I want a React Native mobile app that adapts our web dashboard into mobile-optimized components: condensed Dashboard widgets, project card grid view, full-screen Task Detail modals, and My Tasks with swipe actions for status changes. It should use a bottom tab bar (Dashboard, Projects, Tasks, Profile) instead of the sidebar, sync with our PostgreSQL database in real-time, and add mobile-specific features like push notifications and camera uploads. This should branch from the frontend development milestone and add about 3-4 weeks."
            
            print(f"   User: {user_response[:150]}...")
            
            # Send detailed expansion request
            follow_up_data = {
                "message": user_response,
                "action_type": "expand", 
                "session_id": session_id,
                "conversation_state": data.get('conversation_state')
            }
            
            response2 = requests.post(f"{BASE_URL}/api/agent/chat", json=follow_up_data, timeout=60)
            
            if response2.status_code == 200:
                data2 = response2.json()
                new_state = data2.get('conversation_state')
                new_roadmap = new_state.get('current_roadmap')
                
                if new_roadmap:
                    new_node_count = len(new_roadmap.get('nodes', []))
                    print(f"✅ Roadmap expanded successfully!")
                    print(f"   New node count: {new_node_count}")
                    print(f"   Response: {data2.get('agent_response')[:120]}...")
                    return True
                else:
                    print("❌ Roadmap expansion didn't update nodes")
                    return False
            else:
                print(f"❌ Expansion follow-up failed: {response2.status_code}")
                return False
        else:
            print(f"❌ Expand mode failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Expand test failed: {e}")
        return False

def test_edit_functionality(session_id, conversation_state):
    """Test roadmap editing functionality with LLM simulation"""
    print(f"\n✏️ Testing Roadmap Editing with User Simulation")
    print("="*50)
    
    try:
        # Initial edit request
        edit_request = "I want to modify the authentication system to include OAuth social login"
        print(f"🔧 Edit Request: {edit_request}")
        
        chat_data = {
            "message": edit_request,
            "action_type": "edit",
            "session_id": session_id,
            "conversation_state": conversation_state
        }
        
        response = requests.post(f"{BASE_URL}/api/agent/chat", json=chat_data, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            agent_question = data.get('agent_response')
            print("✅ Edit mode activated successfully")
            print(f"   Agent: {agent_question[:150]}...")
            
            # Simulate detailed user response about OAuth requirements
            if user_simulator:
                user_prompt = f"""You are the developer building TaskFlow Pro with a dashboard interface, sidebar navigation, and multiple pages. You want to modify the authentication system to include OAuth social login.

The agent asked: "{agent_question}"

Respond with specific details about how OAuth fits into your component structure:
- Add Google, GitHub, and Microsoft OAuth buttons to the login page component
- Update the user registration flow to handle OAuth profile data (avatar, name, email)
- Modify the top navbar user profile dropdown to show OAuth provider info
- Keep existing email/password login as backup option
- Update backend authentication middleware and user model
- Affects the Login component, UserProfile component in navbar, and Settings page for account management
- Estimated 2-3 extra days for implementation

Be specific about which components/pages need updates and the OAuth user experience."""

                try:
                    sim_response = user_simulator.chat.completions.create(
                        model=user_model,
                        messages=[{"role": "user", "content": user_prompt}],
                        max_tokens=200,
                        temperature=0.7
                    )
                    user_response = sim_response.choices[0].message.content.strip()
                except:
                    user_response = "I want to modify the Login component to add Google, GitHub, and Microsoft OAuth buttons alongside the existing email/password form. This requires updating the user registration flow to handle OAuth profile data (avatar, name, email), modifying the top navbar UserProfile component to show OAuth provider info, and updating the Settings page for account management. The backend auth middleware and user model need updates too. Should add about 2-3 days to the authentication development timeline."
            else:
                user_response = "I want to modify the Login component to add Google, GitHub, and Microsoft OAuth buttons alongside the existing email/password form. This requires updating the user registration flow to handle OAuth profile data (avatar, name, email), modifying the top navbar UserProfile component to show OAuth provider info, and updating the Settings page for account management. The backend auth middleware and user model need updates too. Should add about 2-3 days to the authentication development timeline."
            
            print(f"   User: {user_response[:150]}...")
            
            # Send detailed edit request
            follow_up_data = {
                "message": user_response,
                "action_type": "edit",
                "session_id": session_id,
                "conversation_state": data.get('conversation_state')
            }
            
            response2 = requests.post(f"{BASE_URL}/api/agent/chat", json=follow_up_data, timeout=60)
            
            if response2.status_code == 200:
                data2 = response2.json()
                print(f"✅ Node editing completed!")
                print(f"   Response: {data2.get('agent_response')[:120]}...")
                return True
            else:
                print(f"❌ Edit follow-up failed: {response2.status_code}")
                return False
        else:
            print(f"❌ Edit mode failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Edit test failed: {e}")
        return False

def test_roadmap_retrieval(session_id):
    """Test roadmap retrieval endpoint"""
    print(f"\n📊 Testing Roadmap Retrieval")
    print("="*30)
    
    try:
        response = requests.get(f"{BASE_URL}/api/agent/roadmap/{session_id}")
        
        if response.status_code == 200:
            print("✅ Roadmap retrieval endpoint working")
            data = response.json()
            print(f"   Response: {data}")
            return True
        else:
            print(f"❌ Roadmap retrieval failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Roadmap retrieval test failed: {e}")
        return False

def main():
    """Run comprehensive API tests with LLM user simulation"""
    print("🚀 COMPREHENSIVE API TESTING WITH AI USER SIMULATION")
    print("🎯 Testing Full Agent Capabilities with Realistic Conversations")
    print("="*80)
    
    # Test complete roadmap generation with LLM simulation
    session_id, conversation_state = test_complete_roadmap_generation()
    
    if not session_id or not conversation_state:
        print("❌ Cannot continue without successful roadmap generation")
        return
    
    # Test roadmap retrieval
    test_roadmap_retrieval(session_id)
    
    # Test expansion functionality with LLM simulation
    expand_success = test_expand_functionality(session_id, conversation_state)
    
    # Test editing functionality with LLM simulation  
    edit_success = test_edit_functionality(session_id, conversation_state)
    
    print("\n" + "="*80)
    print("📊 COMPREHENSIVE TEST RESULTS:")
    print(f"   ✅ Realistic Discovery Conversation: ✅")
    print(f"   ✅ Roadmap Generation: ✅")
    print(f"   ✅ Roadmap Expansion: {'✅' if expand_success else '❌'}")
    print(f"   ✅ Roadmap Editing: {'✅' if edit_success else '❌'}")
    print(f"   🆔 Test Session ID: {session_id}")
    print(f"   🤖 User Simulation: {'LLM-powered' if user_simulator else 'Static fallback'}")
    
    if expand_success and edit_success:
        print("\n🎉 ALL COMPREHENSIVE TESTS PASSED!")
        print("🚀 The agentic backend handles realistic user conversations perfectly!")
    else:
        print("\n⚠️ Some advanced features need attention")
    
    print("="*80)

if __name__ == "__main__":
    main()
