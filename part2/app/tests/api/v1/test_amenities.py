import unittest
from flask_testing import TestCase
from app import create_app
from app.services.facade import HBnBFacade

class TestAmenityEndpoints(TestCase):
    def create_app(self):
        """Initialise l'application Flask en mode test"""
        return create_app(config_name="testing")

    def setUp(self):
        """Configuration avant chaque test"""
        self.client = self.app.test_client()
        self.facade = HBnBFacade()

    def test_create_amenity(self):
        """Test de la création d'un amenity"""
        response = self.client.post('/api/v1/amenities/', json={
            "name": "WiFi",
            "description": "Free high-speed WiFi"
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json)

    def test_get_amenities(self):
        """Test de la récupération de la liste des amenities"""
        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)

    def test_get_non_existent_amenity(self):
        """Test de récupération d'un amenity inexistant"""
        response = self.client.get('/api/v1/amenities/{amenty_id}')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
