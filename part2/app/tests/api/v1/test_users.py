import unittest
from app import create_app
from app.services.facade import HBnBFacade

class TestUserEndpoints(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        
        cls.app = create_app()
        cls.client = cls.app.test_client()

    def create_user(self, first_name, last_name, email, password):
        
        response = self.client.post('/api/v1/users/', json={
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password,
            "place_list": []
        })
        return response.get_json().get('id') if response.status_code == 201 else None

    def test_create_user(self):
        
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com",
            "password": "securepassword",
            "place_list": []
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn("id", data)
        self.assertDictContainsSubset({
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com",
            "place_list": []
        }, data)

    def test_create_user_invalid_data(self):
        
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "",
            "email": "invalid-email",
            "password": "",
            "place_list": []
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())

    def test_create_user_duplicate_email(self):
        
        email = "john.doe@example.com"
        self.create_user("John", "Doe", email, "securepassword")

        response = self.client.post('/api/v1/users/', json={
            "first_name": "Johnny",
            "last_name": "Doe",
            "email": email,
            "password": "anotherpassword",
            "place_list": []
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())

    def test_get_all_users(self):
        
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)

    def test_get_user_by_id(self):
        
        user_id = self.create_user("Alice", "Smith", "alice@example.com", "securepassword")
        response = self.client.get(f'/api/v1/users/{user_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["email"], "alice@example.com")

    def test_get_user_not_found(self):
        
        response = self.client.get('/api/v1/users/99999')
        self.assertEqual(response.status_code, 404)

    def test_update_user(self):
        
        user_id = self.create_user("Bob", "Brown", "bob@example.com", "securepassword")
        response = self.client.put(f'/api/v1/users/{user_id}', json={
            "first_name": "Robert",
            "last_name": "Brown",
            "email": "bob@example.com",
            "password": "securepassword",
            "place_list": []
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["first_name"], "Robert")

    def test_update_user_not_found(self):
        
        response = self.client.put('/api/v1/users/99999', json={
            "first_name": "Unknown",
            "last_name": "User",
            "email": "unknown@example.com",
            "password": "securepassword",
            "place_list": []
        })
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()
