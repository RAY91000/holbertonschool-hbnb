import pytest
from app import create_app
from app.services.facade import HBnBFacade

@pytest.fixture(scope='session')
def app():
    app = create_app(config_class="config.TestingConfig")
    return app

@pytest.fixture(scope='session')
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
    response = client.post('/api/v1/users/', json=user_data)
    user_id = response.get_json().get("id")
    response = client.post('/api/v1/auth/login', json={
        "email": "test.user@example.com",
        "password": "testpassword"
    })
    token = response.get_json().get("access_token")
    return {"Authorization": f"Bearer {token}", "user_id": user_id}

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

@pytest.fixture
def create_place(client, auth_header):
    def _create_place(title, description, price, latitude, longitude, owner_id, amenities=None):
        if amenities is None:
            amenities = ["wifi", "pool"]
        payload = {
            "title": title,
            "description": description,
            "price": price,
            "latitude": latitude,
            "longitude": longitude,
            "amenities": amenities,
        }
        response = client.post('/api/v1/places/', json=payload, headers={"Authorization": auth_header["Authorization"]})
        return response.get_json().get('id') if response.status_code == 201 else None
    return _create_place

def test_create_place(client, auth_header):
    # Utiliser l'utilisateur déjà créé dans auth_header pour la création de la place
    response = client.post('/api/v1/places/', json={
        "title": "Beautiful Apartment",
        "description": "A nice place near the beach",
        "price": 120.5,
        "latitude": 48.8566,
        "longitude": 2.3522,
        "amenities": ["wifi", "pool"]
    }, headers={"Authorization": auth_header["Authorization"]})
    assert response.status_code == 201
    data = response.get_json()
    assert "id" in data
    assert data["title"] == "Beautiful Apartment"
    # L'owner_id doit correspondre à l'ID de l'utilisateur authentifié (celui de auth_header)
    assert data["owner_id"] == auth_header["user_id"]
