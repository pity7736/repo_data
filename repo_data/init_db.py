from tortoise import Tortoise

from repo_data import settings


async def init_db():
    await Tortoise.init({
        'connections': {
            'default': {
                'engine': 'tortoise.backends.asyncpg',
                'credentials': {
                    'host': settings.REPO_DATA_HOST,
                    'port': settings.REPO_DATA_PORT,
                    'user': settings.REPO_DATA_USER,
                    'password': settings.REPO_DATA_PASSWORD,
                    'database': settings.REPO_DATA_DATABASE,
                }
            }
        },
        'apps': {
            'models': {
                'models': ['repo_data.models']
            }
        }
    })
