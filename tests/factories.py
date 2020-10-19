import inspect

from factory import Factory, SubFactory

from repo_data.models import User, Repository


class CreateFactoryMixin:

    @classmethod
    def _create(cls, model_class, **kwargs):
        async def create(**create_kwargs):
            for key, value in create_kwargs.items():
                if inspect.isawaitable(value):
                    create_kwargs[key] = await value
            return await model_class.create(**create_kwargs)
        return create(**kwargs)


class UserFactory(CreateFactoryMixin, Factory):
    username = 'pity7736'
    name = 'julián cortés'

    class Meta:
        model = User


class RepositoryFactory(CreateFactoryMixin, Factory):
    name = 'nyiobo'
    owner = SubFactory(UserFactory)

    class Meta:
        model = Repository
