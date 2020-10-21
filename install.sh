#!/usr/bin/env bash

git clone git@github.com:pity7736/repo_data.git
mv env.sampe .env
chmod +x run.sh
docker-compose build
docker-compose -f docker-compose.yml -f docker-compose-testing.yml build
