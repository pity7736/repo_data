from tortoise import Model, fields


class User(Model):
    username = fields.CharField(max_length=200)
    data_source_id = fields.CharField(max_length=100)
    name = fields.CharField(max_length=100)
