# Roadmap AI - Design Documentation

## Overview

**Roadmap AI** is an interactive AI product manager for personal software engineering projects. It serves as a smart assistant that helps developers plan, organize, and stay accountable for their projects by generating visual roadmaps and providing ongoing project guidance.

### Core Value Proposition
- **AI Product Manager**: Acts as a personal PM that understands your project vision
- **Visual Roadmap Generation**: Creates interactive roadmaps using ReactFlow library
- **Accountability Partner**: Keeps developers on track with their project goals
- **Adaptive Planning**: Allows roadmap expansion and editing as projects evolve

## Product Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   External      │
│  (React/Vite)   │    │  (FastAPI)      │    │   Services      │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ • ReactFlow     │◄──►│ • Agent Service │◄──►│ • OpenAI GPT    │
│ • Chat UI       │    │ • Database      │    │ • GROQ Llama    │
│ • Roadmap Viz   │    │ • API Routes    │    │ • PostgreSQL    │
│ • State Mgmt    │    │ • Session Mgmt  │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## AI Product Manager Phases

The AI follows a structured approach to understand user projects and generate actionable roadmaps:

### 1. Discovery Phase (8-15 rounds)
**Goal**: Gather comprehensive project requirements through intelligent questioning

**Process**:
- Initial project description from user
- AI asks targeted clarifying questions across categories:
  - **Core Features**: What functionality should the project have?
  - **User Needs**: Who is the target audience and their pain points?
  - **Tech Stack**: Preferred technologies and technical requirements
  - **Timeline**: Project deadlines and milestones
  - **Auth/Security**: Authentication and security requirements
  - **Integrations**: Third-party services and APIs needed
  - **Workflow**: User experience and interaction flows

**Example Questions**:
- "What specific pain points does your project solve?"
- "How do you envision users interacting with the main features?"
- "What's your timeline and are there any hard deadlines?"

**Completion Criteria**: 
- Minimum 8 meaningful question-answer exchanges
- Comprehensive coverage of project aspects
- User confirms specifications are complete

### 2. Confirmation Phase
**Goal**: Validate and summarize gathered requirements

**Process**:
- AI presents comprehensive project summary
- Includes: goals, features, tech stack, timeline, user experience
- User confirms or requests modifications
- Specifications marked as complete when confirmed

**Output**: ProjectSpecification object with all validated requirements

### 3. Generation Phase
**Goal**: Create initial visual roadmap with milestone nodes

**Process**:
- AI analyzes confirmed specifications
- Generates 4-8 high-level milestone nodes
- Each node includes:
  - Detailed descriptions and success criteria
  - Time estimates (days/hours)
  - Dependencies between nodes
  - Deliverables and subtasks
  - Technology tags

**Roadmap Structure**:
```
Setup/Planning → Design → Development → Testing → Deployment
     ↓              ↓           ↓          ↓         ↓
  Research      Wireframes   Frontend   QA Tests   Production
  Timeline      Prototypes   Backend    Bug Fixes  Monitoring
```

### 4. Editing Phase (Ongoing)
**Goal**: Refine and adapt roadmap as project evolves

**Capabilities**:
- **Expand Nodes**: Add new features or scope to existing roadmap
- **Edit Nodes**: Modify descriptions, timelines, or requirements
- **Add Subtasks**: Break down nodes into detailed actionable items
- **Update Dependencies**: Adjust project flow and dependencies

## Supported Actions

### Core Function Calls

| Function | Purpose | Phase | Parameters |
|----------|---------|-------|------------|
| `ask_clarifying_question` | Gather project requirements | Discovery | `category`, `question` |
| `confirm_specifications_complete` | Validate requirements | Confirmation | `summary` |
| `generate_project_roadmap` | Create initial roadmap | Generation | `project_title`, `description`, `nodes[]` |
| `expand_roadmap_scope` | Add new features/scope | Editing | `new_nodes[]`, `rationale` |
| `edit_existing_node` | Modify roadmap nodes | Editing | `node_id`, `updates` |
| `add_subtasks_to_node` | Break down nodes | Editing | `node_id`, `subtasks[]` |

