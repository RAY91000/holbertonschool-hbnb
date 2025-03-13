import pytest
from app import create_app

@pytest.fixture
def app():
    app = create_app(config_class="config.TestingConfig")
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_header(client):
    user_data = {
        "first_name": "Test",
        "last_name": "User",
        "email": "test.user@example.com",
        "password": "testpassword"
    }
    client.post('/api/v1/users/', json=user_data)
    response = client.post('/api/v1/auth/login', json={
        "email": "test.user@example.com",
        "password": "testpassword"
    })
    token = response.get_json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def create_user(client):
    def _create_user(first_name, last_name, email, password="secret123"):
        response = client.post('/api/v1/users/', json={
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password
        })
        return response.get_json().get('id') if response.status_code == 201 else None
    return _create_user

def test_create_user(client):
    response = client.post('/api/v1/users/', json={
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane.doe@example.com",
        "password": "janepassword"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert "id" in data
    assert data["first_name"] == "Jane"
    assert data["last_name"] == "Doe"
    assert data["email"] == "jane.doe@example.com"
    assert "password" not in data

def test_update_user(client, create_user, auth_header):
    user_id = create_user("Bob", "Brown", "bob@example.com", password="bobpassword")
    # Connect as this user
    response_login = client.post('/api/v1/auth/login', json={
        "email": "bob@example.com",
        "password": "bobpassword"
    })
    token = response_login.get_json()["access_token"]
    user_header = {"Authorization": f"Bearer {token}"}
    response = client.put(f'/api/v1/users/{user_id}', json={
        "first_name": "Robert",
        "last_name": "Brown",
        "email": "bob@example.com"
    }, headers=user_header)
    assert response.status_code == 200
    data = response.get_json()
    assert data["first_name"] == "Robert"

def test_delete_user(client, create_user, auth_header):
    user_id = create_user("Charlie", "Chaplin", "charlie@example.com", password="charliepass")
    response_login = client.post('/api/v1/auth/login', json={
        "email": "charlie@example.com",
        "password": "charliepass"
    })
    token = response_login.get_json()["access_token"]
    user_header = {"Authorization": f"Bearer {token}"}
    response = client.delete(f'/api/v1/users/{user_id}', headers=user_header)
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "User deleted successfully"
    response = client.get(f'/api/v1/users/{user_id}')
    assert response.status_code == 404

