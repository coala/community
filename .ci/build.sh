#!/bin/bash

set -e -x

mkdir private _site public

python manage.py fetch_gci_task_data private
python manage.py cleanse_gci_task_data private _site

python manage.py collectstatic --noinput
python manage.py distill-local public --force
