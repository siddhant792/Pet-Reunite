"""
Utility Module
"""
import secrets
import string

from http import HTTPStatus

from flask import jsonify
from app.settings import FS_CLIENT
from passlib.hash import pbkdf2_sha256


def custom_response(
    message: str = "",
    data: dict = None,
    error: dict = None,
    status_code: HTTPStatus = HTTPStatus.OK,
) -> tuple:
    return (
        jsonify(
            {
                "message": message,
                "data": data or {},
                "error": error or {},
            }
        ),
        status_code,
    )


def email_exists(email):
    user_query = FS_CLIENT.collection('users').where('email', '==', email).limit(1).get()
    return len(user_query) > 0


def register_user(validated_data):
    # Save user data to Firestore
    user_ref = FS_CLIENT.collection('users').document()
    updated_user_data = {"_id": user_ref.id, **validated_data}
    updated_user_data["password"] = pbkdf2_sha256.hash(updated_user_data["password"])
    user_ref.set(updated_user_data)

    updated_user_data.pop('password', None)
    return updated_user_data


def login_user(validated_data):
    user_query = FS_CLIENT.collection('users').where('email', '==', validated_data['email']).limit(1).get()

    if len(user_query) == 0:
        return custom_response(message="User not found", status_code=HTTPStatus.BAD_REQUEST)

    user_data = user_query[0].to_dict()
    if pbkdf2_sha256.verify(validated_data["password"], user_data["password"]):
        user_data.pop('password', None)
        return custom_response(message="Login successful", data=user_data, status_code=HTTPStatus.OK)
    else:
        return custom_response(message="Incorrect email or password", status_code=HTTPStatus.BAD_REQUEST)


def record_contact_us_query(validated_data):
    ref = FS_CLIENT.collection('contactUs').document()
    ref.set(validated_data)


def fetch_dog_breeds():
    breeds = []
    for e in FS_CLIENT.collection("dogBreeds").stream():
        breeds.append(e.to_dict()["name"])
    
    return breeds


def generate_unique_id(length):
    characters = string.ascii_letters + string.digits
    unique_id = ''.join(secrets.choice(characters) for _ in range(length))
    return unique_id
