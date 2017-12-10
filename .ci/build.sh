#!/bin/bash

set -e -x

bash orgname.sh

mkdir _site public

python activity/scraper.py || true

python manage.py collectstatic --noinput
python manage.py distill-local public --force
