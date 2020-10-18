from typing import Optional

from repo_data.exceptions import DataSourceError
from repo_data.models import User
from .get_data_from_data_source import GetDataFromDataSource


class CreateUserFromDataSource:

    def __init__(self, username: str):
        self._username = username

    async def create(self) -> Optional[User]:
        data_source = GetDataFromDataSource(username=self._username)
        try:
            user_data = await data_source.get_user_data()
        except DataSourceError:
            return None
        else:
            return await User.create(username=user_data.username, name=user_data.name)
