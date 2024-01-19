"""
Utility Module
"""

import base64
import datetime
import secrets
import string

from http import HTTPStatus

from flask import jsonify
import pytz
from app.enums import OrderingDirection, PetStatusEnum
from app.settings import FS_CLIENT, STORAGE_CLIENT
from passlib.hash import pbkdf2_sha256
from math import radians, sin, cos, sqrt, atan2
from google.cloud import firestore
from decimal import Decimal

bucket = STORAGE_CLIENT.bucket('default-bucket-pet-reunite')

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


def register_pet(validated_data):
    doc_ref = FS_CLIENT.document(f"users/{validated_data['user_id']}/pets/{validated_data['id']}")
    blob = bucket.blob(f"pet-images/{doc_ref.id}.jpg")
    decoded_image_data = base64.b64decode(validated_data['image'])
    blob.upload_from_string(decoded_image_data, content_type='image/jpeg')
    blob.acl.all().grant_read()
    blob.acl.save()

    validated_data["image"] = blob.public_url
    doc_ref.set(validated_data)
    return {"id": validated_data["id"]}


def update_pet_last_seen(validated_data):
    pet_ref = FS_CLIENT.document(f"users/{validated_data['user_id']}/pets/{validated_data['pet_id']}")
    pet_ref.set({
        "last_seen": {
            "address": validated_data["address"],
            "coordinates": firestore.GeoPoint(validated_data["latitude"], validated_data["longitude"])
        },
        "status": PetStatusEnum.LOST.value,
        "lostReportingTimeStamp": datetime.datetime.now(tz=pytz.timezone("Australia/Sydney"))
    }, merge=True)


def record_found_pet(validated_data):
    pet_ref = FS_CLIENT.collection(f"users/{validated_data['user_id']}/foundPets").document()
    blob = bucket.blob(f"pet-images/{pet_ref.id}.jpg")
    decoded_image_data = base64.b64decode(validated_data['image'])
    blob.upload_from_string(decoded_image_data, content_type='image/jpeg')
    blob.acl.all().grant_read()
    blob.acl.save()
    validated_data["image"] = blob.public_url
    if "longitude" and "latitude":
        validated_data["coordinates"] = firestore.GeoPoint(validated_data["latitude"], validated_data["longitude"])
        validated_data.pop("latitude", None)
        validated_data.pop("longitude", None)

    pet_ref.set(validated_data)


def distance_between_locations_in_km(lat1, lon1, lat2, lon2):
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    radius_of_earth = 6371.0
    distance = radius_of_earth * c
    return distance


def fetch_lost_pet_search_result(validated_data):
    latitude = validated_data["search_latitude"]
    longitude = validated_data["search_longitude"]
    radius = validated_data["search_radius"]

    query = FS_CLIENT.collection_group("pets").where(
        'status', "==", PetStatusEnum.LOST.value
    ).order_by(
        "lostReportingTimeStamp", direction=OrderingDirection.DESCENDING.value
    )

    filtered_lost_pets = []
    for doc in query.stream():
        doc_data = doc.to_dict()
        doc_coordinates = doc_data.get('last_seen', {}).get("coordinates")

        distance_in_km = distance_between_locations_in_km(latitude, longitude, Decimal(doc_coordinates.latitude), Decimal(doc_coordinates.longitude))
        if distance_in_km <= radius:
            doc_data["last_seen"]["latitude"] = str(doc_coordinates.latitude)
            doc_data["last_seen"]["longitude"] = str(doc_coordinates.longitude)
            doc_data["last_seen"].pop("coordinates", None)
            filtered_lost_pets.append(doc_data)

    return filtered_lost_pets
