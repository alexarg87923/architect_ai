"""
User Simulator Service - Replicates the test script's user simulation approach
"""
from openai import OpenAI
from typing import Dict, Optional
from app.core.config import settings
from .project_prompts import get_user_persona_prompt, format_conversation_history

class UserSimulator:
    """Simulates user responses using LLM (with fallback)"""
    
    def __init__(self):
        # Initialize LLM client
        try:
            groq_key = settings.GROQ_API_KEY
            openai_key = settings.OPENAI_API_KEY
            
            if groq_key:
                self.client = OpenAI(api_key=groq_key, base_url="https://api.groq.com/openai/v1")
                self.model = "llama-3.3-70b-versatile"
                self.use_llm = True
                print(f"✅ Using GROQ for user simulation")
            elif openai_key:
                self.client = OpenAI(api_key=openai_key)
                self.model = "gpt-3.5-turbo"
                self.use_llm = True
                print(f"✅ Using OpenAI for user simulation")
            else:
                self.client = None
                self.model = None
                self.use_llm = False
                print(f"❌ No API keys found for user simulation")
        except Exception as e:
            print(f"⚠️ Failed to initialize user simulator: {e}")
            self.client = None
            self.model = None
            self.use_llm = False
    
    def simulate_user_response(self, agent_question: str, context: Dict) -> str:
        """Simulate a realistic user response to an agent's question"""
        
        if not self.use_llm:
            raise Exception("LLM not available for user simulation")
        
        try:
            # Get conversation history for context
            conversation_history = context.get('conversation_history', [])
            history_text = format_conversation_history(conversation_history)
            
            # Use centralized prompt from project_prompts
            project_type = context.get('project_type', 'codementor')
            user_prompt = get_user_persona_prompt(
                project_type=project_type,
                conversation_history=history_text,
                agent_question=agent_question,
                response_count=context.get('response_count', 1)
            )

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": user_prompt}],
                max_tokens=200,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"❌ LLM simulation failed: {e}")
            raise Exception(f"User simulation failed: {e}")
    
 