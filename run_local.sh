#!/bin/bash

docker run --env-file=env.list -p 8080:8080 -v $PWD/src:/app --rm --name nm nummet
