import httpx

from repo_data import settings


class GithubClient:
    __slots__ = ('_headers',)
    _base_url = 'https://api.github.com'

    def __init__(self):
        headers = {}
        if settings.GITHUB_TOKEN:
            headers = {'Authorization': f'token {settings.GITHUB_TOKEN}'}
        self._headers = headers

    def get_user(self, username: str):
        return self._send_request(f'/users/{username}')

    def get_repository(self, owner, name):
        return self._send_request(f'/repos/{owner}/{name}')

    def get_user_followers(self, username: str):
        return self._send_request(f'/users/{username}/followers')

    def get_user_followings(self, username: str):
        return self._send_request(f'/users/{username}/following')

    async def _send_request(self, resource):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f'{self._base_url}{resource}',
                    headers=self._headers
                )
        except httpx.RequestError:
            return {}
        if response.status_code == 200:
            return response.json()
        return {}
