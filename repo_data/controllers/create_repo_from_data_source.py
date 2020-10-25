from tortoise.exceptions import DoesNotExist

from repo_data.exceptions import DataSourceError
from repo_data.data_source import DataSource
from repo_data.data_source.github import GithubDataSource
from repo_data.models import Repository, User
from .create_user_from_data_source import CreateUserFromDataSource


class CreateRepoFromDataSource:

    __slots__ = ('_data_source',)

    def __init__(self, owner_username: str, data_source: DataSource = None):
        self._data_source = data_source or GithubDataSource(username=owner_username)

    async def create(self, name: str):
        repo = await Repository.get_or_none(
            name=name,
            owner__username=self._data_source.username
        )
        if repo:
            return repo

        try:
            repo_data = await self._data_source.get_repo_data(name=name)
        except DataSourceError:
            return None
        return await Repository.create(
            name=repo_data.name,
            owner=await self._get_owner()
        )

    async def _get_owner(self):
        try:
            owner = await User.get(username=self._data_source.username)
        except DoesNotExist:
            controller = CreateUserFromDataSource(data_source=self._data_source)
            owner = await controller.create()
        return owner
