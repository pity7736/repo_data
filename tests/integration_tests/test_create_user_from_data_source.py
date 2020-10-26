from pytest import mark

from repo_data.controllers import CreateUserFromDataSource
from repo_data.data_source.github.github_data_source import GithubDataSource
from repo_data.models import User
from tests.factories import UserFactory

username_values = (
    (
        'pity7736',
        {
            'name': 'julián cortés',
            'followers_number': 11,
            'followings_number': 7,
            'data_source_id': '4231101',
            "company": "R5",
            "blog": "",
            "location": "Bogotá D.C - Colombia",
            "email": 'pity7736@gmail.com',
            "bio": "I'm python backend developer at https://www.grupor5.com/"
        }
    ),
    (
        'Danjavia',
        {
            'name': 'danny hoower antonio viasus avila',
            'followers_number': 9,
            'followings_number': 15,
            'data_source_id': '1041322',
            "company": "StronGo Atrio Technologies, Inc",
            "blog": "https://twitter.com/danjavia",
            "location": "Bogota - Colombia",
            "email": 'danjavia@gmail.com',
            "bio": "Happy coding and launching ideas to the space!",
        }
    )
)


@mark.parametrize('username, result_data', username_values)
@mark.asyncio
async def test_success(db_connection, username, result_data):
    data_source = GithubDataSource(username=username)
    controller = CreateUserFromDataSource(data_source=data_source)
    created_user = await controller.create(
        create_followers=True,
        create_followings=True
    )

    user = await User.get(username=username)
    followers_number = await user.followers.all().count()
    followings_number = await user.followings.all().count()
    assert created_user == user
    assert user.username == username
    assert user.name == result_data['name']
    assert user.data_source_id == result_data['data_source_id']
    assert followers_number == result_data['followers_number']
    assert followings_number == result_data['followings_number']
    assert user.company == result_data['company']
    assert user.blog == result_data['blog']
    assert user.location == result_data['location']
    assert user.email == result_data['email']
    assert user.bio == result_data['bio']


@mark.asyncio
async def test_when_user_not_exists_in_data_source(db_connection):
    username = 'non_existent_user'
    data_source = GithubDataSource(username=username)
    controller = CreateUserFromDataSource(data_source=data_source)
    created_user = await controller.create()

    user = await User.filter(username=username).first()

    assert user is None
    assert created_user is None


@mark.asyncio
async def test_create_user_when_user_already_exists_in_db(db_connection):
    user_fixture = await UserFactory.create(data_source_id='4231101')
    data_source = GithubDataSource(username=user_fixture.username)
    controller = CreateUserFromDataSource(data_source=data_source)
    created_user = await controller.create()

    user = await User.get(username=user_fixture.username)
    assert created_user == user
    assert user.username == user_fixture.username
    assert user.name == user_fixture.name
    assert user.data_source_id == user_fixture.data_source_id
