from json.decoder import JSONDecodeError

from starlette.responses import JSONResponse
from starlette.routing import Route
from tortoise.exceptions import FieldError

from repo_data.models import User


async def get_user(request):
    user_id = request.path_params['id']
    user = await User.get_or_none(id=user_id)
    if user:
        user_data = {
            'id': user.id,
            'username': user.username,
            'name': user.name
        }
        return JSONResponse({'data': {'user': user_data}})
    return JSONResponse(
        {
            'errors': [
                {
                    'message': 'user not found'
                }
            ]
        },
        status_code=404
    )


async def search_users(request):
    errors = []
    try:
        data = await request.json()
    except JSONDecodeError:
        data = {}
    try:
        users = await User.filter(**data)
    except FieldError:
        fields = ', '.join(data.keys())
        errors.append({'message': f'{fields} is/are not valid field(s)'})
        users = []

    response = {}
    users_data = []
    status_code = 200
    for user in users:
        users_data.append({
            'id': user.id,
            'username': user.username,
            'name': user.name
        })
    if not users_data:
        status_code = 404
        errors.append({'message': 'users not found'})
        response['errors'] = errors
    response['data'] = {'users': users_data}
    return JSONResponse(response, status_code=status_code)


api_routes = [
    Route('/users', search_users),
    Route('/users/{id}', get_user),
]
