import os

import httpx


class GithubClient:

    async def get_user(self, username: str):
        token = os.environ['GITHUB_TOKEN']
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
