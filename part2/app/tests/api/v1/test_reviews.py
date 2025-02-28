import unittest
from app import create_app
from app.services.facade import HBnBFacade

class TestReviewEndpoints(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        
        cls.app = create_app()
        cls.client = cls.app.test_client()

    def test_create_review(self):
        
        response = self.client.post('/api/v1/reviews/', json={
            "comment": "Waow amazing!",
            "rating": 5,
            "user_id": "689987644",
            "place_id": "76543468"
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json)
        self.assertEqual(response.json["comment"], "Waow amazing!")

    def test_create_review_invalid_data(self):
        
        response = self.client.post('/api/v1/reviews/', json={
            "comment": 5,
            "rating": "Nice!",
            "user_id": "",
            "place_id": ""
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json)

    def test_get_all_reviews(self):
        """Test de la récupération de toutes les reviews"""
        response = self.client.get('/api/v1/reviews/')
        self.assertIn(response.status_code, [200, 404])

    def test_get_review_by_id(self):
        """Test de la récupération d'une review spécifique"""
        review_id = "review1"
        response = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertIn(response.status_code, [200, 404])
        if response.status_code == 200:
            self.assertIn("id", response.json)

    def test_update_review(self):
        """Test de la mise à jour d'une review existante"""
        review_id = "review1"
        response = self.client.put(f'/api/v1/reviews/{review_id}', json={
            "comment": "Awesome",
            "rating": 4
        })
        self.assertIn(response.status_code, [200, 404])
        if response.status_code == 200:
            self.assertEqual(response.json["comment"], "Awesome")
            self.assertEqual(response.json["rating"], 4)

    def test_delete_review(self):
        """Test de la suppression d'une review"""
        review_id = "review2"
        response = self.client.delete(f'/api/v1/reviews/{review_id}')
        self.assertIn(response.status_code, [200, 404])
        if response.status_code == 200:
            self.assertEqual(response.json["message"], "Review deleted successfully")

if __name__ == "__main__":
    unittest.main()
