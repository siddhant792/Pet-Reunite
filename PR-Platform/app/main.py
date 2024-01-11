"""
Main Module
"""

from http import HTTPStatus
from flask import request
from flask.views import MethodView
from marshmallow import ValidationError

from app.serializers import ContactUsSchema, UserLoginSchema, UserRegistrationSchema
from app.utils import custom_response, email_exists, login_user, record_contact_us_query, register_user


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