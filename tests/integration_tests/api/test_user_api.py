from tests.factories import UserFactory


def user_data(user):
    return {
        'id': user.id,
        'username': user.username,
        'name': user.name,
        'company': user.company,
        'blog': user.blog,
        'location': user.location,
        'email': user.email,
        'bio': user.bio,
    }


def test_get_user(user_fixture, test_client):
    response = test_client.get(f'/api/users/{user_fixture.id}')
    data = response.json()

    assert response.status_code == 200
    assert data['data'] == {
        'user': user_data(user_fixture)
    }


def test_get_non_existent_user(test_client, db_connection):
    response = test_client.get('/api/users/1')
    data = response.json()

    assert response.status_code == 404
    assert data['errors'] == [
        {
            'message': 'user not found'
        }
    ]


def test_search_users(test_client, event_loop, user_fixture):
    create_user = UserFactory.create(username='qwerty', name='qwerty')
    event_loop.run_until_complete(create_user)

    response = test_client.get('/api/users', params={'username': user_fixture.username})
    data = response.json()

    assert response.status_code == 200
    assert data['data'] == {
        'users': [
            user_data(user_fixture)
        ]
    }


def test_search_by_two_fields(test_client, event_loop, user_fixture):
    create_user = UserFactory.create(username='qwerty', name='qwerty')
    event_loop.run_until_complete(create_user)

    response = test_client.get('/api/users', params={'username': user_fixture.username,
                                                     'name': user_fixture.name})
    data = response.json()

    assert response.status_code == 200
    assert data['data'] == {
        'users': [
            user_data(user_fixture)
        ]
    }


def test_search_users_without_results(test_client, db_connection):
    response = test_client.get('/api/users', params={'username': 'pity7736'})
    data = response.json()

    assert response.status_code == 404
    assert data['data'] == {
        'users': []
    }
    assert data['errors'] == [
        {
            'message': 'users not found'
        }
    ]


def test_get_all_users(test_client, event_loop, db_connection):
    user0 = event_loop.run_until_complete(UserFactory.create(
        username='qwerty',
        name='qwerty'
    ))
    user1 = event_loop.run_until_complete(UserFactory.create(
        username='pity7736',
        name='julián'
    ))

    response = test_client.get('/api/users')
    data = response.json()

    assert response.status_code == 200
    assert data['data'] == {
        'users': [
            user_data(user0),
            user_data(user1),
        ]
    }


def test_search_by_non_existent_field(test_client, event_loop, user_fixture):
    response = test_client.get(
        '/api/users',
        params={'unknown_field': user_fixture.username}
    )
    data = response.json()

    assert response.status_code == 404
    assert data['data'] == {
        'users': []
    }
    assert data['errors'] == [
        {
            'message': 'users not found'
        }
    ]


def test_search_by_non_existent_fields(test_client, event_loop, user_fixture):
    response = test_client.get(
        '/api/users',
        params={
            'unknown_field0': user_fixture.username,
            'unknown_field1': 'whatever'
        }
    )
    data = response.json()

    assert response.status_code == 404
    assert data['data'] == {
        'users': []
    }
    assert data['errors'] == [
        {
            'message': 'users not found'
        }
    ]


def test_get_user_followers(test_client, event_loop, user_fixture):
    user0 = event_loop.run_until_complete(UserFactory.create(
        username='qwerty',
        name='qwerty'
    ))
    user1 = event_loop.run_until_complete(UserFactory.create(
        username='john_doe',
        name='john doe'
    ))
    event_loop.run_until_complete(user_fixture.followers.add(user0, user1))

    response = test_client.get(
        f'/api/users/{user_fixture.id}/followers',
    )
    data = response.json()

    assert response.status_code == 200
    assert data['data'] == {
        'followers': [
            user_data(user0),
            user_data(user1)
        ]
    }


def test_get_user_followers_with_wrong_id(test_client, event_loop, user_fixture):
    response = test_client.get(
        '/api/users/123/followers',
    )
    data = response.json()

    assert response.status_code == 404
    assert data['data'] == {
        'followers': []
    }
    assert data['errors'] == [
        {
            'message': 'user not found'
        }
    ]


def test_get_user_followingss(test_client, event_loop, user_fixture):
    user0 = event_loop.run_until_complete(UserFactory.create(
        username='qwerty',
        name='qwerty'
    ))
    user1 = event_loop.run_until_complete(UserFactory.create(
        username='john_doe',
        name='john doe'
    ))
    event_loop.run_until_complete(user_fixture.followings.add(user0, user1))

    response = test_client.get(
        f'/api/users/{user_fixture.id}/followings',
    )
    data = response.json()

    assert response.status_code == 200
    assert data['data'] == {
        'followings': [
            user_data(user0),
            user_data(user1)
        ]
    }


def test_get_user_followings_with_wrong_id(test_client, event_loop, user_fixture):
    response = test_client.get(
        '/api/users/123/followings',
    )
    data = response.json()

    assert response.status_code == 404
    assert data['data'] == {
        'followings': []
    }
    assert data['errors'] == [
        {
            'message': 'user not found'
        }
    ]
