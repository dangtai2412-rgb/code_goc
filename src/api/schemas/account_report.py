from marshmallow import Schema, fields

class AccountReportRequestSchema(Schema):
    owner_id = fields.Int(required=True)
    report_type = fields.Str(required=True)
    reporting_period = fields.Str(required=True)
    generated_date = fields.Date(required=True)

class AccountReportResponseSchema(Schema):
    report_id = fields.Int()
    owner_id = fields.Int()
    report_type = fields.Str()
    reporting_period = fields.Str()
    generated_date = fields.Date()