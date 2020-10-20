import argparse
import asyncio
import sys

import uvicorn
from dotenv import load_dotenv

from repo_data import init_db
from repo_data.controllers import CreateUserFromDataSource
from repo_data.controllers.create_repo_from_data_source import CreateRepoFromDataSource


def run():
    uvicorn.run('repo_data:app', host='0.0.0.0', port=8000, reload=True)


async def create_user(username):
    load_dotenv()
    await init_db()
    print('creating user with username', username)
    controller = CreateUserFromDataSource(username=username)
    await controller.create()


async def create_repo(owner, name):
    load_dotenv()
    await init_db()
    print('creating repo', name, owner)
    controller = CreateRepoFromDataSource(owner_username=owner)
    await controller.create(name=name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='read data arguments')
    parser.add_argument('-r', '--run', action='store_true', help='run API service')
    parser.add_argument(
        '-cu',
        '--create-user',
        metavar='username',
        help='create user given username'
    )
    parser.add_argument(
        '-cr',
        '--create-repo',
        nargs=2,
        metavar=('owner username', 'repo name'),
        help='create repository given owner username and repo name',
    )
    args = parser.parse_args()
    if args.run:
        run()
    elif args.create_user:
        asyncio.run(create_user(args.create_user))
    elif args.create_repo:
        asyncio.run(create_repo(*args.create_repo))
    else:
        print('not argument given')
        sys.exit(1)
