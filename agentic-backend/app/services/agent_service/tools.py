"""
Agent tools definitions for the roadmap generation system.
Contains all function calling tools used by the agent service.
"""

# Should be consistent with the tags used in the Project model
PROJECT_TAG_CHOICES = ["setup", "mvp", "frontend", "backend", "auth", "deployment", "testing"]

def get_agent_tools():
    """Define all available tools for the agent"""
    return [
        {
            "type": "function",
            "function": {
                "name": "ask_clarifying_question",
                "description": "Ask a focused question to gather more project information",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "question": {
                            "type": "string",
                            "description": "A concise, focused question about the project"
                        },
                        "category": {
                            "type": "string",
                            "enum": [
                                "project_vision", "core_features", "user_needs", "workflow", 
                                "ui_ux", "data_management", "integrations", "goals", 
                                "timeline", "tech_stack", "experience", "deployment", 
                                "auth", "audience", "commercial", "constraints", "inspiration"
                            ],
                            "description": "What category of information this question is gathering"
                        }
                    },
                    "required": ["question", "category"]
                }
            }
        },
        {
            "type": "function", 
            "function": {
                "name": "confirm_specifications_complete",
                "description": "Confirm that all project specifications have been gathered",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "summary": {
                            "type": "string",
                            "description": "A brief summary of the project specifications gathered"
                        }
                    },
                    "required": ["summary"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "generate_high_level_roadmap",
                "description": "Generate high-level roadmap milestone nodes without detailed subtasks (Step 1 of 3)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "project_title": {"type": "string"},
                        "project_description": {"type": "string"},
                        "nodes": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "string"},
                                    "title": {"type": "string", "maxLength": 60},
                                    "description": {"type": "string", "maxLength": 200},
                                    "estimated_days": {"type": "integer"},
                                    "estimated_hours": {"type": "number"},
                                    "tags": {
                                        "type": "array",
                                        "items": {
                                            "type": "string",
                                            "enum": PROJECT_TAG_CHOICES
                                        }
                                    },
                                    "dependencies": {
                                        "type": "array",
                                        "items": {"type": "string"}
                                    },
                                    "deliverables": {
                                        "type": "array",
                                        "items": {"type": "string"}
                                    },
                                    "success_criteria": {
                                        "type": "array",
                                        "items": {"type": "string"}
                                    }
                                },
                                "required": ["id", "title", "description", "estimated_days", "estimated_hours", "tags"]
                            }
                        }
                    },
                    "required": ["project_title", "project_description", "nodes"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "generate_project_overview",
                "description": "Generate a high-level development strategy overview for the setup node (Step 2 of 3)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "setup_node_id": {
                            "type": "string",
                            "description": "The ID of the setup node to add overview to"
                        },
                        "overview": {
                            "type": "array",
                            "items": {"type": "string"},
                            "minItems": 5,
                            "maxItems": 10,
                            "description": "Step-by-step development strategy showing how the project will be built from setup to deployment"
                        }
                    },
                    "required": ["setup_node_id", "overview"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "generate_node_subtasks",
                "description": "Generate detailed subtasks for specific roadmap nodes (Step 3 of 3)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "node_id": {"type": "string"},
                        "subtasks": {
                            "type": "array",
                            "maxItems": 4,
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "string"},
                                    "title": {"type": "string", "maxLength": 40},
                                    "description": {"type": "string", "maxLength": 60},
                                    "estimated_hours": {"type": "number"}
                                },
                                "required": ["id", "title", "description", "estimated_hours"]
                            }
                        }
                    },
                    "required": ["node_id", "subtasks"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "expand_roadmap_node",
                "description": "Add new roadmap nodes that branch from an existing node to expand project scope. ONLY use this after gathering specific details about what to expand and which node to branch from.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "base_node_id": {
                            "type": "string", 
                            "description": "The ID of the existing node to expand from"
                        },
                        "expansion_reason": {
                            "type": "string",
                            "description": "Why this expansion is needed (e.g., 'add authentication', 'new dashboard feature')"
                        },
                        "new_nodes": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "string"},
                                    "title": {"type": "string"},
                                    "description": {"type": "string"},
                                    "subtasks": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "id": {"type": "string"},
                                                "title": {"type": "string"},
                                                "description": {"type": "string"},
                                                "estimated_hours": {"type": "number"}
                                            },
                                            "required": ["id", "title", "description"]
                                        }
                                    },
                                    "estimated_days": {"type": "integer"},
                                    "estimated_hours": {"type": "number"},
                                    "tags": {
                                        "type": "array",
                                        "items": {
                                            "type": "string",
                                            "enum": PROJECT_TAG_CHOICES
                                        }
                                    },
                                    "dependencies": {
                                        "type": "array",
                                        "items": {"type": "string"}
                                    },
                                    "deliverables": {
                                        "type": "array",
                                        "items": {"type": "string"}
                                    },
                                    "success_criteria": {
                                        "type": "array",
                                        "items": {"type": "string"}
                                    }
                                },
                                "required": ["id", "title", "description", "estimated_days", "estimated_hours", "tags"]
                            }
                        }
                    },
                    "required": ["base_node_id", "expansion_reason", "new_nodes"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "add_subtasks_to_node",
                "description": "Add more detailed subtasks to an existing roadmap node",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "node_id": {"type": "string"},
                        "additional_subtasks": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "string"},
                                    "title": {"type": "string"},
                                    "description": {"type": "string"},
                                    "estimated_hours": {"type": "number"}
                                },
                                "required": ["id", "title", "description"]
                            }
                        },
                        "updated_total_hours": {"type": "number"}
                    },
                    "required": ["node_id", "additional_subtasks"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "edit_roadmap_node", 
                "description": "Modify an existing roadmap node. ONLY use this after gathering specific details about which node to edit and what changes to make.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "node_id": {"type": "string"},
                        "updated_fields": {
                            "type": "object",
                            "properties": {
                                "title": {"type": "string"},
                                "description": {"type": "string"},
                                "estimated_days": {"type": "integer"},
                                "estimated_hours": {"type": "number"},
                                "tags": {"type": "array", "items": {"type": "string"}},
                                "deliverables": {"type": "array", "items": {"type": "string"}},
                                "success_criteria": {"type": "array", "items": {"type": "string"}}
                            }
                        }
                    },
                    "required": ["node_id", "updated_fields"]
                }
            }
        }
    ]
