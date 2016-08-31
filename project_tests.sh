#!/bin/bash
set -e

virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
pip install coveralls
cp example-settings.py settings.py
coverage run -m unittest discover tests "*_test.py"
COVERALLS_REPO_TOKEN=$(cat /etc/coveralls/tokens/elife-poa-xml-generation) coveralls
