from tortoise import Model, fields


class Repository(Model):
    name = fields.CharField(max_length=200)
    owner = fields.ForeignKeyField('models.User')
