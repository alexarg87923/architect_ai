#!/usr/bin/env python3
"""
Test script to verify API endpoints are working properly
Run this after starting the FastAPI server with: uvicorn app.main:app --reload
"""

import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000"

def test_endpoint(method: str, endpoint: str, data: Dict[Any, Any] = None) -> Dict[Any, Any]:
    """Test an API endpoint and return the response"""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method.upper() == "GET":
            response = requests.get(url)
        elif method.upper() == "POST":
            response = requests.post(url, json=data)
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        print(f"📡 {method.upper()} {endpoint}")
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Success")
            return result
        else:
            print(f"   ❌ Error: {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        print(f"   💔 Connection failed - is the server running?")
        return None
    except Exception as e:
        print(f"   💥 Error: {str(e)}")
        return None

def main():
    print("🚀 Testing Agentic Backend API Endpoints")
    print("=" * 50)
    
    # Test 1: Basic health checks
    print("\n1️⃣ Testing Health Endpoints")
    test_endpoint("GET", "/")
    test_endpoint("GET", "/health")
    test_endpoint("GET", "/api/agent/health")
    
    # Test 2: Start a new conversation
    print("\n2️⃣ Testing New Conversation")
    chat_request = {
        "message": "I want to build a web application",
        "action_type": "chat"
    }
    
    response = test_endpoint("POST", "/api/agent/chat", chat_request)
    
    if response:
        session_id = response.get("session_id")
        conversation_state = response.get("conversation_state")
        agent_response = response.get("agent_response")
        
        print(f"   Session ID: {session_id}")
        print(f"   Agent Response: {agent_response[:100]}...")
        print(f"   Phase: {conversation_state.get('phase')}")
        print(f"   Messages: {len(conversation_state.get('messages', []))}")
        
        # Test 3: Continue the conversation
        print("\n3️⃣ Testing Conversation Continuation")
        follow_up_request = {
            "message": "It's an e-commerce website for selling books",
            "session_id": session_id,
            "action_type": "chat",
            "conversation_state": conversation_state
        }
        
        response2 = test_endpoint("POST", "/api/agent/chat", follow_up_request)
        
        if response2:
            agent_response2 = response2.get("agent_response")
            updated_state = response2.get("conversation_state")
            
            print(f"   Agent Response: {agent_response2[:100]}...")
            print(f"   Phase: {updated_state.get('phase')}")
            print(f"   Messages: {len(updated_state.get('messages', []))}")
        
        # Test 4: Test conversation retrieval
        print("\n4️⃣ Testing Conversation Retrieval")
        test_endpoint("GET", f"/api/agent/conversation/{session_id}")
        
        # Test 5: Test roadmap retrieval (should return "not implemented" message)
        print("\n5️⃣ Testing Roadmap Retrieval")
        test_endpoint("GET", f"/api/agent/roadmap/{session_id}")
    
    print("\n" + "=" * 50)
    print("🏁 API endpoint testing complete!")
    print("\nTo run the server:")
    print("uvicorn app.main:app --reload")
    print("\nThen access the docs at:")
    print("http://localhost:8000/docs")

if __name__ == "__main__":
    main()
