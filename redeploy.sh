#!/bin/bash

cd ./week-2-portfolio-deployment/

git fetch && git reset origin/main --hard

cd ./week-2-portfolio-deployment/
python3 -m venv python3-virtualenv
source python3-virtualenv/bin/activate
pip install -r requirements.txt
systemctl daemon-reload
systemctl restart myportfolio

echo "deployed"