### Action Types

#### 1. Chat Mode (Default)
- **Purpose**: General conversation and discovery
- **Available Functions**: `ask_clarifying_question`, `confirm_specifications_complete`, `generate_project_roadmap`
- **Use Cases**: Initial project discussion, requirement gathering, roadmap generation

#### 2. Expand Mode
- **Purpose**: Add new features or scope to existing roadmap
- **Available Functions**: `ask_clarifying_question`, `expand_roadmap_scope`, `add_subtasks_to_node`
- **Use Cases**: "I want to add a mobile app", "Let's include user analytics"

#### 3. Edit Mode  
- **Purpose**: Modify existing roadmap elements
- **Available Functions**: `ask_clarifying_question`, `edit_existing_node`, `add_subtasks_to_node`
- **Use Cases**: "Change the authentication system", "Update the timeline"

## Data Models

### ConversationState
```python
class ConversationState(BaseModel):
    session_id: str
    phase: str  # "discovery" | "confirmation" | "generation" | "editing"
    messages: List[ChatMessage]
    specifications_complete: bool = False
    current_roadmap: Optional[ProjectRoadmap] = None
    project_specification: Optional[ProjectSpecification] = None
```

### ProjectRoadmap
```python
class ProjectRoadmap(BaseModel):
    project_specification: ProjectSpecification
    nodes: List[RoadmapNode]
    total_estimated_weeks: int
    total_estimated_hours: float
```

### RoadmapNode
```python
class RoadmapNode(BaseModel):
    id: str
    title: str
    description: str
    subtasks: List[SubTask]
    estimated_days: int
    estimated_hours: float
    tags: List[str]
    dependencies: List[str]
    status: str = "pending"
    deliverables: List[str]
    success_criteria: List[str]
```

## Frontend Architecture (MVP Scope)

### Core Components

#### 1. Layout Structure
```
┌─────────────────────────────────────────────────────────┐
│ TopNavbar (Brand, Session Info, Settings)              │
├─────────────┬───────────────────────────────────────────┤
│ Sidebar     │ MainContent                               │
│ • Chat      │ ┌─────────────────────────────────────┐   │
│ • Roadmap   │ │ Chat Interface                      │   │
│ • Settings  │ │ • Message History                   │   │
│             │ │ • Input Field                       │   │
│             │ │ • Action Mode Selector              │   │
│             │ └─────────────────────────────────────┘   │
│             │ ┌─────────────────────────────────────┐   │
│             │ │ Roadmap Visualization (ReactFlow)  │   │
│             │ │ • Interactive Node Graph           │   │
│             │ │ • Progress Tracking                 │   │
│             │ │ • Node Details Panel                │   │
│             │ └─────────────────────────────────────┘   │
└─────────────┴───────────────────────────────────────────┘
```

#### 2. Chat Interface
- **Message History**: Conversation between user and AI product manager
- **Input Field**: Text area for user messages and project descriptions
- **Action Mode Selector**: Toggle between Chat/Expand/Edit modes
- **Phase Indicator**: Shows current phase (Discovery/Confirmation/Generation/Editing)

#### 3. Roadmap Visualization (ReactFlow)
- **Interactive Nodes**: Visual representation of project milestones
- **Dependency Arrows**: Show relationships between nodes
- **Progress Indicators**: Visual progress tracking per node
- **Node Details**: Expandable details with subtasks and timelines
- **Zoom/Pan**: Navigate large roadmaps efficiently

### State Management
```javascript
// Core Application State
const AppState = {
  // Session Management
  sessionId: string,
  isLoading: boolean,
  
  // Conversation State  
  conversationState: ConversationState,
  messages: ChatMessage[],
  currentPhase: string,
  
  // Roadmap State
  currentRoadmap: ProjectRoadmap | null,
  selectedNode: RoadmapNode | null,
  
  // UI State
  actionMode: 'chat' | 'expand' | 'edit',
  sidebarView: 'chat' | 'roadmap' | 'settings'
};
```

## Technical Implementation

### Backend Architecture
- **Framework**: FastAPI with async support
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Session Management**: UUID-based session tracking
- **API Design**: RESTful endpoints with structured responses

