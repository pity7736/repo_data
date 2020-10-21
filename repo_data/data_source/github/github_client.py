import httpx

from repo_data import settings


class GithubClient:

    async def get_user(self, username: str):
        token = settings.GITHUB_TOKEN
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f'https://api.github.com/users/{username}',
                    headers={
                        'Authorization': f'token {token}'
                    }
                )
            except httpx.RequestError:
                return {}
        if response.status_code == 200:
            return response.json()
        return {}

    async def get_repository(self, owner, name):
        token = settings.GITHUB_TOKEN
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f'https://api.github.com/repos/{owner}/{name}',
                    headers={
                        'Authorization': f'token {token}'
                    }
                )
            except httpx.RequestError:
                return {}
        if response.status_code == 200:
            return response.json()
        return {}
