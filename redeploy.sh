#!/bin/bash

tmux kill-sessions

cd ./week-2-portfolio-deployment/

git fetch && git reset origin/main --hard

tmux new-session -d -s 'portfolio'
tmux send-keys 'cd ./week-2-portfolio-deployment/' C-m
sleep 1
tmux send-keys 'python3 -m venv python3-virtualenv' C-m
sleep 1
tmux send-keys 'source python3-virtualenv/bin/activate' C-m
sleep 1
tmux send-keys 'pip install -r requirements.txt' C-m
sleep 1
tmux send-keys 'flask run --host=0.0.0.0' C-m
echo "deployed"