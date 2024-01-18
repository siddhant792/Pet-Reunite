"""
Serializer Module
"""

from datetime import datetime
from marshmallow import EXCLUDE, Schema, fields, post_load, validate

from app.enums import PetStatusEnum

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
    gender = fields.Str(required=True)
    description = fields.Str(required=True, validate=validate.Length(max=1000))
    image = fields.Str(required=True)
    user_id = fields.Str(required=True)
    status = fields.Str(
        validate=validate.OneOf([status.value for status in PetStatusEnum]),
        default=PetStatusEnum.REGISTERED.value
    )

    class Meta:
        unknown = EXCLUDE


class LastSeenPetSchema(Schema):
    user_id = fields.Str(required=True)
    pet_id = fields.Str(required=True)
    address = fields.Str(required=True, validate=validate.Length(max=300))
    latitude = fields.Str(required=True)
    longitude = fields.Str(required=True)

    class Meta:
        unknown = EXCLUDE
