from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    name = fields.Str()
    company = fields.Str()
    blog = fields.Str()
    location = fields.Str()
    email = fields.Str()
    bio = fields.Str()


class RepoSchema(Schema):
    name = fields.Str()
