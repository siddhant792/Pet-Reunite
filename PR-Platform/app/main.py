"""
Main Module
"""

from http import HTTPStatus
from flask import request
from flask.views import MethodView
from marshmallow import ValidationError

from app.serializers import ContactUsSchema, LastSeenLostPetSchema, LostPetSearchRequestSchema, RegisterPetSchema, ReportFoundPetSchema, UserLoginSchema, UserRegistrationSchema
from app.utils import custom_response, email_exists, fetch_dog_breeds, fetch_lost_pet_search_result, generate_unique_id, login_user, record_contact_us_query, record_found_pet, register_pet, register_user, update_pet_last_seen


class RegisterView(MethodView):
    """
    Class to register a user
    """

    def post(self) -> tuple:
        request_data = request.get_json()
        try:
            validated_data = UserRegistrationSchema().load(request_data)
        except ValidationError as e:
            return custom_response(message="Invalid Payload", error=e.messages, status_code=HTTPStatus.BAD_REQUEST)

        if email_exists(validated_data["email"]):
            return custom_response(message="User with this email is already registered", status_code=HTTPStatus.BAD_REQUEST)

        data = register_user(validated_data)
        return custom_response(message="User registered successfully", data=data)


class LoginView(MethodView):
    """
    Class to login a user
    """

    def post(self) -> tuple:
        request_data = request.get_json()
        try:
            validated_data = UserLoginSchema().load(request_data)
        except ValidationError as e:
            return custom_response(message="Invalid Payload", error=e.messages, status_code=HTTPStatus.BAD_REQUEST)

        return login_user(validated_data)


class ContactUsView(MethodView):
    """
    Class to record contact us queries
    """

    def post(self) -> tuple:
        request_data = request.get_json()
        try:
            validated_data = ContactUsSchema().load(request_data)
        except ValidationError as e:
            return custom_response(message="Invalid Payload", error=e.messages, status_code=HTTPStatus.BAD_REQUEST)

        record_contact_us_query(validated_data)
        return custom_response(message="We will get back to you")


class GetRegisterPetDetailsView(MethodView):
    """
    Class to get the details required to register a pet
    """

    def get(self) -> tuple:
        data = {
            "dog_breeds": fetch_dog_breeds(),
            "pet_unique_id": generate_unique_id(10)
        }
        return custom_response(data=data, message="OK")


class RegisterPetView(MethodView):
    """
    Class to register a pet
    """

    def post(self) -> tuple:
        request_data = request.get_json()
        try:
            validated_data = RegisterPetSchema().load(request_data)
        except ValidationError as e:
            return custom_response(message="Invalid Payload", error=e.messages, status_code=HTTPStatus.BAD_REQUEST)

        return custom_response(data=register_pet(validated_data), message="Your pet has been registered successfully")


class LastSeenLostPetView(MethodView):
    """
    Class to update the last seen of a pet if it is lost
    """

    def post(self) -> tuple:
        request_data = request.get_json()
        try:
            validated_data = LastSeenLostPetSchema().load(request_data)
        except ValidationError as e:
            return custom_response(message="Invalid Payload", error=e.messages, status_code=HTTPStatus.BAD_REQUEST)

        return custom_response(data=update_pet_last_seen(validated_data), message="Last seen recorded successfully")


class ReportFoundPetView(MethodView):
    """
    Class to record a found pet details
    """

    def post(self) -> tuple:
        request_data = request.get_json()
        try:
            validated_data = ReportFoundPetSchema().load(request_data)
        except (ValidationError, ValueError) as e:
            return custom_response(message="Invalid Payload", error=str(e), status_code=HTTPStatus.BAD_REQUEST)

        return custom_response(data=record_found_pet(validated_data), message="Found pet recorded successfully")


class GetPaginatedLostPetsSearchResults(MethodView):
    """
    Class to fetch paginated list of Lost pets based on search
    """

    def get(self) -> tuple:
        request_data = request.get_json()
        try:
            validated_data = LostPetSearchRequestSchema().load(request_data)
        except ValidationError as e:
            return custom_response(message="Invalid Payload", error=e.messages, status_code=HTTPStatus.BAD_REQUEST)

        return custom_response(data=fetch_lost_pet_search_result(validated_data), message="OK")
