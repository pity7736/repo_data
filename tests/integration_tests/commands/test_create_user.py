from pytest import mark

from repo_data.commands import CreateUser
from repo_data.constanst import DataSourceEnum
from repo_data.models import User


@mark.asyncio
async def test_success(db_connection):
    username = 'pity7736'
    command = CreateUser(username=username, data_source=DataSourceEnum.GITHUB.value)
    await command.run()

    user = await User.get(username=username)

    assert user.username == username
