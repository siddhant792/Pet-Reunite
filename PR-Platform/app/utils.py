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
from PIL import Image
import torch
import requests
from io import BytesIO
from transformers import ViTFeatureExtractor, ViTForImageClassification

bucket = STORAGE_CLIENT.bucket('default-bucket-pet-reunite')
model = ViTForImageClassification.from_pretrained("skyau/dog-breed-classifier-vit")
feature_extractor = ViTFeatureExtractor.from_pretrained("skyau/dog-breed-classifier-vit")

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


def predict_dog_breed(image_path):
    response = requests.get(image_path)
    image = Image.open(BytesIO(response.content))
    inputs = feature_extractor(images=image, return_tensors="pt")

    # Make predictions
    with torch.no_grad():
        logits = model(**inputs).logits

    predicted_label = logits.argmax(-1).item()
    return str(model.config.id2label[predicted_label]).lower()


def record_found_pet(validated_data):
    pet_ref = FS_CLIENT.collection(f"users/{validated_data['user_id']}/foundPets").document()
    blob = bucket.blob(f"pet-images/{pet_ref.id}.jpg")
    decoded_image_data = base64.b64decode(validated_data['image'])
    blob.upload_from_string(decoded_image_data, content_type='image/jpeg')
    blob.acl.all().grant_read()
    blob.acl.save()
    validated_data["image"] = blob.public_url
    if "longitude" in validated_data and "latitude" in validated_data:
        validated_data["coordinates"] = firestore.GeoPoint(validated_data["latitude"], validated_data["longitude"])
        validated_data.pop("latitude", None)
        validated_data.pop("longitude", None)

    if "breed" not in validated_data:
        predicted_breed = predict_dog_breed(blob.public_url)
        validated_data["breed"] = predicted_breed

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
        if distance_in_km <= radius and validated_data['color'].lower() == doc_data['color'] and validated_data['breed'].lower() == doc_data["breed"] and validated_data['gender'].lower() == doc_data["gender"]:
            doc_data["last_seen"]["latitude"] = str(doc_coordinates.latitude)
            doc_data["last_seen"]["longitude"] = str(doc_coordinates.longitude)
            doc_data["last_seen"].pop("coordinates", None)
            user = FS_CLIENT.document(f"users/{doc_data['user_id']}").get().to_dict()
            doc_data["user_name"] = user["first_name"] + " " + user["last_name"]
            filtered_lost_pets.append(doc_data)

    return filtered_lost_pets


def fetch_found_pet_search_result(validated_data):
    latitude = validated_data["search_latitude"]
    longitude = validated_data["search_longitude"]
    radius = validated_data["search_radius"]

    query = FS_CLIENT.collection_group("foundPets")

    filtered_lost_pets = []
    for doc in query.stream():
        doc_data = doc.to_dict()
        address = doc_data.get("address")
        if doc_data["shelter_type"] != "home":
            shelter_data = FS_CLIENT.document(f"animalShelters/{doc_data['animal_shelter_id']}").get().to_dict()
            doc_coordinates = shelter_data.get("coordinates")
            address = shelter_data.get("address")
        else:
            doc_coordinates = doc_data.get("coordinates")
        doc_data["last_seen"] = {}
        distance_in_km = distance_between_locations_in_km(latitude, longitude, Decimal(doc_coordinates.latitude), Decimal(doc_coordinates.longitude))
        if distance_in_km <= radius and validated_data['color'].lower() == doc_data['color'] and validated_data['breed'].lower() == doc_data["breed"] and validated_data['gender'].lower() == doc_data["gender"]:
            doc_data["last_seen"]["latitude"] = str(doc_coordinates.latitude)
            doc_data["last_seen"]["longitude"] = str(doc_coordinates.longitude)
            if doc_data["shelter_type"] == "home":
                doc_data.pop("coordinates")
            doc_data["last_seen"]["address"] = address
            user = FS_CLIENT.document(f"users/{doc_data['user_id']}").get().to_dict()
            doc_data["user_name"] = user["first_name"] + " " + user["last_name"]
            filtered_lost_pets.append(doc_data)

    return filtered_lost_pets


def fetch_animal_shelters():
    animal_shelters = []
    for e in FS_CLIENT.collection("animalShelters").stream():
        data = e.to_dict()
        data["latitude"] = data["coordinates"].latitude
        data["longitude"] = data["coordinates"].longitude
        data.pop("coordinates")
        animal_shelters.append(data)
    
    return animal_shelters


def fetch_user_pets(user_id):
    registered_pets = []
    for e in FS_CLIENT.collection(f"users/{user_id}/pets").stream():
        doc_data = e.to_dict()
        doc_data["last_seen"] = {}
        registered_pets.append(doc_data)
    
    return registered_pets


def update_registered_pet_lost_status(validated_data):
    pet_ref = FS_CLIENT.document(f"users/{validated_data['user_id']}/pets/{validated_data['pet_id']}")
    updated_data = {
        'last_seen': {
            'address': validated_data['address'],
            'coordinates': firestore.GeoPoint(validated_data["latitude"], validated_data["longitude"])
        },
        'lostReportingTimeStamp': datetime.datetime.now(),
        'status': PetStatusEnum.LOST.value
    }
    pet_ref.set(updated_data, merge=True)
