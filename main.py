import argparse
import asyncio
import sys

import uvicorn
from dotenv import load_dotenv


def run():
    uvicorn.run('repo_data:app', host='0.0.0.0', port=8000, reload=True)


async def _initialize():
    load_dotenv()
    from repo_data import init_db
    await init_db()


async def create_user(username, create_followers, create_followings):
    await _initialize()
    from repo_data.commands import CreateUser
    print('creating user with username', username, create_followers, create_followings)
    command = CreateUser(
        username=username,
        data_source='github',
        create_followers=create_followers,
        create_followings=create_followings
    )
    await command.run()


async def create_repo(owner, name):
    await _initialize()
    from repo_data.commands import CreateRepo
    print('creating repo', name, owner)
    command = CreateRepo(
        username=owner,
        name=name,
        data_source='github'
    )
    await command.run()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='repo data arguments')
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
    parser.add_argument(
        '-cfr',
        '--create-followers',
        help='create user followers',
        action='store_true'
    )
    parser.add_argument(
        '-cfg',
        '--create-followings',
        help='create user followings',
        action='store_true'
    )
    args = parser.parse_args()
    if args.run:
        run()
    elif args.create_user:
        asyncio.run(create_user(
            args.create_user,
            args.create_followers,
            args.create_followings
        ))
    elif args.create_repo:
        asyncio.run(create_repo(*args.create_repo))
    else:
        print('not argument given')
        sys.exit(1)
