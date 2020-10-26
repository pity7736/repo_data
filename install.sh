#!/usr/bin/env bash

cp env.sample .env
cp env.test.sample .env.test
chmod +x run.sh
chmod +x run_command_on_container.sh
docker-compose build
docker-compose -f docker-compose.yml -f docker-compose-testing.yml build
