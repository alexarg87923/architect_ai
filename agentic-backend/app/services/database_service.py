from sqlalchemy.orm import Session
from app.models.database import Conversation, Message, Roadmap as RoadmapDB
from app.models.api_schemas import ConversationState, ChatMessage, Roadmap
from typing import Optional
import json
from datetime import datetime

class DatabaseService:
    """Service for handling database operations for conversations and roadmaps"""
    
    def save_conversation_state(self, db: Session, conversation_state: ConversationState) -> bool:
        """Save or update conversation state in database"""
        try:
            # Find existing conversation or create new one
            db_conversation = db.query(Conversation).filter(
                Conversation.session_id == conversation_state.session_id
            ).first()
            
            if not db_conversation:
                # Ensure user_id is provided for new conversations
                if not conversation_state.user_id:
                    raise ValueError("user_id is required for new conversations")
                    
                db_conversation = Conversation(
                    session_id=conversation_state.session_id,
                    user_id=conversation_state.user_id,
                    current_phase=conversation_state.phase,
                    is_specification_complete=conversation_state.specifications_complete
                )
                db.add(db_conversation)
            else:
                db_conversation.current_phase = conversation_state.phase
                db_conversation.is_specification_complete = conversation_state.specifications_complete
                db_conversation.updated_at = datetime.utcnow()
            
            # Save project specification if available
            if conversation_state.project_specification:
                db_conversation.project_name = conversation_state.project_specification.title
                db_conversation.specifications = conversation_state.project_specification.dict()
            
            db.commit()
            db.refresh(db_conversation)
            
            # Save roadmap if available
            if conversation_state.current_roadmap:
                self.save_roadmap(db, db_conversation.id, conversation_state.current_roadmap, conversation_state.user_id)
            
            # Save new messages
            self.save_messages(db, db_conversation.id, conversation_state.messages)
            
            return True
            
        except Exception as e:
            db.rollback()
            print(f"Error saving conversation state: {e}")
            return False
    
    def save_roadmap(self, db: Session, conversation_id: int, roadmap: Roadmap, user_id: int) -> bool:
        """Save or update roadmap in database"""
        try:
            # Find existing roadmap or create new one
            db_roadmap = db.query(RoadmapDB).filter(
                RoadmapDB.conversation_id == conversation_id
            ).first()
            
            roadmap_data = roadmap.dict()
            
            if not db_roadmap:
                db_roadmap = RoadmapDB(
                    conversation_id=conversation_id,
                    user_id=user_id,
                    roadmap_data=roadmap_data
                )
                db.add(db_roadmap)
            else:
                db_roadmap.roadmap_data = roadmap_data
                db_roadmap.updated_at = datetime.utcnow()
            
            db.commit()
            return True
            
        except Exception as e:
            db.rollback()
            print(f"Error saving roadmap: {e}")
            return False
    
    def save_messages(self, db: Session, conversation_id: int, messages: list[ChatMessage]) -> bool:
        """Save messages to database (only new ones)"""
        try:
            # Get existing message count
            existing_count = db.query(Message).filter(
                Message.conversation_id == conversation_id
            ).count()
            
            # Save only new messages
            new_messages = messages[existing_count:]
            
            for msg in new_messages:
                db_message = Message(
                    conversation_id=conversation_id,
                    role=msg.role,
                    content=msg.content,
                    action_type=msg.action_type,
                    timestamp=datetime.fromisoformat(msg.timestamp) if msg.timestamp else datetime.utcnow()
                )
                db.add(db_message)
            
            db.commit()
            return True
            
        except Exception as e:
            db.rollback()
            print(f"Error saving messages: {e}")
            return False
    
    def load_conversation_state(self, db: Session, session_id: str) -> Optional[ConversationState]:
        """Load conversation state from database"""
        try:
            # Get conversation
            db_conversation = db.query(Conversation).filter(
                Conversation.session_id == session_id
            ).first()
            
            if not db_conversation:
                return None
            
            # Get messages
            db_messages = db.query(Message).filter(
                Message.conversation_id == db_conversation.id
            ).order_by(Message.timestamp).all()
            
            messages = [
                ChatMessage(
                    role=msg.role,
                    content=msg.content,
                    timestamp=msg.timestamp.isoformat(),
                    action_type=msg.action_type
                ) for msg in db_messages
            ]
            
            # Get roadmap
            db_roadmap = db.query(RoadmapDB).filter(
                RoadmapDB.conversation_id == db_conversation.id
            ).first()
            
            current_roadmap = None
            if db_roadmap and db_roadmap.roadmap_data:
                current_roadmap = Roadmap(**db_roadmap.roadmap_data)
            
            # Build conversation state
            from app.models.agent import ProjectSpecification
            project_specification = None
            if db_conversation.specifications:
                project_specification = ProjectSpecification(**db_conversation.specifications)
            
            conversation_state = ConversationState(
                session_id=session_id,
                phase=db_conversation.current_phase,
                specifications_complete=db_conversation.is_specification_complete,
                project_specification=project_specification,
                current_roadmap=current_roadmap,
                messages=messages
            )
            
            return conversation_state
            
        except Exception as e:
            print(f"Error loading conversation state: {e}")
            return None
    
    def load_roadmap(self, db: Session, session_id: str) -> Optional[Roadmap]:
        """Load roadmap for a session"""
        try:
            # Get conversation
            db_conversation = db.query(Conversation).filter(
                Conversation.session_id == session_id
            ).first()
            
            if not db_conversation:
                return None
            
            # Get roadmap
            db_roadmap = db.query(RoadmapDB).filter(
                RoadmapDB.conversation_id == db_conversation.id
            ).first()
            
            if db_roadmap and db_roadmap.roadmap_data:
                return Roadmap(**db_roadmap.roadmap_data)
            
            return None
            
        except Exception as e:
            print(f"Error loading roadmap: {e}")
            return None
    
    def delete_conversation(self, db: Session, session_id: str) -> bool:
        """Delete conversation and all associated data"""
        try:
            # Get conversation
            db_conversation = db.query(Conversation).filter(
                Conversation.session_id == session_id
            ).first()
            
            if not db_conversation:
                return False
            
            # Delete messages
            db.query(Message).filter(
                Message.conversation_id == db_conversation.id
            ).delete()
            
            # Delete roadmap
            db.query(RoadmapDB).filter(
                RoadmapDB.conversation_id == db_conversation.id
            ).delete()
            
            # Delete conversation
            db.delete(db_conversation)
            
            db.commit()
            return True
            
        except Exception as e:
            db.rollback()
            print(f"Error deleting conversation: {e}")
            return False
    
    def get_user_conversations(self, db: Session, user_id: int) -> list:
        """Get all conversations for a user"""
        try:
            conversations = db.query(Conversation).filter(
                Conversation.user_id == user_id
            ).order_by(Conversation.updated_at.desc()).all()
            
            return [
                {
                    "session_id": conv.session_id,
                    "project_name": conv.project_name,
                    "phase": conv.current_phase,
                    "created_at": conv.created_at.isoformat(),
                    "updated_at": conv.updated_at.isoformat()
                }
                for conv in conversations
            ]
            
        except Exception as e:
            print(f"Error getting user conversations: {e}")
            return []
    
    def get_user_roadmaps(self, db: Session, user_id: int) -> list:
        """Get all roadmaps for a user"""
        try:
            roadmaps = db.query(RoadmapDB).filter(
                RoadmapDB.user_id == user_id
            ).order_by(RoadmapDB.updated_at.desc()).all()
            
            return [
                {
                    "id": roadmap.id,
                    "conversation_id": roadmap.conversation_id,
                    "roadmap_data": roadmap.roadmap_data,
                    "created_at": roadmap.created_at.isoformat(),
                    "updated_at": roadmap.updated_at.isoformat()
                }
                for roadmap in roadmaps
            ]
            
        except Exception as e:
            print(f"Error getting user roadmaps: {e}")
            return []
