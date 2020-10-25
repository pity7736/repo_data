from repo_data.constanst import DataSourceEnum
from repo_data.controllers.create_repo_from_data_source import CreateRepoFromDataSource
from repo_data.data_source import DataSourceFactory


class CreateRepo:

    def __init__(self, username: str, name: str, data_source: str):
        self._username = username
        self._name = name
        self._data_source = data_source

    async def run(self):
        factory = DataSourceFactory(
            data_source=DataSourceEnum(self._data_source),
            username=self._username
        )
        data_source = factory.get()
        controller = CreateRepoFromDataSource(
            owner_username=self._username,
            data_source=data_source
        )
        await controller.create(name=self._name)
