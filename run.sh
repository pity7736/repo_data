#!/usr/bin/env bash

run_tests(){
  pytest -s -vvv --cov=repo_data --cov-report term-missing tests/
}

run_tests_docker(){
  docker-compose -f docker-compose.yml -f docker-compose-testing.yml run --rm repo_data pytest -s -vvv --cov=repo_data --cov-report term-missing tests/
}

run_api_web(){
  python main.py --run
}

run_xenon(){
  xenon -b B -m A -a A repo_data/
}

run_radon(){
  radon cc -a -s repo_data
}


main(){
  case $1 in
    tests)
      echo "running tests"
      run_tests
      ;;
    tests_docker)
      echo "running tests on docker"
      run_tests_docker
      ;;
    api_web)
      echo "running api web"
      run_api_web
      ;;
    xenon)
      echo "running xenon"
      run_xenon
      ;;
    radon)
      echo "running radon"
      run_radon
      ;;
  esac
}
main $1
