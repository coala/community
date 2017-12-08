#!/bin/bash

regex="github.com/[a-z0-9A-Z]*"
git config -l | grep -o "$regex" | while read -r line ; do
    echo "${line:11}" | xargs echo -n > org_name.txt
done
