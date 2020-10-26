Repo data
=========

Installation
------------

Run `sh install.sh`.
This going to:

* Rename `env.sample` file to `.env`
* Rename `env.test.sample` file to `.env.test`
* Build docker images

Optional, set right variable values (with sample variables should work fine).
GITHUB_TOKEN is optional but if you don't set, requests number are limited by github.

Run API web
-----------

* Run `docker-compose up`
* Check that everything is ok. Run `curl http://0.0.0.0:8000`


Testing
-------

Make sure the container is not running.
To run tests, you can run `sh run.sh tests_docker`


Getting repository and user data
--------------------------------

There is a CLI tool to get data from data source. You need to have container running.
You can do it running `docker-compose up`.
To get help about tool you can run `sh run_command_on_container.sh -h`

All following command are on `run_command_on_container.sh` file.

#### Create user

This command get user data from data source and stores in DB.

    -cu username

    or

    --create-user username

To create followers too, you can add `-cfr` or `--create-followers` option.
This going to get followers user and store in DB. Example:

    -cu pity7736 -cfr

Also, you can create followings adding `-cfg`  or `--create-followings` option.
Example:

    -cu pity7736 -cfg

To create user, followers and followings, you can put all together. Example:

    -cu pity736 -cfr -cfg


#### Create repository

This command get repository and owner data from data source and stores in DB.

    -cr owner repo_name

    or

    --create-repo owner repo_name

Example:

    -cr pity7736 nyoibo


API Documentation
-----------------

This service expose an API query to get repository and user data.
Base url: http://0.0.0.0:8000/api

#### List users

Resource: /users

Example: `curl {base_url}/users`

Response:

    {
        "data": {
            "users": [
                {
                    "company":"R5",
                    "bio":"I'm python backend developer at https://www.grupor5.com/",
                    "name":"julián cortés",
                    "username":"pity7736",
                    "blog":"",
                    "location":"Bogotá D.C - Colombia",
                    "email":"pity7736@gmail.com",
                    "id":1
                }
            ]
        }
    }

#### Filter users

Resource: /users

Example: `curl {base_url}/users?username=pity7736`

Response: same above

If users are not found, the status code will be 404.


#### Get user

Resource: /users/{user_id}

Example: `curl {base_url}/users/1`

Response:

    {
        "data": {
            "user":{
                "company":"R5",
                "bio":"I'm python backend developer at https://www.grupor5.com/",
                "name":"julián cortés",
                "username":"pity7736",
                "blog":"",
                "location":"Bogotá D.C - Colombia",
                "email":"pity7736@gmail.com","id":1
            }
        }
    }

#### Get user followers

Resource: /users/{user_id}/followers

Example: `curl {base_url}/1/followers`

Response:

    {
        "data": {
            "followers": [
                {
                    "company":"R5",
                    "bio":"I'm python backend developer at https://www.grupor5.com/",
                    "name":"julián cortés",
                    "username":"pity7736",
                    "blog":"",
                    "location":"Bogotá D.C - Colombia",
                    "email":"pity7736@gmail.com","id":1
                }
            ]
        }
    }

#### Get user followings

Resource: /users/{user_id}/followings

Example: `curl {base_url}/1/followings`

Response:

    {
        "data": {
            "followings": [
                {
                    "company":"R5",
                    "bio":"I'm python backend developer at https://www.grupor5.com/",
                    "name":"julián cortés",
                    "username":"pity7736",
                    "blog":"",
                    "location":"Bogotá D.C - Colombia",
                    "email":"pity7736@gmail.com","id":1
                }
            ]
        }
    }


#### List repositories

Resource: /repos

Example: `curl {base_url}/repos`

Response:

    {
        "data": {
            "repos": [
                {
                    "language":"Python",
                    "name":"kinton-orm",
                    "description":"Async data access layer",
                    "private":false,
                    "owner_url":"/api/users/1",
                    "full_name":"pity7736/kinton-orm",
                    "id":1
                }
            ]
        }
    }


#### Search repositories

Resource: /repos

Example: `curl {base_url}/repos?name=kinton-orm`

Response: same above


#### Get repository

Resource: /repos/{repo_id}

Example: `curl {base_url}/repos/1`

Response:

    {
        "data": {
            "repo": {
                "language":"Python",
                "name":"kinton-orm",
                "description":"Async data access layer",
                "private":false,
                "owner_url":"/api/users/1",
                "full_name":"pity7736/kinton-orm",
                "id":1
            }
        }
    }


#### Get repositories by owner

Resource: /repos/owner/{owner_id}

Example: `curl {base_url}/repos/owner/1`

Response:

    {
        "data": {
            "repos": [
                {
                    "language":"Python",
                    "name":"kinton-orm",
                    "description":"Async data access layer",
                    "private":false,
                    "owner_url":"/api/users/1",
                    "full_name":"pity7736/kinton-orm",
                    "id":1
                }
            ]
        }
    }
