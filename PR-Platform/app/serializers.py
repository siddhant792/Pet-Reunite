"""
Serializer Module
"""

from datetime import datetime
from marshmallow import EXCLUDE, Schema, fields, post_load, validate

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
