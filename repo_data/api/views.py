from json.decoder import JSONDecodeError

from starlette.responses import JSONResponse
from starlette.routing import Route
from tortoise.exceptions import FieldError

from repo_data.models import User, Repository


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


async def get_repo(request):
    repo_id = request.path_params['id']
    repo = await Repository.get_or_none(id=repo_id)
    if repo:
        repo_data = {
            'id': repo.id,
            'name': repo.name,
            'owner_url': f'/api/users/{repo.owner_id}'
        }
        return JSONResponse({'data': {'repo': repo_data}})
    return JSONResponse(
        {
            'errors': [
                {
                    'message': 'repo not found'
                }
            ]
        },
        status_code=404
    )


async def search_repos(request):
    errors = []
    try:
        data = await request.json()
    except JSONDecodeError:
        data = {}
    try:
        repos = await Repository.filter(**data)
    except FieldError:
        fields = ', '.join(data.keys())
        errors.append({'message': f'{fields} is/are not valid field(s)'})
        repos = []

    response = {}
    repos_data = []
    status_code = 200
    for repo in repos:
        repos_data.append({
            'id': repo.id,
            'name': repo.name,
            'owner_url': f'/api/users/{repo.owner_id}',
        })
    if not repos_data:
        status_code = 404
        errors.append({'message': 'repos not found'})
        response['errors'] = errors
    response['data'] = {'repos': repos_data}
    return JSONResponse(response, status_code=status_code)


async def get_repos_by_owner(request):
    owner_id = request.path_params['id']
    try:
        data = await request.json()
    except JSONDecodeError:
        data = {}
    data['owner_id'] = owner_id
    repos = await Repository.filter(**data)
    status_code = 200 if repos else 404
    repos_data = []
    for repo in repos:
        repos_data.append({
            'id': repo.id,
            'name': repo.name,
            'owner_url': f'/api/users/{repo.owner_id}',
        })
    return JSONResponse({'data': {'repos': repos_data}}, status_code=status_code)


api_routes = [
    Route('/users', search_users),
    Route('/users/{id}', get_user),
    Route('/repos', search_repos),
    Route('/repos/{id}', get_repo),
    Route('/repos/owner/{id}', get_repos_by_owner),
]
