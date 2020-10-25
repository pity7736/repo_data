from typing import List

from repo_data.data_source.user_data import UserData
from repo_data.exceptions import DataSourceError
from .github_client import GithubClient
from ..data_source import DataSource
from ..repo_data import RepoData


class GithubDataSource(DataSource):

    def __init__(self, username: str):
        super().__init__(username)
        self._client = GithubClient()

    async def get_user_followers_data(self) -> List[UserData]:
        followers_data = await self._client.get_user_followers(username=self._username)
        if followers_data:
            result = []
            for follower_data in followers_data:
                result.append(await self.get_user_data(follower_data['login']))
            return result
        raise DataSourceError('There was a mistake getting data from github')

    async def get_user_data(self, username=None) -> UserData:
        username = username or self._username
        user_data = await self._client.get_user(username=username)
        if user_data:
            return UserData(
                username=username,
                name=user_data['name'].lower() if user_data['name'] else ''
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
