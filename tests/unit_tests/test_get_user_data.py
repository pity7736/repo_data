from unittest.mock import AsyncMock

from pytest import mark, raises

from repo_data.controllers import GetUserData
from repo_data.data_source.github.client import Client
from repo_data.exceptions import DataSourceError


@mark.asyncio
async def test_connection_error(mocker):
    github_client_mock = mocker.patch.object(
        Client,
        'get_user',
        new_callabler=AsyncMock
    )
    github_client_mock.return_value = {}
    controller = GetUserData(username='pity7736')
    with raises(DataSourceError):
        await controller.get()
