from repo_data.data_source.github.github_data_source import GithubDataSource


class GetDataFromDataSource:

    def __init__(self, username: str):
        self._username = username

    async def get_user_data(self):
        get_user_data = GithubDataSource(username=self._username)
        return await get_user_data.get_user_data()

    async def get_repo_data(self, name):
        data_source = GithubDataSource(username=self._username)
        return await data_source.get_repo_data(name=name)
