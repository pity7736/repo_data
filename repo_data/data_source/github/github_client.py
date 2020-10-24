import httpx

from repo_data import settings


class GithubClient:
    __slots__ = ()
    _token = settings.GITHUB_TOKEN
    _base_url = 'https://api.github.com'

    def get_user(self, username: str):
        return self._send_request(f'/users/{username}')

    def get_repository(self, owner, name):
        return self._send_request(f'/repos/{owner}/{name}')

    async def _send_request(self, resource):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f'{self._base_url}{resource}',
                    headers={
                        'Authorization': f'token {self._token}'
                    }
                )
        except httpx.RequestError:
            return {}
        if response.status_code == 200:
            return response.json()
        return {}
