from repo_data.data_source.github.get_user_data import GetUserData as GetGithubData


class GetUserData:

    def __init__(self, username: str):
        self._username = username

    async def get(self):
        get_user_data = GetGithubData(username=self._username)
        return await get_user_data.get()
