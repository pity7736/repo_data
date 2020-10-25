from abc import ABCMeta, abstractmethod
from typing import List

from .repo_data import RepoData
from .user_data import UserData


class DataSource(metaclass=ABCMeta):

    def __init__(self, username: str):
        self._username = username

    @property
    def username(self) -> str:
        return self._username

    @abstractmethod
    async def get_user_data(self) -> UserData:
        pass

    @abstractmethod
    async def get_repo_data(self, name: str) -> RepoData:
        pass

    @abstractmethod
    async def get_user_followers_data(self) -> List[UserData]:
        pass
