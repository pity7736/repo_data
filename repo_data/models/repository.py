from tortoise import Model, fields


class Repository(Model):
    name = fields.CharField(max_length=200)
    full_name = fields.CharField(max_length=300)
    owner = fields.ForeignKeyField('models.User')
    private = fields.BooleanField()
    description = fields.TextField()
    language = fields.CharField(max_length=50)
