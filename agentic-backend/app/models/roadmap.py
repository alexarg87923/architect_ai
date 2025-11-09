from pydantic import BaseModel
from typing import List, Optional

class RoadmapNode(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    children: List['RoadmapNode'] = []

class Roadmap(BaseModel):
    id: str
    title: str
    nodes: List[RoadmapNode]

# Forward declaration for type hinting
RoadmapNode.update_forward_refs()