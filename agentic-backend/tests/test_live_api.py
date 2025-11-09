#!/usr/bin/env python3
"""
Live API Test Script - Tests the actual running FastAPI server
"""
import requests
import json
import time

# Server configuration
BASE_URL = "http://127.0.0.1:8000"

def test_server_health():
    """Test if the server is running and healthy"""
    print("🔍 Testing server health...")
    
    try:
        # Test main health endpoint
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Main server health check passed")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Main health check failed: {response.status_code}")
            return False
        
        # Test agent health endpoint
        response = requests.get(f"{BASE_URL}/api/agent/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Agent service health check passed")
            print(f"   Client mode: {data.get('client_mode')}")
            print(f"   Model: {data.get('model')}")
        else:
            print(f"❌ Agent health check failed: {response.status_code}")
            return False
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Server not running or not accessible")
        print("   Please start the server with: uvicorn app.main:app --reload")
        return False
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_chat_endpoint():
    """Test the main chat endpoint"""
    print("\n🤖 Testing chat endpoint...")
    
    try:
        # Test basic chat request
        chat_data = {
            "message": "I want to build a web application for managing tasks",
            "action_type": "chat"
        }
        
        response = requests.post(
            f"{BASE_URL}/api/agent/chat",
            json=chat_data,
            timeout=30  # LLM calls can take time
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Chat endpoint working successfully")
            print(f"   Session ID: {data.get('session_id')}")
            print(f"   Agent response: {data.get('agent_response')[:100]}...")
            print(f"   Phase: {data.get('conversation_state', {}).get('phase')}")
            print(f"   Action button: {data.get('action_button')}")
            return data.get('session_id')
        else:
            print(f"❌ Chat endpoint failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Chat test failed: {e}")
        return None

def test_conversation_retrieval(session_id):
    """Test conversation retrieval"""
    print(f"\n📋 Testing conversation retrieval for session: {session_id}")
    
    try:
        response = requests.get(f"{BASE_URL}/api/agent/conversation/{session_id}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Conversation retrieval working")
            print(f"   Phase: {data.get('phase')}")
            print(f"   Specifications complete: {data.get('specifications_complete')}")
            print(f"   Messages count: {len(data.get('messages', []))}")
            return True
        else:
            print(f"❌ Conversation retrieval failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Conversation retrieval test failed: {e}")
        return False

def test_multi_turn_conversation():
    """Test a multi-turn conversation flow"""
    print("\n🔄 Testing multi-turn conversation...")
    
    session_id = None
    conversation_state = None
    
    messages = [
        "I want to build a task management web app",
        "It should be for small teams of 5-10 people",
        "I'm a beginner developer",
        "Yes, I need user authentication and I want to deploy it"
    ]
    
    try:
        for i, message in enumerate(messages):
            print(f"\n   Turn {i+1}: {message}")
            
            chat_data = {
                "message": message,
                "action_type": "chat",
                "session_id": session_id,
                "conversation_state": conversation_state
            }
            
            response = requests.post(
                f"{BASE_URL}/api/agent/chat",
                json=chat_data,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                session_id = data.get('session_id')
                conversation_state = data.get('conversation_state')
                
                print(f"   ✅ Response: {data.get('agent_response')[:100]}...")
                print(f"   Phase: {conversation_state.get('phase')}")
                
                if data.get('action_button'):
                    print(f"   🔘 Action button: {data.get('action_button')}")
                    
            else:
                print(f"   ❌ Turn {i+1} failed: {response.status_code}")
                return False
                
        print("\n✅ Multi-turn conversation test completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ Multi-turn conversation test failed: {e}")
        return False

def main():
    """Run all API tests"""
    print("🧪 Live API Testing - Agentic Backend")
    print("="*50)
    
    # Test server health first
    if not test_server_health():
        print("\n💡 To start the server, run:")
        print("   uvicorn app.main:app --reload")
        return
    
    # Test basic chat endpoint
    session_id = test_chat_endpoint()
    if not session_id:
        return
    
    # Test conversation retrieval
    test_conversation_retrieval(session_id)
    
    # Test multi-turn conversation
    test_multi_turn_conversation()
    
    print("\n" + "="*50)
    print("🎉 API testing completed!")
    print("\n📝 Next steps:")
    print("   1. Test the edit and expand action types")
    print("   2. Implement database persistence")
    print("   3. Connect with the React frontend")
    print("="*50)

if __name__ == "__main__":
    main()
