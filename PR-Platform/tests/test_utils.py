import unittest
from unittest.mock import Mock, patch
from http import HTTPStatus
from datetime import datetime
from app.utils import (
    custom_response,
    email_exists,
    register_user,
    login_user,
    record_contact_us_query,
    fetch_dog_breeds,
    generate_unique_id,
    register_pet,
    update_pet_last_seen,
    predict_dog_breed,
    record_found_pet,
    distance_between_locations_in_km,
    fetch_lost_pet_search_result,
    fetch_found_pet_search_result,
    fetch_animal_shelters,
    fetch_user_pets,
    update_registered_pet_lost_status,
)

class TestUtils(unittest.TestCase):

    def test_custom_response(self):
        response, status_code = custom_response("Test message", {"key": "value"}, {"error_key": "error_value"}, HTTPStatus.OK)
        self.assertEqual(status_code, HTTPStatus.OK)
        self.assertEqual(response.status_code, HTTPStatus.OK)

        data = response.get_json()
        self.assertEqual(data["message"], "Test message")
        self.assertEqual(data["data"], {"key": "value"})
        self.assertEqual(data["error"], {"error_key": "error_value"})

    def test_email_exists(self):
        with patch('app.utils.FS_CLIENT') as mock_firestore:
            mock_firestore.return_value.collection.return_value.where.return_value.limit.return_value.get.return_value = [Mock()]
            result = email_exists("test@example.com")
            self.assertTrue(result)

    def test_register_user(self):
        with patch('app.utils.FS_CLIENT') as mock_firestore:
            mock_user_ref = mock_firestore.return_value.collection.return_value.document.return_value
            result = register_user({"email": "test@example.com", "password": "password"})
            mock_user_ref.set.assert_called_once()
            self.assertIn('_id', result)

    def test_login_user(self):
        with patch('app.utils.FS_CLIENT') as mock_firestore:
            mock_user_ref = Mock()
            mock_user_ref.to_dict.return_value = {"password": "hashed_password"}
            mock_firestore.return_value.collection.return_value.where.return_value.limit.return_value.get.return_value = [mock_user_ref]

            result = login_user({"email": "test@example.com", "password": "password"})
            self.assertEqual(result[1], HTTPStatus.OK)
            self.assertEqual(result[0].get_json()["message"], "Login successful")

    def test_record_contact_us_query(self):
        with patch('app.utils.FS_CLIENT') as mock_firestore:
            mock_ref = mock_firestore.return_value.collection.return_value.document.return_value
            record_contact_us_query({"query": "Test query"})
            mock_ref.set.assert_called_once_with({"query": "Test query"})

    def test_fetch_dog_breeds(self):
        with patch('app.utils.FS_CLIENT') as mock_firestore:
            mock_breed_1 = Mock()
            mock_breed_1.to_dict.return_value = {"name": "Breed1"}
            mock_breed_2 = Mock()
            mock_breed_2.to_dict.return_value = {"name": "Breed2"}
            mock_firestore.return_value.collection.return_value.stream.return_value = [mock_breed_1, mock_breed_2]

            result = fetch_dog_breeds()
            self.assertEqual(result, ["Breed1", "Breed2"])

    def test_generate_unique_id(self):
        result = generate_unique_id(10)
        self.assertEqual(len(result), 10)

    def test_register_pet(self):
        with patch('app.utils.FS_CLIENT') as mock_firestore, \
                patch('app.utils.STORAGE_CLIENT') as mock_storage_client:
            mock_pet_ref = mock_firestore.return_value.document.return_value
            mock_blob = mock_storage_client.return_value.bucket.return_value.blob.return_value
            mock_blob.public_url = "https://example.com/image.jpg"

            result = register_pet({"user_id": "123", "id": "456", "image": "base64_encoded_image"})
            mock_pet_ref.set.assert_called_once()
            mock_blob.upload_from_string.assert_called_once()
            self.assertEqual(result, {"id": "456"})

    def test_update_pet_last_seen(self):
        with patch('app.utils.FS_CLIENT') as mock_firestore:
            mock_pet_ref = mock_firestore.return_value.document.return_value
            validated_data = {"user_id": "123", "pet_id": "456", "address": "TestAddress", "latitude": 1.23, "longitude": 4.56}
            update_pet_last_seen(validated_data)
            mock_pet_ref.set.assert_called_once()

    def test_predict_dog_breed(self):
        with patch('app.utils.requests.get') as mock_requests_get, \
                patch('app.utils.Image.open') as mock_image_open, \
                patch('app.utils.feature_extractor') as mock_feature_extractor, \
                patch('app.utils.model') as mock_model:
            mock_image = mock_image_open.return_value
            mock_requests_get.return_value.content = b"image_content"
            mock_feature_extractor.return_value.return_tensors.return_value = {"input_ids": 123}
            mock_model.return_value.logits = Mock(argmax=Mock(return_value=0))
            mock_model.return_value.config.id2label = {0: "DogBreed"}

            result = predict_dog_breed("https://example.com/image.jpg")
            self.assertEqual(result, "dogbreed")

    def test_record_found_pet(self):
        with patch('app.utils.FS_CLIENT') as mock_firestore, \
                patch('app.utils.STORAGE_CLIENT') as mock_storage_client:
            mock_pet_ref = mock_firestore.return_value.collection.return_value.document.return_value
            mock_blob = mock_storage_client.return_value.bucket.return_value.blob.return_value
            mock_blob.public_url = "https://example.com/image.jpg"

            validated_data = {"user_id": "123", "image": "base64_encoded_image"}
            record_found_pet(validated_data)
            mock_pet_ref.set.assert_called_once()
            mock_blob.upload_from_string.assert_called_once()

    def test_distance_between_locations_in_km(self):
        result = distance_between_locations_in_km(0, 0, 0, 180)
        self.assertAlmostEqual(result, 20015.086796020572, places=2)

    def test_fetch_lost_pet_search_result(self):
        with patch('app.utils.FS_CLIENT') as mock_firestore:
            mock_pet_1 = Mock()
            mock_pet_1.to_dict.return_value = {"status": "LOST", "color": "Black", "breed": "Labrador", "gender": "Male", "user_id": "123"}
            mock_pet_2 = Mock()
            mock_pet_2.to_dict.return_value = {"status": "LOST", "color": "Brown", "breed": "Golden Retriever", "gender": "Female", "user_id": "456"}
            mock_firestore.return_value.collection_group.return_value.where.return_value.order_by.return_value.stream.return_value = [mock_pet_1, mock_pet_2]

            validated_data = {"search_latitude": 0, "search_longitude": 0, "search_radius": 100, "color": "black", "breed": "labrador", "gender": "male"}
            result = fetch_lost_pet_search_result(validated_data)
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0

]["status"], "LOST")

    def test_fetch_found_pet_search_result(self):
        with patch('app.utils.FS_CLIENT') as mock_firestore:
            mock_pet_1 = Mock()
            mock_pet_1.to_dict.return_value = {"color": "Black", "breed": "Labrador", "gender": "Male", "user_id": "123", "shelter_type": "home"}
            mock_pet_2 = Mock()
            mock_pet_2.to_dict.return_value = {"color": "Brown", "breed": "Golden Retriever", "gender": "Female", "user_id": "456", "shelter_type": "shelter"}
            mock_firestore.return_value.collection_group.return_value.stream.return_value = [mock_pet_1, mock_pet_2]

            validated_data = {"search_latitude": 0, "search_longitude": 0, "search_radius": 100, "color": "black", "breed": "labrador", "gender": "male"}
            result = fetch_found_pet_search_result(validated_data)
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]["shelter_type"], "home")

    def test_fetch_animal_shelters(self):
        with patch('app.utils.FS_CLIENT') as mock_firestore:
            mock_shelter_1 = Mock()
            mock_shelter_1.to_dict.return_value = {"coordinates": Mock(latitude=1.23, longitude=4.56), "address": "Shelter1"}
            mock_shelter_2 = Mock()
            mock_shelter_2.to_dict.return_value = {"coordinates": Mock(latitude=7.89, longitude=10.11), "address": "Shelter2"}
            mock_firestore.return_value.collection.return_value.stream.return_value = [mock_shelter_1, mock_shelter_2]

            result = fetch_animal_shelters()
            self.assertEqual(len(result), 2)
            self.assertEqual(result[0]["latitude"], 1.23)
            self.assertEqual(result[1]["address"], "Shelter2")

    def test_fetch_user_pets(self):
        with patch('app.utils.FS_CLIENT') as mock_firestore:
            mock_pet_1 = Mock()
            mock_pet_1.to_dict.return_value = {"name": "Pet1"}
            mock_pet_2 = Mock()
            mock_pet_2.to_dict.return_value = {"name": "Pet2"}
            mock_firestore.return_value.collection.return_value.stream.return_value = [mock_pet_1, mock_pet_2]

            result = fetch_user_pets("123")
            self.assertEqual(len(result), 2)
            self.assertEqual(result[0]["name"], "Pet1")
            self.assertEqual(result[1]["name"], "Pet2")

    def test_update_registered_pet_lost_status(self):
        with patch('app.utils.FS_CLIENT') as mock_firestore:
            mock_pet_ref = mock_firestore.return_value.document.return_value
            validated_data = {"user_id": "123", "pet_id": "456", "address": "TestAddress", "latitude": 1.23, "longitude": 4.56}
            update_registered_pet_lost_status(validated_data)
            mock_pet_ref.set.assert_called_once()

if __name__ == '__main__':
    unittest.main()
