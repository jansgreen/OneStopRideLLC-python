#!/bin/sh

if [ "$DEBUG" = "False" ]; then
        FLASK_ENV="development"
        python run.py
else
        gunicorn app:app
fi
