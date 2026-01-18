from marshmallow import Schema, fields

class AIAssistantRequestSchema(Schema):
    version = fields.Str(required=True)
    supported_languages = fields.Str()
    ai_model_type = fields.Str()

class AIAssistantResponseSchema(Schema):
    ai_id = fields.Int()
    version = fields.Str()
    supported_languages = fields.Str()
    ai_model_type = fields.Str()