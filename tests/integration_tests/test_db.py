from pytest import mark

from repo_data.models import User


@mark.asyncio
async def test_query(db_connection):
    assert await User.all() == []
