from unittest.mock import AsyncMock

from pytest import mark, raises

from repo_data.controllers import GetUserDataFromDataSource
from repo_data.data_source.github.github_client import GithubClient
from repo_data.exceptions import DataSourceError


@mark.asyncio
async def test_connection_error(mocker):
    github_client_mock = mocker.patch.object(
        GithubClient,
        'get_user',
        new_callabler=AsyncMock
    )
    github_client_mock.return_value = {}
    controller = GetUserDataFromDataSource(username='pity7736')
    with raises(DataSourceError):
        await controller.get()
