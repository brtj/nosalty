#!/bin/bash

cd ..
venvPATH="$(pwd)"
cd nofluffscraper
appPATH="$(pwd)"
pythonENV="$venvPATH/venv/"
source $pythonENV/bin/activate

cities=(
    Rogozno
)
categories=(
    backend
    business-analyst
    business-intelligence
    devops
    frontend
    fullstack
    hr
    mobile
    other
    project-manager
    support
    testing
    ux
)

start_time="$(date -u +%s)"
for city in "${cities[@]}"; do
    for category in "${categories[@]}"; do
        $appPATH/nofluff.py --city=$city --category=$category
    done
done
end_time="$(date -u +%s)"
elapsed="$(($end_time-$start_time))"
echo "Total of $elapsed seconds elapsed for script"