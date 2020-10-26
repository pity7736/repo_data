from pytest import mark

from repo_data.commands import CreateUser
from repo_data.constanst import DataSourceEnum
from repo_data.models import User


@mark.asyncio
async def test_success(db_connection):
    username = 'pity7736'
    command = CreateUser(
        username=username,
        data_source=DataSourceEnum.GITHUB.value,
        create_followers=False,
        create_followings=False
    )
    await command.run()

    user = await User.get(username=username)

    assert user.username == username


@mark.asyncio
async def test_create_followers_and_followings(db_connection):
    username = 'pity7736'
    command = CreateUser(
        username=username,
        data_source=DataSourceEnum.GITHUB.value,
        create_followers=True,
        create_followings=True
    )
    await command.run()

    user = await User.get(username=username)
    number_followers = await user.followers.all().count()
    number_followings = await user.followings.all().count()

    assert user.username == username
    assert number_followers == 11
    assert number_followings == 7
