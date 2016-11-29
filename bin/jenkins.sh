#! /usr/bin/env bash

env_dir="$JENKINS_HOME/virtualenv/${JOB_NAME// /_}"

#create and activate a virtualenv
virtualenv $env_dir
. $env_dir/bin/activate

#install requirements
pip3 install --upgrade pip==7.1.2
pyenv rehash && hash -r
pip3 install -r requirements.txt --upgrade

mkdir ../logs

./unit_test.sh

unit_test_pass=$?

./run_linting.sh

python_linting=$?

coverage xml
coverage -rm

e_code=$((unit_test_pass + python_linting))

exit $e_code
