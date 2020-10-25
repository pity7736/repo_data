from typing import Optional

from repo_data.exceptions import DataSourceError
from repo_data.models import User
from ..data_source.data_source import DataSource


class CreateUserFromDataSource:

    __slots__ = ('_data_source',)

    def __init__(self, data_source: DataSource):
        self._data_source = data_source

    async def create(self) -> Optional[User]:
        try:
            user_data = await self._data_source.get_user_data()
        except DataSourceError:
            return None
        else:
            return await User.create(username=user_data.username, name=user_data.name)
