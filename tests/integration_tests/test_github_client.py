from pytest import mark

from repo_data.data_source.github.github_client import GithubClient


@mark.asyncio
async def test_get_user():
    client = GithubClient()
    user_data = await client.get_user('pity7736')

    assert user_data['login'] == 'pity7736'
    assert user_data['name'] == 'Julián Cortés'


@mark.asyncio
async def test_get_non_existent_user():
    client = GithubClient()
    user_data = await client.get_user('qwertyzxc123')

    assert user_data == {}
