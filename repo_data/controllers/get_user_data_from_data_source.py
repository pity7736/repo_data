from repo_data.data_source.github.github_data_source import GithubDataSource


class GetUserDataFromDataSource:

    def __init__(self, username: str):
        self._username = username

    async def get(self):
        get_user_data = GithubDataSource(username=self._username)
        return await get_user_data.get_user_data()
