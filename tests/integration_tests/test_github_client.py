from pytest import mark, fixture

from repo_data import settings
from repo_data.data_source.github.github_client import GithubClient


@fixture
def client():
    return GithubClient()


@mark.asyncio
async def test_get_user(client):
    user_data = await client.get_user('pity7736')

    assert user_data['login'] == 'pity7736'
    assert user_data['name'] == 'Julián Cortés'


@mark.asyncio
async def test_get_non_existent_user(client):
    user_data = await client.get_user(username='qwertyzxc123')
    assert user_data == {}


@mark.asyncio
async def test_get_repo(client):
    repo_data = await client.get_repository(owner='pity7736', name='nyoibo')

    assert repo_data['name'] == 'nyoibo'
    assert repo_data['private'] is False
    assert repo_data['description'] == 'Create automatically attribute accessor in ' \
                                       'Python.'
    assert repo_data['full_name'] == 'pity7736/nyoibo'


@mark.asyncio
async def test_get_non_existent_repo(client):
    user_data = await client.get_repository(owner='pitty7736', name='qwerty')
    assert user_data == {}


@mark.skip(reason='request limited')
@mark.asyncio
async def test_make_request_without_token():
    settings.GITHUB_TOKEN = None
    client = GithubClient()
    user_data = await client.get_user('pity7736')

    assert user_data['login'] == 'pity7736'
    assert user_data['name'] == 'Julián Cortés'


@mark.asyncio
async def test_get_user_followers(client):
    user_followers_data = await client.get_user_followers('pity7736')
    assert len(user_followers_data) == 11


@mark.asyncio
async def test_get_user_followings(client):
    user_followings_data = await client.get_user_followings('pity7736')
    assert len(user_followings_data) == 7
