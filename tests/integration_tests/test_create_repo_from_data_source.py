from pytest import mark

from repo_data.controllers.create_repo_from_data_source import CreateRepoFromDataSource
from repo_data.models import User, Repository


@mark.asyncio
async def test_create_repo_with_existent_user(user_fixture: User):
    controller = CreateRepoFromDataSource(owner_username=user_fixture.username)
    await controller.create(name='nyoibo')

    repo = await Repository.get(name='nyoibo').prefetch_related('owner')
    assert repo.owner == user_fixture
    assert repo.name == 'nyoibo'
    assert repo.private is False
    assert repo.description == 'Create automatically attribute accessor in Python.'
    assert repo.language == 'Python'


@mark.asyncio
async def test_create_repo_with_non_existent_user(db_connection):
    username = 'pity7736'
    controller = CreateRepoFromDataSource(owner_username=username)
    await controller.create(name='nyoibo')

    repo = await Repository.get(name='nyoibo').prefetch_related('owner')
    assert repo.name == 'nyoibo'


@mark.asyncio
async def test_create_repo_that_already_exists_in_db(repo_fixture: Repository):
    owner = repo_fixture.owner
    controller = CreateRepoFromDataSource(owner_username=owner.username)
    await controller.create(name=repo_fixture.name)

    repo = await Repository.get(name=repo_fixture.name).prefetch_related('owner')
    assert repo.owner.username == owner.username
    assert repo.name == repo_fixture.name


@mark.asyncio
async def test_create_when_repo_non_exist_in_data_source(db_connection):
    repo_name = 'qwerty123'
    controller = CreateRepoFromDataSource(owner_username='pity7736')
    await controller.create(name=repo_name)

    repo = await Repository.get_or_none(name=repo_name)
    assert repo is None
