from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_gather_project_specifications():
    response = client.post("/api/agent/specifications", json={"project_name": "Test Project", "details": "This is a test project."})
    assert response.status_code == 200
    assert "roadmap" in response.json()

def test_generate_roadmap():
    response = client.post("/api/agent/generate_roadmap", json={"project_name": "Test Project"})
    assert response.status_code == 200
    assert "roadmap" in response.json()

def test_expand_roadmap_node():
    response = client.post("/api/agent/expand_node", json={"node_id": 1, "details": "Expand this node."})
    assert response.status_code == 200
    assert "updated_node" in response.json()

def test_edit_roadmap_node():
    response = client.post("/api/agent/edit_node", json={"node_id": 1, "new_details": "Updated node details."})
    assert response.status_code == 200
    assert "updated_node" in response.json()