### LLM Integration
- **Primary**: OpenAI GPT-4 for reliable function calling
- **Secondary**: GROQ Llama with fallback text parsing
- **Function Calling**: Structured tool use for consistent responses
- **Context Management**: Conversation history with context window optimization

### Database Schema
```sql
-- Sessions table for conversation tracking
CREATE TABLE sessions (
    id UUID PRIMARY KEY,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    phase VARCHAR(50),
    specifications_complete BOOLEAN
);

-- Messages table for conversation history  
CREATE TABLE messages (
    id UUID PRIMARY KEY,
    session_id UUID REFERENCES sessions(id),
    role VARCHAR(20),
    content TEXT,
    timestamp TIMESTAMP
);

-- Roadmaps table for generated project plans
CREATE TABLE roadmaps (
    id UUID PRIMARY KEY,
    session_id UUID REFERENCES sessions(id),
    project_title VARCHAR(255),
    project_description TEXT,
    total_estimated_weeks INTEGER,
    total_estimated_hours FLOAT,
    created_at TIMESTAMP
);

-- Nodes table for roadmap milestones
CREATE TABLE nodes (
    id UUID PRIMARY KEY,
    roadmap_id UUID REFERENCES roadmaps(id),
    title VARCHAR(255),
    description TEXT,
    estimated_days INTEGER,
    estimated_hours FLOAT,
    status VARCHAR(50),
    dependencies JSONB,
    deliverables JSONB,
    success_criteria JSONB
);
```

## API Endpoints

### Agent Endpoints (Core)
```
POST /api/agent/chat              # Main conversation endpoint
GET  /api/agent/conversation/{id} # Retrieve conversation state  
GET  /api/agent/roadmap/{id}      # Get generated roadmap
DELETE /api/agent/conversation/{id} # Clear conversation
GET  /api/agent/health            # Service health check
```

### Request/Response Format
```javascript
// Chat Request
{
  "message": "I want to build a task management app",
  "session_id": "optional-session-id", 
  "action_type": "chat|expand|edit",
  "conversation_state": "optional-state-object"
}

// Chat Response
{
  "agent_response": "What specific features...",
  "conversation_state": {...},
  "session_id": "uuid",
  "action_button": "generate_roadmap|null",
  "phase": "discovery"
}
```

## MVP Feature Scope

### ✅ Implemented Features
1. **Interactive AI Product Manager**: Multi-phase conversation system
2. **Roadmap Generation**: Automated creation of milestone-based project plans
3. **Roadmap Editing**: Expand and modify existing roadmaps
4. **Session Persistence**: Database-backed conversation and roadmap storage
5. **Multi-LLM Support**: OpenAI and GROQ integration with fallbacks

### 🚧 Current Limitations
1. **No ReactFlow Frontend**: Roadmap visualization not yet implemented
2. **No User Authentication**: Single-session usage only
3. **No Project Templates**: Each roadmap generated from scratch
4. **No Progress Tracking**: Cannot mark nodes/subtasks as complete
5. **No Export Features**: Cannot export roadmaps to external formats

### 🎯 Immediate Next Steps
1. **Implement ReactFlow Visualization**: Interactive roadmap display
2. **Build Chat Interface**: Real-time conversation UI
3. **Add Session Management**: Frontend session persistence
4. **Create Node Interaction**: Click to expand, edit, and modify nodes
5. **Add Progress Indicators**: Visual completion tracking

## Quality Metrics

### Performance Targets
- **Response Time**: <10 seconds for roadmap generation
- **Session Persistence**: 99.9% data retention
- **LLM Reliability**: <5% function calling failures

### User Experience Goals
- **Discovery Efficiency**: 8-15 questions to complete specifications
- **Roadmap Actionability**: 4-8 concrete milestone nodes
- **Conversation Flow**: Natural, PM-like interactions
- **Visual Clarity**: Intuitive roadmap navigation with ReactFlow

---

*This document reflects the current state of Roadmap AI MVP, focused on providing an interactive AI product manager that generates visual project roadmaps for software engineering projects.*