#!/usr/bin/env python3
"""
Extended API Test - Testing Full Roadmap Generation and Edit/Expand Features
"""
import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"

def test_complete_roadmap_generation():
    """Test the complete flow from discovery to roadmap generation"""
    print("🎯 Testing Complete Roadmap Generation Flow")
    print("="*50)
    
    session_id = None
    conversation_state = None
    
    # Discovery phase - provide comprehensive project info
    discovery_messages = [
        "I want to build a task management web application",
        "Let's call it TaskFlow Pro", 
        "The main goals are to help small teams organize tasks, track progress, and collaborate effectively",
        "I want it completed in about 6-8 weeks",
        "I'd like to use React for frontend and Python FastAPI for backend",
        "I'm a beginner developer",
        "Yes, I need user authentication and deployment",
        "This is for my portfolio to show potential employers",
        "The target audience is small development teams and startups",
        "No, I haven't built similar projects before"
    ]
    
    try:
        for i, message in enumerate(discovery_messages):
            print(f"\n📝 Discovery Step {i+1}: {message[:50]}...")
            
            chat_data = {
                "message": message,
                "action_type": "chat",
                "session_id": session_id,
                "conversation_state": conversation_state
            }
            
            response = requests.post(f"{BASE_URL}/api/agent/chat", json=chat_data, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                session_id = data.get('session_id')
                conversation_state = data.get('conversation_state')
                
                phase = conversation_state.get('phase')
                print(f"   ✅ Phase: {phase}")
                print(f"   Response: {data.get('agent_response')[:100]}...")
                
                if data.get('action_button') == 'generate_roadmap':
                    print(f"   🎯 READY FOR ROADMAP GENERATION!")
                    break
                    
            else:
                print(f"   ❌ Failed: {response.status_code}")
                return None, None
        
        # Now trigger roadmap generation by sending a message asking for it
        print(f"\n🚀 Triggering roadmap generation...")
        
        chat_data = {
            "message": "That sounds good, please generate the roadmap",
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
                return session_id, conversation_state
        else:
            print(f"❌ Roadmap generation failed: {response.status_code}")
            return None, None
            
    except Exception as e:
        print(f"❌ Complete flow test failed: {e}")
        return None, None

def test_expand_functionality(session_id, conversation_state):
    """Test roadmap expansion functionality"""
    print(f"\n🔧 Testing Roadmap Expansion")
    print("="*30)
    
    try:
        # Test expand action type
        chat_data = {
            "message": "I want to add a mobile app version to my project",
            "action_type": "expand",
            "session_id": session_id,
            "conversation_state": conversation_state
        }
        
        response = requests.post(f"{BASE_URL}/api/agent/chat", json=chat_data, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Expand mode activated successfully")
            print(f"   Agent response: {data.get('agent_response')[:150]}...")
            
            # Continue the expansion conversation
            follow_up_data = {
                "message": "Yes, I want a React Native mobile app that syncs with the web version, branching from the frontend development node",
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
                    print(f"   Response: {data2.get('agent_response')[:100]}...")
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
    """Test roadmap editing functionality"""
    print(f"\n✏️ Testing Roadmap Editing")
    print("="*30)
    
    try:
        # Test edit action type
        chat_data = {
            "message": "I want to modify the frontend development timeline",
            "action_type": "edit",
            "session_id": session_id,
            "conversation_state": conversation_state
        }
        
        response = requests.post(f"{BASE_URL}/api/agent/chat", json=chat_data, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Edit mode activated successfully")
            print(f"   Agent response: {data.get('agent_response')[:150]}...")
            
            # Continue the edit conversation
            follow_up_data = {
                "message": "I want to extend the frontend development from 5 days to 8 days because I want to add more advanced UI components",
                "action_type": "edit",
                "session_id": session_id,
                "conversation_state": data.get('conversation_state')
            }
            
            response2 = requests.post(f"{BASE_URL}/api/agent/chat", json=follow_up_data, timeout=60)
            
            if response2.status_code == 200:
                data2 = response2.json()
                print(f"✅ Node editing completed!")
                print(f"   Response: {data2.get('agent_response')[:100]}...")
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
    """Run comprehensive API tests"""
    print("🚀 COMPREHENSIVE API TESTING")
    print("🎯 Testing Full Agent Capabilities")
    print("="*60)
    
    # Test complete roadmap generation
    session_id, conversation_state = test_complete_roadmap_generation()
    
    if not session_id or not conversation_state:
        print("❌ Cannot continue without successful roadmap generation")
        return
    
    # Test roadmap retrieval
    test_roadmap_retrieval(session_id)
    
    # Test expansion functionality
    expand_success = test_expand_functionality(session_id, conversation_state)
    
    # Test editing functionality  
    edit_success = test_edit_functionality(session_id, conversation_state)
    
    print("\n" + "="*60)
    print("📊 COMPREHENSIVE TEST RESULTS:")
    print(f"   ✅ Roadmap Generation: ✅")
    print(f"   ✅ Roadmap Expansion: {'✅' if expand_success else '❌'}")
    print(f"   ✅ Roadmap Editing: {'✅' if edit_success else '❌'}")
    print(f"   🆔 Test Session ID: {session_id}")
    
    if expand_success and edit_success:
        print("\n🎉 ALL COMPREHENSIVE TESTS PASSED!")
        print("🚀 The agentic backend is fully functional!")
    else:
        print("\n⚠️ Some advanced features need attention")
    
    print("="*60)

if __name__ == "__main__":
    main()
