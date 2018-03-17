#!/bin/bash

set -e -x

mkdir private _site public

scrapy crawl gsoc
if [[ -n "$GCI_TOKEN" ]]; then
  python manage.py fetch_gci_task_data private
  python manage.py cleanse_gci_task_data private _site
  rm -rf private/
else
  python manage.py fetch_old_gci_task_data _site || true
fi

python manage.py migrate
python manage.py import_contributors_data
python manage.py collectstatic --noinput
python manage.py distill-local public --force
