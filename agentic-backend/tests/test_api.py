#!/usr/bin/env python3
"""
Quick test script to verify API routes are working
"""
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

def test_imports():
    """Test if all imports work correctly"""
    print("Testing imports...")
    
    try:
        from app.services.agent_service import AgentService
        print("✅ AgentService import successful")
    except Exception as e:
        print(f"❌ AgentService import failed: {e}")
        return False
    
    try:
        from app.models.agent import ConversationState, ChatMessage
        print("✅ Agent models import successful")
    except Exception as e:
        print(f"❌ Agent models import failed: {e}")
        return False
    
    try:
        from app.api.routes.agent import router
        print("✅ Agent routes import successful")
    except Exception as e:
        print(f"❌ Agent routes import failed: {e}")
        return False
    
    try:
        from app.core.config import settings
        print(f"✅ Config import successful - Using {settings.APP_NAME}")
    except Exception as e:
        print(f"❌ Config import failed: {e}")
        return False
    
    return True

def test_agent_service():
    """Test if AgentService initializes correctly"""
    print("\nTesting AgentService initialization...")
    
    try:
        from app.services.agent_service import AgentService
        agent = AgentService()
        print(f"✅ AgentService initialized successfully")
        print(f"   Client mode: {agent.client_mode}")
        print(f"   Model: {agent.model}")
        print(f"   Max tokens: {agent.max_tokens}")
        return True
    except Exception as e:
        print(f"❌ AgentService initialization failed: {e}")
        return False

def test_conversation_state():
    """Test ConversationState creation"""
    print("\nTesting ConversationState...")
    
    try:
        from app.models.agent import ConversationState, ChatMessage
        
        # Create a test conversation state
        state = ConversationState(
            session_id="test-session",
            phase="discovery",
            specifications_complete=False,
            messages=[]
        )
        
        # Add a test message
        message = ChatMessage(
            role="user",
            content="Hello, I want to build a web app",
            timestamp="2025-01-01T00:00:00"
        )
        
        state.messages.append(message)
        
        print(f"✅ ConversationState created successfully")
        print(f"   Session ID: {state.session_id}")
        print(f"   Phase: {state.phase}")
        print(f"   Messages: {len(state.messages)}")
        return True
    except Exception as e:
        print(f"❌ ConversationState creation failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Agentic Backend Components\n")
    
    all_tests_passed = True
    
    # Run tests
    all_tests_passed &= test_imports()
    all_tests_passed &= test_agent_service()
    all_tests_passed &= test_conversation_state()
    
    print("\n" + "="*50)
    if all_tests_passed:
        print("🎉 All tests passed! The backend is ready for testing.")
    else:
        print("💥 Some tests failed. Check the errors above.")
    
    print("="*50)
