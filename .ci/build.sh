#!/bin/bash

set -e -x

mkdir _site public

python manage.py collectstatic --noinput
python manage.py distill-local public --force
