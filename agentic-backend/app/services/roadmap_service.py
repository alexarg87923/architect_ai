from typing import List, Dict, Optional
from pydantic import BaseModel
import uuid

class RoadmapNode(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    children: List['RoadmapNode'] = []

class Roadmap(BaseModel):
    id: str
    title: str
    nodes: List[RoadmapNode]

class RoadmapService:
    def __init__(self):
        self.roadmaps: Dict[str, Roadmap] = {}

    def generate_roadmap(self, title: str) -> Roadmap:
        roadmap_id = str(uuid.uuid4())
        roadmap = Roadmap(id=roadmap_id, title=title, nodes=[])
        self.roadmaps[roadmap_id] = roadmap
        return roadmap

    def add_node(self, roadmap_id: str, title: str, description: Optional[str] = None, parent_id: Optional[str] = None) -> RoadmapNode:
        if roadmap_id not in self.roadmaps:
            raise ValueError("Roadmap not found")

        node_id = str(uuid.uuid4())
        new_node = RoadmapNode(id=node_id, title=title, description=description)

        if parent_id:
            parent_node = self.find_node(self.roadmaps[roadmap_id].nodes, parent_id)
            if parent_node:
                parent_node.children.append(new_node)
            else:
                raise ValueError("Parent node not found")
        else:
            self.roadmaps[roadmap_id].nodes.append(new_node)

        return new_node

    def find_node(self, nodes: List[RoadmapNode], node_id: str) -> Optional[RoadmapNode]:
        for node in nodes:
            if node.id == node_id:
                return node
            found_node = self.find_node(node.children, node_id)
            if found_node:
                return found_node
        return None

    def edit_node(self, roadmap_id: str, node_id: str, title: Optional[str] = None, description: Optional[str] = None) -> RoadmapNode:
        if roadmap_id not in self.roadmaps:
            raise ValueError("Roadmap not found")

        node = self.find_node(self.roadmaps[roadmap_id].nodes, node_id)
        if not node:
            raise ValueError("Node not found")

        if title:
            node.title = title
        if description:
            node.description = description

        return node

    def get_roadmap(self, roadmap_id: str) -> Optional[Roadmap]:
        return self.roadmaps.get(roadmap_id)