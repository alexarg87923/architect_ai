from fastapi.testclient import TestClient
from app.main import app
from app.models.roadmap import Roadmap, RoadmapNode

client = TestClient(app)

def test_generate_roadmap():
    response = client.post("/api/roadmap/generate", json={"project_name": "Test Project", "specifications": "Sample specifications"})
    assert response.status_code == 200
    data = response.json()
    assert "roadmap" in data
    assert isinstance(data["roadmap"], list)

def test_expand_roadmap_node():
    response = client.post("/api/roadmap/expand", json={"node_id": 1, "details": "Expand this node"})
    assert response.status_code == 200
    data = response.json()
    assert "updated_node" in data
    assert data["updated_node"]["id"] == 1
    assert "details" in data["updated_node"]

def test_edit_roadmap_node():
    response = client.put("/api/roadmap/edit", json={"node_id": 1, "new_content": "Updated content"})
    assert response.status_code == 200
    data = response.json()
    assert "updated_node" in data
    assert data["updated_node"]["content"] == "Updated content"

def test_roadmap_structure():
    roadmap = Roadmap(project_name="Test Project", nodes=[RoadmapNode(id=1, content="Node 1")])
    assert roadmap.project_name == "Test Project"
    assert len(roadmap.nodes) == 1
    assert roadmap.nodes[0].content == "Node 1"