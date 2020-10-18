from pytest import mark

from repo_data.controllers import GetDataFromDataSource


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
    controller = GetDataFromDataSource(username=username)
    user_data = await controller.get_user_data()

    assert user_data.username == username
    assert user_data.name == result_data['name']


@mark.asyncio
async def test_repo_date():
    controller = GetDataFromDataSource(username='pity7736')
    repo_data = await controller.get_repo_data(name='nyoibo')

    assert repo_data.name == 'nyoibo'
    assert repo_data.private is False
    assert repo_data.description == 'Create automatically attribute accessor in ' \
                                    'Python.'
    assert repo_data.full_name == 'pity7736/nyoibo'
