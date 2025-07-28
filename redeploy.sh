#!/bin/bash

# Get updates
git fetch && git reset origin/main --hard

docker compose -f docker-compose.prod.yml down 

docker compose -f docker-compose.prod.yml up -d --build