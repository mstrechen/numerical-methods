#!/bin/bash
git pull

docker build -t nummethods/web .
docker stop nummethods

docker run --rm -p 80:8080 -d --name nummethods nummethods/web
