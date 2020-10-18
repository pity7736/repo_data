from pytest import fixture
from starlette.testclient import TestClient

from repo_data.api import app
from repo_data.models import User


@fixture
def test_client():
    return TestClient(app=app)


def test_get_user(event_loop, test_client, db_connection):
    user = event_loop.run_until_complete(User.create(username='pity7736',
                                                     name='julián'))

    response = test_client.get(f'/api/users/{user.id}')
    data = response.json()

    assert response.status_code == 200
    assert data['data'] == {
        'user': {
            'id': user.id,
            'username': user.username,
            'name': user.name
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


def test_search_users(test_client, event_loop, db_connection):
    event_loop.run_until_complete(User.create(username='qwerty', name='qwerty'))
    user = event_loop.run_until_complete(User.create(username='pity7736',
                                                     name='julián'))

    response = test_client.get('/api/users', json={'username': 'pity7736'})
    data = response.json()

    assert response.status_code == 200
    assert data['data'] == {
        'users': [
            {
                'id': user.id,
                'username': user.username,
                'name': user.name
            }
        ]
    }


def test_search_by_two_fields(test_client, event_loop, db_connection):
    event_loop.run_until_complete(User.create(username='qwerty', name='qwerty'))
    user = event_loop.run_until_complete(User.create(username='pity7736',
                                                     name='julián'))

    response = test_client.get('/api/users', json={'username': 'pity7736',
                                                   'name': 'julián'})
    data = response.json()

    assert response.status_code == 200
    assert data['data'] == {
        'users': [
            {
                'id': user.id,
                'username': user.username,
                'name': user.name
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
    user0 = event_loop.run_until_complete(User.create(username='qwerty', name='qwerty'))
    user1 = event_loop.run_until_complete(User.create(username='pity7736',
                                                      name='julián'))

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


def test_search_by_non_existent_field(test_client, event_loop, db_connection):
    event_loop.run_until_complete(User.create(username='qwerty', name='qwerty'))
    response = test_client.get('/api/users', json={'unknown_field': 'pity7736'})
    data = response.json()

    assert response.status_code == 404
    assert data['data'] == {
        'users': []
    }
    assert data['errors'] == [
        {
            'message': 'unknown_field is/are not valid field(s)'
        },
        {
            'message': 'users not found'
        }
    ]


def test_search_by_non_existent_fields(test_client, event_loop, db_connection):
    event_loop.run_until_complete(User.create(username='qwerty', name='qwerty'))
    response = test_client.get('/api/users', json={'unknown_field0': 'pity7736',
                                                   'unknown_field1': 'whatever'})
    data = response.json()

    assert response.status_code == 404
    assert data['data'] == {
        'users': []
    }
    assert data['errors'] == [
        {
            'message': 'unknown_field0, unknown_field1 is/are not valid field(s)'
        },
        {
            'message': 'users not found'
        }
    ]
