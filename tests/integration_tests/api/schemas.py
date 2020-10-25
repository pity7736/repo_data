from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    name = fields.Str()


class RepoSchema(Schema):
    name = fields.Str()
