from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.api.routes.chat import router as chat_router

app = FastAPI()
app.include_router(chat_router)

client = TestClient(app)

def test_chat_interaction():
    response = client.post("/chat", json={"message": "What is the project about?"})
    assert response.status_code == 200
    assert "response" in response.json()

def test_generate_roadmap():
    response = client.post("/chat/generate_roadmap", json={"specifications": {"goal": "Launch a new product"}})
    assert response.status_code == 200
    assert "roadmap" in response.json()

def test_expand_roadmap_node():
    response = client.post("/chat/expand_node", json={"node_id": 1, "details": "Add more tasks"})
    assert response.status_code == 200
    assert "updated_node" in response.json()

def test_edit_roadmap_node():
    response = client.post("/chat/edit_node", json={"node_id": 1, "new_details": "Update task description"})
    assert response.status_code == 200
    assert "updated_node" in response.json()