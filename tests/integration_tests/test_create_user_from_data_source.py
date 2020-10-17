from pytest import mark

from repo_data.controllers import CreateUserFromDataSource
from repo_data.models import User


username_values = (
    (
        'pity7736',
        {
            'name': 'julián cortés'
        }
    ),
    (
        'Danjavia',
        {
            'name': 'danny hoower antonio viasus avila'
        }
    )
)


@mark.parametrize('username, result_data', username_values)
@mark.asyncio
async def test_sucess(db_connection, username, result_data):
    controller = CreateUserFromDataSource(username=username)
    created_user = await controller.create()

    user = await User.get(username=username)
    assert created_user == user
    assert user.username == username
    assert user.name == result_data['name']
