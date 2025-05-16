import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_add_message(client):
    response = client.post('/message', json={"text": "Test message"})
    assert response.status_code == 201
    assert response.json == {"status": "Message added"}

def test_add_message_missing_text(client):
    response = client.post('/message', json={})
    assert response.status_code == 400
    assert response.json == {"error": "Text required"}

def test_get_messages(client):
    response = client.get('/messages')
    assert response.status_code == 200
    assert isinstance(response.json, list)