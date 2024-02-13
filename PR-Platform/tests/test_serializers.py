import unittest
from datetime import datetime
from decimal import Decimal
from marshmallow import ValidationError
from app.serializers import (
    UserRegistrationSchema,
    UserLoginSchema,
    ContactUsSchema,
    RegisterPetSchema,
    LastSeenLostPetSchema,
    ReportFoundPetSchema,
    LostPetSearchRequestSchema,
    UpdateLostPetSchema,
)

class TestSerializers(unittest.TestCase):

    def test_user_registration_schema(self):
        data = {"first_name": "John", "last_name": "Doe", "email": "john@example.com", "address": "123 Main St", "password": "password123"}
        schema = UserRegistrationSchema()
        result = schema.load(data)
        self.assertEqual(result, data)

    def test_user_login_schema(self):
        data = {"email": "john@example.com", "password": "password123"}
        schema = UserLoginSchema()
        result = schema.load(data)
        self.assertEqual(result, data)

    def test_contact_us_schema(self):
        data = {"name": "John Doe", "email": "john@example.com", "message": "Test message"}
        schema = ContactUsSchema()
        result = schema.load(data)
        self.assertEqual(result["name"], "John Doe")
        self.assertEqual(result["email"], "john@example.com")
        self.assertEqual(result["message"], "Test message")
        self.assertIsInstance(result["timestamp"], datetime)

    def test_register_pet_schema(self):
        data = {"id": "123", "name": "Buddy", "breed": "Labrador", "color": "Black", "age": 2, "gender": "male", "description": "Friendly dog", "image": "base64_encoded_image", "user_id": "456"}
        schema = RegisterPetSchema()
        result = schema.load(data)
        self.assertEqual(result, data)

    def test_last_seen_lost_pet_schema(self):
        data = {"user_id": "123", "pet_id": "456", "address": "TestAddress", "latitude": "1.23", "longitude": "4.56"}
        schema = LastSeenLostPetSchema()
        result = schema.load(data)
        self.assertEqual(result["latitude"], Decimal("1.23"))
        self.assertEqual(result["longitude"], Decimal("4.56"))

    def test_report_found_pet_schema(self):
        data = {"user_id": "123", "breed": "Labrador", "color": "Black", "gender": "male", "description": "Friendly dog", "address": "TestAddress", "latitude": "1.23", "longitude": "4.56", "animal_shelter_id": "789", "shelter_type": "home", "image": "base64_encoded_image"}
        schema = ReportFoundPetSchema()
        result = schema.load(data)
        self.assertEqual(result["latitude"], Decimal("1.23"))
        self.assertEqual(result["longitude"], Decimal("4.56"))
        self.assertEqual(result["breed"], "labrador")

    def test_lost_pet_search_request_schema(self):
        data = {"color": "Black", "gender": "male", "breed": "Labrador", "search_address": "TestAddress", "search_latitude": "1.23", "search_longitude": "4.56", "search_radius": 100}
        schema = LostPetSearchRequestSchema()
        result = schema.load(data)
        self.assertEqual(result["search_latitude"], Decimal("1.23"))
        self.assertEqual(result["search_longitude"], Decimal("4.56"))

    def test_update_lost_pet_schema(self):
        data = {"address": "TestAddress", "latitude": "1.23", "longitude": "4.56", "user_id": "123", "pet_id": "456"}
        schema = UpdateLostPetSchema()
        result = schema.load(data)
        self.assertEqual(result["latitude"], Decimal("1.23"))
        self.assertEqual(result["longitude"], Decimal("4.56"))

    def test_report_found_pet_schema_validate_shelter_type(self):
        schema = ReportFoundPetSchema()
        data_home = {"shelter_type": "home", "address": "TestAddress", "latitude": "1.23", "longitude": "4.56"}
        data_animal_shelter = {"shelter_type": "animal_shelter", "animal_shelter_id": "789"}
        with self.subTest(data=data_home):
            result = schema.load(data_home)
            self.assertEqual(result["shelter_type"], "home")

        with self.subTest(data=data_animal_shelter):
            result = schema.load(data_animal_shelter)
            self.assertEqual(result["shelter_type"], "animal_shelter")

        data_invalid = {"shelter_type": "invalid_type"}
        with self.subTest(data=data_invalid):
            with self.assertRaises(ValidationError):
                schema.load(data_invalid)

    def test_report_found_pet_schema_convert_coordinates(self):
        schema = ReportFoundPetSchema()
        data = {"latitude": "1.23", "longitude": "4.56"}
        result = schema.load(data)
        self.assertEqual(result["latitude"], Decimal("1.23"))
        self.assertEqual(result["longitude"], Decimal("4.56"))

if __name__ == '__main__':
    unittest.main()
