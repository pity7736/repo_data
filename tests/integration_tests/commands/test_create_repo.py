from pytest import mark

from repo_data.commands import CreateRepo
from repo_data.constanst import DataSourceEnum
from repo_data.models import Repository


@mark.asyncio
async def test_success(db_connection):
    username = 'pity7736'
    repo_name = 'nyoibo'
    command = CreateRepo(
        username=username,
        name=repo_name,
        data_source=DataSourceEnum.GITHUB.value,
    )
    await command.run()

    repo = await Repository.get(name=repo_name).prefetch_related('owner')

    assert repo.name == repo_name
    assert repo.owner.username == username
