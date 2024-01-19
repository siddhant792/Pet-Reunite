"""
Serializer Module
"""

from datetime import datetime
from marshmallow import EXCLUDE, Schema, fields, post_load, pre_load, validate

from app.enums import PetGenderEnum, PetShelterEnum, PetStatusEnum
from decimal import Decimal

class UserRegistrationSchema(Schema):
    first_name = fields.Str(required=True, validate=validate.Length(max=50))
    last_name = fields.Str(required=True, validate=validate.Length(max=50))
    email = fields.Email(required=True)
    address = fields.Str(required=True, validate=validate.Length(max=255))
    password = fields.Str(required=True, validate=validate.Length(min=5))

    class Meta:
        unknown = EXCLUDE


class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)

    class Meta:
        unknown = EXCLUDE


class ContactUsSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(max=50))
    email = fields.Email(required=True)
    message = fields.Str(required=True, validate=validate.Length(max=455))
    timestamp = fields.DateTime()

    class Meta:
        unknown = EXCLUDE

    @post_load
    def transform(self, data, *args, **kwargs):
        data["timestamp"] = datetime.now()
        return data


class RegisterPetSchema(Schema):
    id = fields.Str(required=True)
    name = fields.Str(required=True)
    breed = fields.Str(required=True)
    color = fields.Str(required=True)
    age = fields.Int(required=True)
    gender = fields.Str(required=True, validate=validate.OneOf([status.value for status in PetGenderEnum]))
    description = fields.Str(required=True, validate=validate.Length(max=1000))
    image = fields.Str(required=True)
    user_id = fields.Str(required=True)
    status = fields.Str(
        validate=validate.OneOf([status.value for status in PetStatusEnum]),
        default=PetStatusEnum.REGISTERED.value
    )

    class Meta:
        unknown = EXCLUDE


class LastSeenLostPetSchema(Schema):
    user_id = fields.Str(required=True)
    pet_id = fields.Str(required=True)
    address = fields.Str(required=True)
    latitude = fields.Str(required=True)
    longitude = fields.Str(required=True)

    class Meta:
        unknown = EXCLUDE

    @post_load
    def convert_coordinates(self, data, **_):
        data['latitude'] = Decimal(data['latitude'])
        data['longitude'] = Decimal(data['longitude'])
        return data


class ReportFoundPetSchema(Schema):
    user_id = fields.Str(required=True)
    breed = fields.Str()
    color = fields.Str()
    gender = fields.Str(required=True, validate=validate.OneOf([status.value for status in PetGenderEnum]))
    description = fields.Str(required=True, validate=validate.Length(max=1000))
    address = fields.Str()
    latitude = fields.Str()
    longitude = fields.Str()
    animal_shelter_id = fields.Str()
    shelter_type = fields.Str(validate=validate.OneOf([status.value for status in PetShelterEnum]), required=True)
    image = fields.Str(required=True)

    class Meta:
        unknown = EXCLUDE

    @pre_load
    def validate_shelter_type(self, data, **_):
        shelter_type = data.get('shelter_type')
        if shelter_type == PetShelterEnum.ANIMAL_SHELTER.value:
            if 'animal_shelter_id' not in data:
                raise ValueError('animal_shelter_id must be present for animal_shelter type.')

        elif shelter_type == PetShelterEnum.HOME.value:
            required_fields = ['address', 'latitude', 'longitude']
            if not all(field in data for field in required_fields):
                raise ValueError('address, latitude, and longitude must be present for home type.')

        return data
    
    @post_load
    def convert_coordinates(self, data, **_):
        if "latitude" in data:
            data['latitude'] = Decimal(data['latitude'])
        
        if "longitude" in data:
            data['longitude'] = Decimal(data['longitude'])

        return data


class LostPetSearchRequestSchema(Schema):
    color = fields.Str(required=True)
    gender = fields.Str(required=True)
    breed = fields.Str(required=True)
    search_address = fields.Str(required=True)
    search_latitude = fields.Str(required=True)
    search_longitude = fields.Str(required=True)
    search_radius = fields.Int(required=True)

    class Meta:
        unknown = EXCLUDE

    @post_load
    def convert_coordinates(self, data, **_):
        data['search_latitude'] = Decimal(data['search_latitude'])
        data['search_longitude'] = Decimal(data['search_longitude'])
        return data