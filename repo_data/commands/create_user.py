from repo_data.constanst import DataSourceEnum
from repo_data.controllers import CreateUserFromDataSource
from repo_data.data_source import DataSourceFactory


class CreateUser:

    def __init__(self, username: str, data_source: str, create_followers: bool,
                 create_followings: bool):
        self._username = username
        self._data_source = data_source
        self._create_followers = create_followers
        self._create_followings = create_followings

    async def run(self):
        factory = DataSourceFactory(
            data_source=DataSourceEnum(self._data_source),
            username=self._username
        )
        data_source = factory.get()
        controller = CreateUserFromDataSource(data_source=data_source)
        await controller.create(
            create_followers=self._create_followers,
            create_followings=self._create_followings
        )
