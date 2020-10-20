import asyncio

from dotenv import load_dotenv
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route, Mount
from tortoise import Tortoise

from repo_data.init_db import init_db
from repo_data.api.views import api_routes


async def hello_world(request):
    return JSONResponse({'hello': 'world'})


async def _initializer(attempt=1):
    print('loading envvars')
    load_dotenv()
    try:
        print('init db, attempt', attempt)
        await init_db()
        await Tortoise.generate_schemas()
    except ConnectionRefusedError:
        print('connection error')
        if attempt < 4:
            attempt += 1
            print(f'sleeping {attempt} seconds')
            await asyncio.sleep(attempt)
            print('retrying...')
            return await _initializer(attempt)
        raise
    else:
        print('db initialized!')


app = Starlette(
    debug=True,
    routes=[
        Route('/', hello_world),
        Mount('/api', routes=api_routes)
    ],
    on_startup=[_initializer]
)
