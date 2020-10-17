from pytest import mark

from repo_data.controllers import GetUserData


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
async def test_get_user_data(username, result_data):
    controller = GetUserData(username=username)
    user_data = await controller.get()

    assert user_data.username == username
    assert user_data.name == result_data['name']
