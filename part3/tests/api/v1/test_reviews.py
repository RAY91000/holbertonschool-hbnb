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
            "owner_id": owner_id
        }
        response = client.post('/api/v1/places/', json=payload, headers=auth_header)
        return response.get_json().get('id') if response.status_code == 201 else None
    return _create_place

def test_create_review(client, create_user, create_place, auth_header):
    # Create a user and a place (owner of the place will be a different user)
    owner_id = create_user("Owner", "Place", "owner@example.com", password="ownerpass")
    reviewer_id = create_user("Reviewer", "User", "reviewer@example.com", password="reviewpass")
    # Connect as reviewer
    response_login = client.post('/api/v1/auth/login', json={
        "email": "reviewer@example.com",
        "password": "reviewpass"
    })
    reviewer_token = response_login.get_json()["access_token"]
    reviewer_header = {"Authorization": f"Bearer {reviewer_token}"}
    # Create a place with owner_id
    place_id = create_place("Beautiful Apartment", "A nice place near the beach", 120.5, 48.8566, 2.3522, owner_id)
    # Reviewer creates a review
    response = client.post('/api/v1/reviews/', json={
        "text": "Wow amazing!",
        "rating": 5,
        "place_id": place_id
    }, headers=reviewer_header)
    assert response.status_code == 201
    data = response.get_json()
    assert "id" in data
    assert data["text"] == "Wow amazing!"

# Les autres tests de reviews (update, delete) doivent inclure des vérifications d'ownership via auth_header.
