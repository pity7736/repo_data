from dotenv import load_dotenv
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route, Mount

from repo_data.init_db import init_db
from repo_data.api.views import api_routes


async def hello_world(request):
    return JSONResponse({'hello': 'world'})


async def _initializer():
    load_dotenv()
    await init_db()


app = Starlette(
    debug=True,
    routes=[
        Route('/', hello_world),
        Mount('/api', routes=api_routes)
    ],
    on_startup=[_initializer]
)
