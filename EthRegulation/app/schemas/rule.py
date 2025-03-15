from marshmallow import Schema, fields, validates, ValidationError
from app.utils.validators import validate_ethereum_address

class RuleParameterSchema(Schema):
    name = fields.Str(required=True)
    type = fields.Str(required=True)
    condition = fields.Str(required=True)
    value = fields.Str(required=True)

class RuleFunctionSchema(Schema):
    name = fields.Str(required=True)
    params = fields.List(fields.Nested(RuleParameterSchema))

class RuleSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    regulator_address = fields.Str(required=True, data_key='regulatorAddress')
    description = fields.Str(allow_none=True)
    contract_address = fields.Str(required=True, data_key='contractAddress')
    owner = fields.Str(required=True)
    rule_id = fields.Str(dump_only=True, data_key='ruleId')
    status = fields.Int(dump_only=True)
    create_time = fields.DateTime(format='%Y-%m-%d %H:%M:%S', dump_only=True, data_key='createTime')
    functions = fields.List(fields.Nested(RuleFunctionSchema))

    @validates('regulator_address')
    def validate_regulator_address(self, value):
        if not validate_ethereum_address(value):
            raise ValidationError('Invalid regulator address format')

    @validates('contract_address')
    def validate_contract_address(self, value):
        if not validate_ethereum_address(value):
            raise ValidationError('Invalid contract address format') 