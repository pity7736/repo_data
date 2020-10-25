from typing import Optional

from tortoise.exceptions import DoesNotExist

from repo_data.exceptions import DataSourceError
from repo_data.models import User
from ..data_source.data_source import DataSource


class CreateUserFromDataSource:

    __slots__ = ('_data_source',)

    def __init__(self, data_source: DataSource):
        self._data_source = data_source

    async def create(self, create_followers=False,
                     create_followings=False) -> Optional[User]:
        try:
            user = await User.get(username=self._data_source.username)
        except DoesNotExist:
            try:
                user_data = await self._data_source.get_user_data()
            except DataSourceError:
                return None
            else:
                user = await User.create(
                    username=user_data.username,
                    name=user_data.name
                )
        await self._create_followers(user, create_followers)
        await self._create_following(user, create_followings)
        return user

    async def _create_followers(self, user, create_followers):
        if create_followers is True:
            followers_data = await self._data_source.get_user_followers_data()
            followers = []
            for follower_data in followers_data:
                follower, created = await User.get_or_create(
                    username=follower_data.username,
                    name=follower_data.name
                )
                followers.append(follower)
            await user.followers.add(*followers)

    async def _create_following(self, user, create_followings):
        if create_followings is True:
            followings_data = await self._data_source.get_user_followings_data()
            followings = []
            for following_data in followings_data:
                following, created = await User.get_or_create(
                    username=following_data.username,
                    name=following_data.name
                )
                followings.append(following)
            await user.followings.add(*followings)
