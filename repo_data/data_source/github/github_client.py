import httpx

from repo_data import settings


class GithubClient:
    _token = settings.GITHUB_TOKEN
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._client = httpx.AsyncClient()
        return cls._instance

    async def get_user(self, username: str):
        try:
            response = await self._client.get(
                f'https://api.github.com/users/{username}',
                headers={
                    'Authorization': f'token {self._token}'
                }
            )
        except httpx.RequestError:
            return {}
        if response.status_code == 200:
            return response.json()
        return {}

    async def get_repository(self, owner, name):
        try:
            response = await self._client.get(
                f'https://api.github.com/repos/{owner}/{name}',
                headers={
                    'Authorization': f'token {self._token}'
                }
            )
        except httpx.RequestError:
            return {}
        if response.status_code == 200:
            return response.json()
        return {}
