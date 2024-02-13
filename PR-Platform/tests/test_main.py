import unittest
from unittest.mock import patch, Mock
from flask import json
from app import app
from http import HTTPStatus

class TestAPIs(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_register_user_api(self):
        with patch('app.views.register_user') as mock_register_user:
            mock_register_user.return_value = {"user_id": "123", "email": "john@example.com"}
            response = self.app.post('/register', json={"first_name": "John", "last_name": "Doe", "email": "john@example.com", "address": "123 Main St", "password": "password123"})
            self.assertEqual(response.status_code, HTTPStatus.OK)
            data = json.loads(response.data)
            self.assertEqual(data['data'], {"user_id": "123", "email": "john@example.com"})

    def test_login_user_api(self):
        with patch('app.views.login_user') as mock_login_user:
            mock_login_user.return_value = {"user_id": "123", "email": "john@example.com"}
            response = self.app.post('/login', json={"email": "john@example.com", "password": "password123"})
            self.assertEqual(response.status_code, HTTPStatus.OK)
            data = json.loads(response.data)
            self.assertEqual(data['data'], {"user_id": "123", "email": "john@example.com"})

    def test_contact_us_api(self):
        with patch('app.views.record_contact_us_query'):
            response = self.app.post('/contact_us', json={"name": "John Doe", "email": "john@example.com", "message": "Test message"})
            self.assertEqual(response.status_code, HTTPStatus.OK)
            data = json.loads(response.data)
            self.assertEqual(data['message'], "We will get back to you")

    def test_get_register_pet_details_api(self):
        with patch('app.views.fetch_dog_breeds') as mock_fetch_dog_breeds, patch('app.views.generate_unique_id') as mock_generate_unique_id:
            mock_fetch_dog_breeds.return_value = ["Labrador", "Golden Retriever"]
            mock_generate_unique_id.return_value = "abcdef1234"
            response = self.app.get('/register_pet/details')
            self.assertEqual(response.status_code, HTTPStatus.OK)
            data = json.loads(response.data)
            self.assertEqual(data['data'], {"dog_breeds": ["Labrador", "Golden Retriever"], "pet_unique_id": "abcdef1234"})

    def test_register_pet_api(self):
        with patch('app.views.register_pet') as mock_register_pet:
            mock_register_pet.return_value = {"id": "123"}
            response = self.app.post('/register_pet', json={"id": "123", "name": "Buddy", "breed": "Labrador", "color": "Black", "age": 2, "gender": "male", "description": "Friendly dog", "image": "base64_encoded_image", "user_id": "456"})
            self.assertEqual(response.status_code, HTTPStatus.OK)
            data = json.loads(response.data)
            self.assertEqual(data['data'], {"id": "123"})

    def test_last_seen_lost_pet_api(self):
        with patch('app.views.update_pet_last_seen') as mock_update_pet_last_seen:
            mock_update_pet_last_seen.return_value = {"status": "LOST"}
            response = self.app.post('/last_seen_lost_pet', json={"user_id": "123", "pet_id": "456", "address": "TestAddress", "latitude": "1.23", "longitude": "4.56"})
            self.assertEqual(response.status_code, HTTPStatus.OK)
            data = json.loads(response.data)
            self.assertEqual(data['data'], {"status": "LOST"})

    def test_report_found_pet_api(self):
        with patch('app.views.record_found_pet') as mock_record_found_pet:
            mock_record_found_pet.return_value = {"id": "789"}
            response = self.app.post('/report_found_pet', json={"user_id": "123", "breed": "Labrador", "color": "Black", "gender": "male", "description": "Friendly dog", "address": "TestAddress", "latitude": "1.23", "longitude": "4.56", "animal_shelter_id": "789", "shelter_type": "home", "image": "base64_encoded_image"})
            self.assertEqual(response.status_code, HTTPStatus.OK)
            data = json.loads(response.data)
            self.assertEqual(data['data'], {"id": "789"})

    def test_get_lost_pets_search_results_api(self):
        with patch('app.views.fetch_lost_pet_search_result') as mock_fetch_lost_pet_search_result:
            mock_fetch_lost_pet_search_result.return_value = [{"name": "Buddy"}]
            response = self.app.post('/get_lost_pets_search_results', json={"color": "Black", "gender": "male", "breed": "Labrador", "search_address": "TestAddress", "search_latitude": "1.23", "search_longitude": "4.56", "search_radius": 100})
            self.assertEqual(response.status_code, HTTPStatus.OK)
            data = json.loads(response.data)
            self.assertEqual(data['data'], [{"name": "Buddy"}])

    def test_get_found_pets_search_results_api(self):
        with patch('app.views.fetch_found_pet_search_result') as mock_fetch_found_pet_search_result:
            mock_fetch_found_pet_search_result.return_value = [{"name": "Buddy"}]
            response = self.app.post('/get_found_pets_search_results', json={"color": "Black", "gender": "male", "breed": "Labrador", "search_address": "TestAddress", "search_latitude": "1.23", "search_longitude": "4.56", "search_radius": 100})
            self.assertEqual(response.status_code, HTTPStatus.OK)
            data = json.loads(response.data)
            self.assertEqual(data['data'], [{"name": "Buddy"}])

    def test_get_animal_shelter_list_api(self):
        with patch('app.views.fetch_animal_shelters') as mock_fetch_animal_shelters:
            mock_fetch_animal_shelters.return_value = [{"name": "Shelter1"}, {"name": "Shelter2"}]
            response = self.app.get('/get_animal_shelter_list')
            self.assertEqual(response.status_code, HTTPStatus.OK)
            data = json.loads(response.data)
            self.assertEqual(data['data'], [{"name": "Shelter1"}, {"name": "Shelter2"}])

    def test_get_registered_pets_api(self):
        with patch('app.views.fetch_user_pets') as mock_fetch_user_pets:
            mock_fetch_user_pets.return_value = [{"name": "Buddy"}]
            response = self.app.get('/get_registered_pets/123')
            self.assertEqual(response.status_code, HTTPStatus.OK)
            data = json.loads(response.data)
            self.assertEqual(data['data'], [{"name": "Buddy"}])

    def test_update_registered_pet_lost_status_details_api(self):
        with patch('app.views.update_registered_pet_lost_status') as mock_update_registered_pet_lost_status:
            mock_update_registered_pet_lost_status.return_value = {"status": "FOUND"}
            response = self.app.post('/update_registered_pet_lost_status_details', json={"address": "TestAddress", "latitude": "1.23", "longitude": "4.56", "user_id": "123", "pet_id": "456"})
            self.assertEqual(response.status_code, HTTPStatus.OK)
            data = json.loads(response.data)
            self.assertEqual(data['data'], {"status": "FOUND"})

if __name__ == '__main__':
    unittest.main()
