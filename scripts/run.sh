#!/bin/sh

set -e

python manage.py wait_for_db
python manage.py collectstatic --noinput
python manage.py migrate

# 4 different workers are 4 instances ,
# --module defines the app name
uwsgi --socket :9000 --workers 4 --master --enable-threads --module app.wsgi