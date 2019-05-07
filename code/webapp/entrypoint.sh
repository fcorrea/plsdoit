#!/usr/bin/env bash

./wait-for-it.sh -t 60 db:3306

if [ -z "$APP_TEST" ]; then
    /entrypoint.sh /start.sh
else
    pytest app/
fi
