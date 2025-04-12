from marshmallow import Schema, fields, validate, validates, ValidationError

class ContractAuditSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    source_code = fields.Str(required=True)
    version = fields.Str(required=True)
    optimization = fields.Boolean()
    submit_time = fields.DateTime(format='%Y-%m-%d %H:%M:%S', dump_only=True)
    audit_status = fields.Int(validate=validate.OneOf([0, 1, 2]))
    audit_result = fields.Dict(keys=fields.Str(), values=fields.Raw(), allow_none=True)
    registered_contract_id = fields.Int(allow_none=True)