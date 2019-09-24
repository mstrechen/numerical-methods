#!/bin/bash

if [ "$DEBUG" == "TRUE" ]
then
  echo "DEBUG MODE ON"
  gunicorn --reload -b 0.0.0.0:8080 -w 3 app:app
else
  gunicorn -b 0.0.0.0:80 -w 3 app:app
fi
