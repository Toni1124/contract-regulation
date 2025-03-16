from marshmallow import Schema, fields, validates, ValidationError
from app.utils.validators import validate_ethereum_address

class ContractSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    address = fields.Str(required=True)
    source_code = fields.Str(required=True)
    abi = fields.Dict(allow_none=True)
    create_time = fields.DateTime(format='%Y-%m-%d %H:%M:%S', dump_only=True)
    status = fields.Int(dump_only=True)

    @validates('address')
    def validate_address(self, value):
        if not validate_ethereum_address(value):
            raise ValidationError('Invalid contract address format') 