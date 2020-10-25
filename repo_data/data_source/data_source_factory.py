from repo_data.constanst import DataSourceEnum
from repo_data.data_source.github import GithubDataSource


class DataSourceFactory:

    __slots__ = ('_data_source', '_username')

    _data_sources = {
        DataSourceEnum.GITHUB: GithubDataSource
    }

    def __init__(self, data_source: DataSourceEnum, username: str):
        self._data_source = data_source
        self._username = username

    def get(self):
        try:
            data_source_class = self._data_sources.get(self._data_source)
        except KeyError:
            raise ValueError(f'there are not {self._data_source} data source')
        return data_source_class(username=self._username)
