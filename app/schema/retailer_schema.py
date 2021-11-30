from marshmallow import Schema, fields, validate
from marshmallow_enum import EnumField

from app import constants
from app.utils import StatusEnum, IDEnum


class RetailerSchema(Schema):
    id = fields.UUID()
    phone_number = fields.Str(
        validate=[
            validate.Regexp(constants.PHONE_NUMBER_REGEX),
        ]
    )
    first_name = fields.Str(validate=validate.Length(min=2))
    last_name = fields.Str(validate=validate.Length(min=2))
    id_type = EnumField(IDEnum)
    id_number = fields.Str(validate=validate.Length(min=5))
    pin = fields.Str(validate=validate.Length(min=4, max=4))
    status = EnumField(StatusEnum)
    created = fields.DateTime()
    modified = fields.DateTime()

    class Meta:
        fields = [
            "id",
            "phone_number",
            "first_name",
            "last_name",
            "id_type",
            "id_number",
            "pin",
            "status",
            "created",
            "modified",
        ]
        load_only = ["pin"]


class RetailerCreateSchema(Schema):
    phone_number = fields.Str(
        validate=[
            validate.Regexp(constants.PHONE_NUMBER_REGEX),
            validate.Length(min=10, max=10),
        ],
        required=True,
    )
    first_name = fields.Str(required=True, validate=validate.Length(min=2))
    last_name = fields.Str(required=True, validate=validate.Length(min=2))
    id_type = EnumField(IDEnum, required=True)
    id_number = fields.Str(required=True, validate=validate.Length(min=5))
    pin = fields.Str(required=True, validate=validate.Length(min=4, max=4))

    class Meta:
        fields = [
            "phone_number",
            "first_name",
            "last_name",
            "id_type",
            "id_number",
            "pin",
        ]


class RetailerReadSchema(Schema):
    id = fields.UUID()
    phone_number = fields.Str(
        validate=[
            validate.Regexp(constants.PHONE_NUMBER_REGEX),
        ]
    )
    first_name = fields.Str(validate=validate.Length(min=2))
    last_name = fields.Str(validate=validate.Length(min=2))
    id_type = EnumField(IDEnum)
    id_number = fields.Str(validate=validate.Length(min=5))
    status = EnumField(StatusEnum)
    created = fields.DateTime()
    modified = fields.DateTime()

    class Meta:
        fields = [
            "id",
            "phone_number",
            "first_name",
            "last_name",
            "id_type",
            "id_number",
            "status",
            "created",
            "modified",
        ]


class RetailerUpdateSchema(Schema):
    phone_number = fields.Str(validate=validate.Regexp(constants.PHONE_NUMBER_REGEX))
    first_name = fields.Str(validate=validate.Length(min=2))
    last_name = fields.Str(validate=validate.Length(min=2))
    id_type = EnumField(IDEnum)
    id_number = fields.Str(validate=validate.Length(min=5))
    status = EnumField(StatusEnum)

    class Meta:
        fields = [
            "id",
            "phone_number",
            "first_name",
            "last_name",
            "id_type",
            "id_number",
            "status",
        ]
