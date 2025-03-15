from marshmallow import Schema, fields, validate, validates, ValidationError, post_dump
from app.utils.validators import validate_ethereum_address
from typing import Any

class BlackWhiteListSchema(Schema):
    id = fields.Int(dump_only=True)
    address = fields.Str(required=True)
    operate_time = fields.DateTime(format='%Y-%m-%d %H:%M:%S', dump_only=True, data_key='operateTime')
    operator = fields.Str(required=True)
    type = fields.Int(required=True, validate=validate.OneOf([1, 2]))
    organization = fields.Str(required=True)
    region = fields.Str(required=True)

    @validates('address')
    def validate_address(self, value: str) -> None:
        if not validate_ethereum_address(value):
            raise ValidationError('Invalid Ethereum address format')

    @validates('operator')
    def validate_operator_value(self, value: str) -> None:
        if not value or len(value) > 100:
            raise ValidationError('Invalid operator')

    @validates('organization')
    def validate_organization_value(self, value: str) -> None:
        if not value or len(value) > 100:
            raise ValidationError('Invalid organization')

    @validates('region')
    def validate_region_value(self, value: str) -> None:
        if not value or len(value) > 100:
            raise ValidationError('Invalid region') 