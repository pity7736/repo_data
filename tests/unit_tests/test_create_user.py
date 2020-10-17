from unittest.mock import AsyncMock

from pytest import mark

from repo_data.controllers import CreateUser
from repo_data.data_source.github.client import Client


@mark.asyncio
async def test_connection_error(mocker):
    github_client_mock = mocker.patch.object(
        Client,
        'get_user',
        new_callabler=AsyncMock
    )
    github_client_mock.return_value = {}
    controller = CreateUser(username='pity7736')

    assert await controller.create() is None
