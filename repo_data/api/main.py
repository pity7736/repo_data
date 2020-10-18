from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route, Mount

from repo_data.api.app import api_routes


async def hello_world(request):
    return JSONResponse({'hello': 'world'})


app = Starlette(
    debug=True,
    routes=[
        Route('/', hello_world),
        Mount('/api', routes=api_routes)
    ]
)
