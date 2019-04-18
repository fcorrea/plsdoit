#!/usr/bin/env bash

./wait-for-it.sh -t 60 db:3306

if [ -z "$APP_TEST" ]; then
    FLASK_APP=app/app.py flask run --host=0.0.0.0
else
    pytest
fi
