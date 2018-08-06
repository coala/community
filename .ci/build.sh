#!/bin/bash

set -e -x

mkdir private _site public

META_REVIEW_DATA="meta_review.json"

EXPORTED_DATA="static/tasks.yaml static/instances.yaml static/$META_REVIEW_DATA"

ISSUES_JSON="issues.json"

python manage.py fetch_deployed_data --allow-failure _site $EXPORTED_DATA

if [[ -n "$GCI_TOKEN" ]]; then
  python manage.py fetch_gci_task_data private
  python manage.py cleanse_gci_task_data private _site
  rm -rf private/
fi

# fetch deployed issues data in gh-board repo
python manage.py fetch_deployed_data _site $ISSUES_JSON --repo-name gh-board

python manage.py migrate
python manage.py import_contributors_data
python manage.py import_issues_data
python manage.py import_merge_requests_data
python manage.py import_openhub_data

if [[ -f "_site/$META_REVIEW_DATA" ]]; then
  echo "File $META_REVIEW_DATA exists."
  # Load meta_review data
  python manage.py loaddata _site/$META_REVIEW_DATA
else
  echo "File $META_REVIEW_DATA does not exist."
fi

# Run meta review system
python manage.py run_meta_review_system

rm _site/$ISSUES_JSON

# Dump meta_review data
python manage.py dumpdata meta_review > _site/$META_REVIEW_DATA

python manage.py collectstatic --noinput
python manage.py distill-local public --force
