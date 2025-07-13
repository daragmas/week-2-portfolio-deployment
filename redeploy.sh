#!/bin/bash

# Go into folder
cd ./week-2-portfolio-deployment/

# Get updates
git fetch && git reset origin/main --hard

# Enter virtual env and install requirements
python3 -m venv python3-virtualenv
source python3-virtualenv/bin/activate
pip install -r requirements.txt

# Restart Service
systemctl daemon-reload
systemctl restart myportfolio

echo "deployed"