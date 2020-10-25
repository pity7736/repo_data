import argparse
import asyncio
import sys

import uvicorn
from dotenv import load_dotenv

from repo_data import init_db
from repo_data.commands import CreateUser, CreateRepo


def run():
    uvicorn.run('repo_data:app', host='0.0.0.0', port=8000, reload=True)


async def _initialize():
    load_dotenv()
    await init_db()


async def create_user(username):
    await _initialize()
    print('creating user with username', username)
    command = CreateUser(username=username, data_source='github')
    await command.run()


async def create_repo(owner, name):
    await _initialize()
    print('creating repo', name, owner)
    command = CreateRepo(
        username=owner,
        name=name,
        data_source='github'
    )
    await command.run()


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
