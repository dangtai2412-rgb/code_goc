from marshmallow import Schema, fields, validate


class AccountReportRequestSchema(Schema):
    owner_id = fields.Int(required=True)
    report_type = fields.Str(
        required=True,
        validate=validate.OneOf([
            "daily",
            "weekly",
            "monthly",
            "yearly"
        ])
    )
    reporting_period = fields.Str(required=True)
    generated_date = fields.Date(required=True)


class AccountReportResponseSchema(Schema):
    report_id = fields.Int()
    owner_id = fields.Int()
    report_type = fields.Str()
    reporting_period = fields.Str()
    generated_date = fields.Date()

    total_income = fields.Float()
    total_expense = fields.Float()
    profit = fields.Float()

    status = fields.Str()