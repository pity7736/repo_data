from json.decoder import JSONDecodeError

from marshmallow import ValidationError
from starlette.responses import JSONResponse
from starlette.routing import Route
from tortoise.exceptions import FieldError

from repo_data.models import User, Repository
from tests.integration_tests.api.schemas import UserSchema, RepoSchema


async def get_user(request):
    user_id = request.path_params['id']
    user = await User.get_or_none(id=user_id)
    if user:
        user_data = UserSchema().dump(user)
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
        data = UserSchema().load(data)
    except ValidationError:
        users = []
    else:
        users = await User.filter(**data)

    response = {}
    status_code = 200
    users_data = UserSchema().dump(users, many=True)
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
        repo_data = RepoSchema().dump(repo)
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
    status_code = 200
    repos_data = RepoSchema().dump(repos, many=True)
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
    repos_data = RepoSchema().dump(repos, many=True)
    return JSONResponse({'data': {'repos': repos_data}}, status_code=status_code)


async def get_user_followers(request):
    user_id = request.path_params['id']
    user = await User.get_or_none(id=user_id)
    if user:
        followers = await user.followers.all()
        followers_data = UserSchema().dump(followers, many=True)
        return JSONResponse({'data': {'followers': followers_data}})
    return JSONResponse(
        {
            'data': {
                'followers': []
            },
            'errors': [
                {
                    'message': 'user not found'
                }
            ]
        },
        status_code=404
    )


async def get_user_followings(request):
    user_id = request.path_params['id']
    user = await User.get_or_none(id=user_id)
    if user:
        followings = await user.followings.all()
        followings_data = UserSchema().dump(followings, many=True)
        return JSONResponse({'data': {'followings': followings_data}})
    return JSONResponse(
        {
            'data': {
                'followings': []
            },
            'errors': [
                {
                    'message': 'user not found'
                }
            ]
        },
        status_code=404
    )


api_routes = [
    Route('/users', search_users),
    Route('/users/{id}', get_user),
    Route('/users/{id}/followers', get_user_followers),
    Route('/users/{id}/followings', get_user_followings),
    Route('/repos', search_repos),
    Route('/repos/{id}', get_repo),
    Route('/repos/owner/{id}', get_repos_by_owner),
]
