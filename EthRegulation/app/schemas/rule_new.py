from app.extensions import ma
from app.models.rule_new import RuleNew
from marshmallow import fields

class RuleNewSchema(ma.SQLAlchemySchema):
    class Meta:
        model = RuleNew
        load_instance = True

    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    contract_address = fields.Str(required=True, data_key='contractAddress')
    description = fields.Str(allow_none=True)
    owner = fields.Str(required=True)
    functions = fields.Raw()  # 使用Raw字段处理JSON数据
    status = fields.Int(dump_only=True)
    create_time = fields.DateTime(format='%Y-%m-%d %H:%M:%S', dump_only=True, data_key='createTime')
    update_time = fields.DateTime(format='%Y-%m-%d %H:%M:%S', dump_only=True, data_key='updateTime')
    rule_number = fields.Str(allow_none=True, data_key='ruleNumber')
    regulator_address = fields.Str(allow_none=True, data_key='regulatorAddress') 