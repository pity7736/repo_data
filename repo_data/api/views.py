import logging
from json.decoder import JSONDecodeError

from marshmallow import ValidationError
from starlette.responses import JSONResponse
from starlette.routing import Route
from tortoise.exceptions import FieldError

from repo_data.models import User, Repository
from tests.integration_tests.api.schemas import UserSchema, RepoSchema


logger = logging.getLogger('repo_data')


async def get_user(request):
    user_id = request.path_params['id']
    logger.info('user id: %s', user_id)
    user = await User.get_or_none(id=user_id)
    if user:
        user_data = UserSchema().dump(user)
        logger.debug('user data response: %s', user_data)
        return JSONResponse({'data': {'user': user_data}})
    logger.warning('user not found!')
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
        data = request.query_params
        logger.info('query params: %s', data)
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
        logger.warning('users not found!')
    logger.debug('users data response: %s', users_data)
    response['data'] = {'users': users_data}
    return JSONResponse(response, status_code=status_code)


async def get_repo(request):
    repo_id = request.path_params['id']
    logger.info('repo id: %s', repo_id)
    repo = await Repository.get_or_none(id=repo_id)
    if repo:
        repo_data = RepoSchema().dump(repo)
        return JSONResponse({'data': {'repo': repo_data}})
    logger.warning('repo not found!')
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
        data = request.query_params
        logger.info('query params: %s', data)
    except JSONDecodeError:
        logger.error('bat query params')
        data = {}
    try:
        repos = await Repository.filter(**data)
    except FieldError:
        logger.error('invalid filters')
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
        logger.error('repo not found!')
    logger.debug('repo data response: %s', repos_data)
    response['data'] = {'repos': repos_data}
    return JSONResponse(response, status_code=status_code)


async def get_repos_by_owner(request):
    owner_id = request.path_params['id']
    logger.info('owner id: %s', owner_id)
    try:
        data = dict(request.query_params)
    except JSONDecodeError:
        logger.error('bad query param!')
        data = {}
    data['owner_id'] = owner_id
    repos = await Repository.filter(**data)
    status_code = 200 if repos else 404
    repos_data = RepoSchema().dump(repos, many=True)
    logger.debug('repo data response: %s', repos_data)
    return JSONResponse({'data': {'repos': repos_data}}, status_code=status_code)


async def get_user_followers(request):
    user_id = request.path_params['id']
    logger.info('user id: %s', user_id)
    user = await User.get_or_none(id=user_id)
    if user:
        followers = await user.followers.all()
        followers_data = UserSchema().dump(followers, many=True)
        logger.debug('followers data %s', followers_data)
        return JSONResponse({'data': {'followers': followers_data}})
    logger.warning('user not found!')
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
    logger.info('user id: %s', user_id)
    user = await User.get_or_none(id=user_id)
    if user:
        followings = await user.followings.all()
        followings_data = UserSchema().dump(followings, many=True)
        logger.debug('followings data %s', followings_data)
        return JSONResponse({'data': {'followings': followings_data}})
    logger.warning('user not found!')
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
