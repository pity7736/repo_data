from tortoise.exceptions import DoesNotExist

from repo_data.models import Repository, User
from .create_user_from_data_source import CreateUserFromDataSource
from .get_data_from_data_source import GetDataFromDataSource
from ..exceptions import DataSourceError


class CreateRepoFromDataSource:

    def __init__(self, owner_username: str):
        self._owner_username = owner_username

    async def create(self, name: str):
        repo = await Repository.get_or_none(
            name=name,
            owner__username=self._owner_username
        )
        if repo:
            return repo

        data_source = GetDataFromDataSource(username=self._owner_username)
        try:
            repo_data = await data_source.get_repo_data(name=name)
        except DataSourceError:
            return None
        return await Repository.create(
            name=repo_data.name,
            owner=await self._get_owner()
        )

    async def _get_owner(self):
        try:
            owner = await User.get(username=self._owner_username)
        except DoesNotExist:
            controller = CreateUserFromDataSource(username=self._owner_username)
            owner = await controller.create()
        return owner
