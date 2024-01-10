"""
Serializer Module
"""

from marshmallow import Schema, fields, validate

class UserRegistrationSchema(Schema):
    first_name = fields.Str(required=True, validate=validate.Length(max=50))
    last_name = fields.Str(required=True, validate=validate.Length(max=50))
    email = fields.Email(required=True)
    address = fields.Str(required=True, validate=validate.Length(max=255))
    password = fields.Str(required=True, validate=validate.Length(min=5))


class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)
