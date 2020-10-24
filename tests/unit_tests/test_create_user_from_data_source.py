from unittest.mock import AsyncMock

from pytest import mark

from repo_data.controllers import CreateUserFromDataSource
from repo_data.data_source.github.github_client import GithubClient


@mark.asyncio
async def test_connection_error(mocker):
    github_client_mock = mocker.patch.object(
        GithubClient,
        'get_user',
        new_callable=AsyncMock
    )
    github_client_mock.return_value = {}
    controller = CreateUserFromDataSource(username='pity7736')

    assert await controller.create() is None
