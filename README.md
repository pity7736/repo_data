Repo data
=========

Installation
------------

Run `sh install.sh`.
This going to:

* Clone project
* Rename `env.sample` file to `.env`
* Build docker images

Then, set right variable values.
GITHUB_TOKEN is optional but if you don't set, requests number are limited by github.

Run API web
-----------

* Run `docker-compose up`
* Check that everything is ok. Run `curl http://0.0.0.0:8000`


Testing
-------

To run tests, you can run `sh run.sh tests_docker`
