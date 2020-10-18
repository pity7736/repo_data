from repo_data.data_source.user_data import UserData
from repo_data.exceptions import DataSourceError
from .github_client import GithubClient


class GithubDataSource:

    def __init__(self, username: str):
        self._username = username
        self._client = GithubClient()

    async def get_user_data(self) -> UserData:
        user_data = await self._client.get_user(username=self._username)
        if user_data:
            return UserData(
                username=self._username,
                name=user_data['name'].lower()
            )
        raise DataSourceError('There was a mistake getting data from github')
