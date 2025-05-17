from marshmallow import Schema, fields


class NoteSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    body = fields.Str(required=True)
    user_id = fields.Int(required=True)
    category_id = fields.Int(load_default=None)
