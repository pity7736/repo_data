import os

from tortoise import Tortoise


async def init_db():
    await Tortoise.init({
        'connections': {
            'default': {
                'engine': 'tortoise.backends.asyncpg',
                'credentials': {
                    'host': os.environ['REPO_DATA_HOST'],
                    'port': os.environ['REPO_DATA_PORT'],
                    'user': os.environ['REPO_DATA_USER'],
                    'password': os.environ['REPO_DATA_PASSWORD'],
                    'database': os.environ['REPO_DATA_DATABASE'],
                }
            }
        },
        'apps': {
            'models': {
                'models': ['repo_data.models']
            }
        }
    })
