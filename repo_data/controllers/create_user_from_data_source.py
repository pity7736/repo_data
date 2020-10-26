from typing import Optional

from repo_data.exceptions import DataSourceError
from repo_data.models import User
from ..data_source.data_source import DataSource
from ..data_source.user_data import UserData


async def _create_user_from_user_data(user_data: UserData) -> User:
    user, created = await User.get_or_create(
        username=user_data.username,
        data_source_id=user_data.data_source_id,
        defaults={
            'name': user_data.name,
            'company': user_data.company,
            'blog': user_data.blog,
            'location': user_data.location,
            'email': user_data.email,
            'bio': user_data.bio,
        }
    )
    return user


class CreateUserFromDataSource:

    __slots__ = ('_data_source',)

    def __init__(self, data_source: DataSource):
        self._data_source = data_source

    async def create(self, create_followers=False,
                     create_followings=False) -> Optional[User]:
        try:
            user_data = await self._data_source.get_user_data()
        except DataSourceError:
            return None
        else:
            user = await _create_user_from_user_data(user_data=user_data)
        await self._create_followers(user, create_followers)
        await self._create_following(user, create_followings)
        return user

    async def _create_followers(self, user, create_followers):
        if create_followers is True:
            followers_data = await self._data_source.get_user_followers_data()
            followers = []
            for follower_data in followers_data:
                follower = await _create_user_from_user_data(user_data=follower_data)
                followers.append(follower)
            await user.followers.add(*followers)

    async def _create_following(self, user, create_followings):
        if create_followings is True:
            followings_data = await self._data_source.get_user_followings_data()
            followings = []
            for following_data in followings_data:
                following = await _create_user_from_user_data(user_data=following_data)
                followings.append(following)
            await user.followings.add(*followings)
