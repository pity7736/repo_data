Repo data
=========

Installation
------------

Run `sh install.sh`.
This going to:

* Clone project
* Rename `env.sample` file to `.env`
* Rename `env.test.sample` file to `.env.test`
* Build docker images

Then, set right variable values.
GITHUB_TOKEN is optional but if you don't set, requests number are limited by github.

Run API web
-----------

* Run `docker-compose up`
* Check that everything is ok. Run `curl http://0.0.0.0:8000`


Testing
-------

Make sure the container is not running.
To run tests, you can run `sh run.sh tests_docker`


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

##### filter users

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
