from repo_data.models import Repository
from tests.factories import RepositoryFactory


def repo_data(repo):
    return {
        'id': repo.id,
        'name': repo.name,
        'owner_url': f'/api/users/{repo.owner_id}',
        'private': repo.private,
        'full_name': repo.full_name,
        'description': repo.description,
        'language': repo.language
    }


def test_get_repo(repo_fixture: Repository, test_client):
    response = test_client.get(f'/api/repos/{repo_fixture.id}')
    data = response.json()

    assert response.status_code == 200
    assert data['data'] == {
        'repo': repo_data(repo_fixture)
    }


def test_get_non_existent_repo(db_connection, test_client):
    response = test_client.get('/api/repos/1')
    data = response.json()

    assert response.status_code == 404
    assert data['errors'] == [
        {
            'message': 'repo not found'
        }
    ]


def test_search_repos(test_client, repo_fixture: Repository, event_loop):
    event_loop.run_until_complete(RepositoryFactory.create(
        owner=repo_fixture.owner,
        name='test'
    ))
    response = test_client.get('/api/repos', json={'name': repo_fixture.name})
    data = response.json()

    assert response.status_code == 200
    assert data['data'] == {
        'repos': [
            repo_data(repo_fixture)
        ]
    }


def test_search_repo_without_results(test_client, db_connection):
    response = test_client.get('/api/repos', json={'name': 'nyoibo'})
    data = response.json()

    assert response.status_code == 404
    assert data['data'] == {
        'repos': []
    }
    assert data['errors'] == [
        {
            'message': 'repos not found'
        }
    ]


def test_get_all_repos(test_client, event_loop, repo_fixture: Repository):
    repo1 = event_loop.run_until_complete(RepositoryFactory.create(
        owner=repo_fixture.owner,
        name='test'
    ))

    response = test_client.get('/api/repos')
    data = response.json()

    assert response.status_code == 200
    assert data['data'] == {
        'repos': [
            repo_data(repo_fixture),
            repo_data(repo1)
        ]
    }


def test_search_by_non_existent_field(test_client, event_loop, db_connection):
    response = test_client.get(
        '/api/repos',
        json={'unknown_field': 'test'}
    )
    data = response.json()

    assert response.status_code == 404
    assert data['data'] == {
        'repos': []
    }
    assert data['errors'] == [
        {
            'message': 'unknown_field is/are not valid field(s)'
        },
        {
            'message': 'repos not found'
        }
    ]


def test_get_repos_by_owner_id(test_client, repo_fixture: Repository):
    response = test_client.get(f'/api/repos/owner/{repo_fixture.owner_id}')
    data = response.json()

    assert response.status_code == 200
    assert data['data'] == {
        'repos': [
            repo_data(repo_fixture)
        ]
    }


def test_get_repos_by_non_existent_owner_id(test_client, db_connection):
    response = test_client.get('/api/repos/owner/1')
    data = response.json()

    assert response.status_code == 404
    assert data['data'] == {
        'repos': []
    }


def test_get_some_repos_by_owner(test_client, event_loop, repo_fixture: Repository):
    event_loop.run_until_complete(RepositoryFactory.create(
        owner=repo_fixture.owner,
        name='test'
    ))
    response = test_client.get(
        f'/api/repos/owner/{repo_fixture.owner_id}',
        json={'name': repo_fixture.name}
    )
    data = response.json()

    assert response.status_code == 200
    assert data['data'] == {
        'repos': [
            repo_data(repo_fixture)
        ]
    }


def test_get_some_repos_by_owner_id(test_client, event_loop, repo_fixture: Repository):
    event_loop.run_until_complete(RepositoryFactory.create(
        owner=repo_fixture.owner,
        name='test'
    ))
    response = test_client.get(
        f'/api/repos/owner/{repo_fixture.owner_id}',
        json={
            'name': repo_fixture.name,
            'owner_id': repo_fixture.owner_id
        }
    )
    data = response.json()

    assert response.status_code == 200
    assert data['data'] == {
        'repos': [
            repo_data(repo_fixture)
        ]
    }
