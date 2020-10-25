from tests.factories import UserFactory


def test_get_user(user_fixture, test_client):
    response = test_client.get(f'/api/users/{user_fixture.id}')
    data = response.json()

    assert response.status_code == 200
    assert data['data'] == {
        'user': {
            'id': user_fixture.id,
            'username': user_fixture.username,
            'name': user_fixture.name
        }
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

    response = test_client.get('/api/users', json={'username': user_fixture.username})
    data = response.json()

    assert response.status_code == 200
    assert data['data'] == {
        'users': [
            {
                'id': user_fixture.id,
                'username': user_fixture.username,
                'name': user_fixture.name
            }
        ]
    }


def test_search_by_two_fields(test_client, event_loop, user_fixture):
    create_user = UserFactory.create(username='qwerty', name='qwerty')
    event_loop.run_until_complete(create_user)

    response = test_client.get('/api/users', json={'username': user_fixture.username,
                                                   'name': user_fixture.name})
    data = response.json()

    assert response.status_code == 200
    assert data['data'] == {
        'users': [
            {
                'id': user_fixture.id,
                'username': user_fixture.username,
                'name': user_fixture.name
            }
        ]
    }


def test_search_users_without_results(test_client, db_connection):
    response = test_client.get('/api/users', json={'username': 'pity7736'})
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
            {
                'id': user0.id,
                'username': user0.username,
                'name': user0.name
            },
            {
                'id': user1.id,
                'username': user1.username,
                'name': user1.name
            },
        ]
    }


def test_search_by_non_existent_field(test_client, event_loop, user_fixture):
    response = test_client.get(
        '/api/users',
        json={'unknown_field': user_fixture.username}
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
        json={
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
