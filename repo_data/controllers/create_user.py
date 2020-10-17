from typing import Optional

from repo_data.exceptions import DataSourceError
from repo_data.models import User
from .get_user_data import GetUserData


class CreateUser:

    def __init__(self, username: str):
        self._username = username

    async def create(self) -> Optional[User]:
        get_user_data = GetUserData(username=self._username)
        try:
            user_data = await get_user_data.get()
        except DataSourceError:
            return None
        else:
            return await User.create(username=user_data.username, name=user_data.name)
