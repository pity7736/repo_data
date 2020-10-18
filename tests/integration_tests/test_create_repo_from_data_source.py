from pytest import mark

from repo_data.controllers.create_repo_from_data_source import CreateRepoFromDataSource
from repo_data.models import User, Repository


@mark.asyncio
async def test_create_repo_with_existent_user(db_connection):
    user = await User.create(username='pity7736', name='julián')
    controller = CreateRepoFromDataSource(owner_username='pity7736')
    await controller.create(name='nyoibo')

    repo = await Repository.get(name='nyoibo').prefetch_related('owner')
    assert repo.owner == user
    assert repo.name == 'nyoibo'


@mark.asyncio
async def test_create_repo_with_non_existent_user(db_connection):
    username = 'pity7736'
    controller = CreateRepoFromDataSource(owner_username=username)
    await controller.create(name='nyoibo')

    repo = await Repository.get(name='nyoibo').prefetch_related('owner')
    assert repo.owner.username == username
    assert repo.name == 'nyoibo'


@mark.asyncio
async def test_create_repo_that_already_exists_in_db(db_connection):
    username = 'pity7736'
    repo_name = 'nyoibo'
    user = await User.create(username=username, name='julián')
    await Repository.create(name=repo_name, owner=user)

    controller = CreateRepoFromDataSource(owner_username=username)
    await controller.create(name=repo_name)

    repo = await Repository.get(name='nyoibo').prefetch_related('owner')
    assert repo.owner.username == username
    assert repo.name == 'nyoibo'


@mark.asyncio
async def test_create_when_repo_non_exist_in_data_source(db_connection):
    repo_name = 'qwerty123'
    controller = CreateRepoFromDataSource(owner_username='pity7736')
    await controller.create(name=repo_name)

    repo = await Repository.get_or_none(name=repo_name)
    assert repo is None
