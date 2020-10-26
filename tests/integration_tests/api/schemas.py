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
    id = fields.Int()
    name = fields.Str()
    full_name = fields.Str()
    owner_url = fields.Function(lambda obj: f'/api/users/{obj.owner_id}')
    private = fields.Bool()
    description = fields.Str()
    language = fields.Str()
