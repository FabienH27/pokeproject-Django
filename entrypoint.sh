#!/bin/sh

python manage.py migrate

# Start the server
exec "$@"