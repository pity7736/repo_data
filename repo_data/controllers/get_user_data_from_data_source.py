from repo_data.data_source.github.get_user_data_from_github import GetUserDataFromGithub


class GetUserDataFromDataSource:

    def __init__(self, username: str):
        self._username = username

    async def get(self):
        get_user_data = GetUserDataFromGithub(username=self._username)
        return await get_user_data.get()
