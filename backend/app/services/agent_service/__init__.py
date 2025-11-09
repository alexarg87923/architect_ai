"""
Agent service package for handling project roadmap conversations.
"""

from .orchestrator import AgentOrchestrator

# Export the main class for backwards compatibility
AgentService = AgentOrchestrator
