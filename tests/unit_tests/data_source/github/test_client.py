from unittest.mock import AsyncMock

import httpx
from httpx import Request
from pytest import mark

from repo_data.data_source.github.github_client import GithubClient


exception_classes = (
    httpx.ConnectTimeout,
    httpx.ConnectError
)


@mark.parametrize('exception_class', exception_classes)
@mark.asyncio
async def test_request_error(mocker, exception_class):
    get_user_mock = mocker.patch.object(
        httpx.AsyncClient,
        'get',
        new_callable=AsyncMock
     )
    username = 'pity7736'
    request = Request(
        'GET',
        f'https://api.github.com/users/{username}'
    )
    get_user_mock.side_effect = exception_class('timeout error', request=request)

    client = GithubClient()
    user_data = await client.get_user(username)

    assert user_data == {}
