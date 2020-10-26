from tortoise import Model, fields


class User(Model):
    username = fields.CharField(max_length=200)
    data_source_id = fields.CharField(max_length=100)
    name = fields.CharField(max_length=100)
    company = fields.CharField(max_length=200, null=True)
    blog = fields.CharField(max_length=200, null=True)
    location = fields.CharField(max_length=200, null=True)
    email = fields.CharField(max_length=200, null=True)
    bio = fields.CharField(max_length=200, null=True)
    followers = fields.ManyToManyField(
        'models.User',
        related_name='user_followers',
        through='user_followers'
    )
    followings = fields.ManyToManyField(
        'models.User',
        related_name='user_following',
        through='user_followings'
    )

    def __str__(self):
        return f'User: {self.username}'
