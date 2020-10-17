from repo_data.data_source.user_data import UserData
from repo_data.exceptions import DataSourceError
from .client import Client


class GetUserData:

    def __init__(self, username: str):
        self._username = username
        self._client = Client()

    async def get(self) -> UserData:
        user_data = await self._client.get_user(username=self._username)
        if user_data:
            return UserData(
                username=self._username,
                name=user_data['name'].lower()
            )
        raise DataSourceError('There was a mistake getting data from github')
