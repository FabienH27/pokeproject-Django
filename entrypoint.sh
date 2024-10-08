#!/bin/sh

python manage.py migrate

echo "Starting Django app on port ${PORT:-8000}"

# Start the server
exec python manage.py runserver 0.0.0.0:${PORT:-8000}
