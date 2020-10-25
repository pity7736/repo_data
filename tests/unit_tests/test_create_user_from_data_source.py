from unittest.mock import AsyncMock

from pytest import mark

from repo_data.controllers import CreateUserFromDataSource
from repo_data.data_source.github.github_client import GithubClient
from repo_data.data_source.github.github_data_source import GithubDataSource


@mark.asyncio
async def test_connection_error(mocker):
    github_client_mock = mocker.patch.object(
        GithubClient,
        'get_user',
        new_callable=AsyncMock
    )
    github_client_mock.return_value = {}
    data_source = GithubDataSource(username='pity7736')
    controller = CreateUserFromDataSource(data_source=data_source)

    assert await controller.create() is None
