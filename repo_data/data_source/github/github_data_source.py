from repo_data.data_source.user_data import UserData
from repo_data.exceptions import DataSourceError
from .github_client import GithubClient
from ..repo_data import RepoData


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

    async def get_repo_data(self, name: str) -> RepoData:
        repo_data = await self._client.get_repository(
            owner=self._username,
            name=name
        )
        if repo_data:
            return RepoData(
                name=name,
                full_name=repo_data['full_name'],
                description=repo_data['description'],
                private=repo_data['private']
            )

        raise DataSourceError('There was a mistake getting data from github')
