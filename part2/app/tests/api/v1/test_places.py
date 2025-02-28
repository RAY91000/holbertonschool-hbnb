import unittest
from flask_testing import TestCase
from app import create_app
from app.services.facade import HBnBFacade

class TestPlaceEndpoints(TestCase):
    def create_app(self):
        return create_app(config_name="testing")

    def setUp(self):
        self.client = self.app.test_client()
        self.facade = HBnBFacade()

    def test_create_place(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Beautiful Apartment",
            "description": "A nice place near the beach",
            "price": 120.5,
            "latitude": 48.8566,
            "longitude": 2.3522,
            "owner_id": "user123",
            "amenities": ["wifi", "pool"]
        })
        self.assertEqual(response.status_code, 201)

    def test_get_places(self):
        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)

    def test_get_place_not_found(self):
        response = self.client.get('/api/v1/places/999')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
