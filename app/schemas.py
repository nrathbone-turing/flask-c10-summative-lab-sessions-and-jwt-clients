# app/schemas.py
# Marshmallow schemas for serializing User and Note models into JSON.

from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True)

class NoteSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    body = fields.Str()

user_schema = UserSchema()
note_schema = NoteSchema()
notes_schema = NoteSchema(many=True)
