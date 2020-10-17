#!/usr/bin/env bash
pytest -s -vvv --cov=repo_data --cov-report term-missing tests/
