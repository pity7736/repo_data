import asyncio
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
            tasks = []
            for follower_data in followers_data:
                tasks.append(self.get_user_data(follower_data['login']))
            return await asyncio.gather(*tasks)
        raise DataSourceError('There was a mistake getting data from github')

    async def get_user_followings_data(self) -> List[UserData]:
        followings_data = await self._client.get_user_followings(
            username=self._username
        )
        if followings_data:
            tasks = []
            for following_data in followings_data:
                tasks.append(self.get_user_data(username=following_data['login']))
            return await asyncio.gather(*tasks)
        raise DataSourceError('There was a mistake getting data from github')

    async def get_user_data(self, username=None) -> UserData:
        username = username or self._username
        user_data = await self._client.get_user(username=username)
        if user_data:
            return UserData(
                username=username,
                name=user_data['name'].lower() if user_data['name'] else '',
                data_source_id=user_data['id'],
                company=user_data['company'],
                blog=user_data['blog'],
                location=user_data['location'],
                email=user_data['email'],
                bio=user_data['bio'],
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
