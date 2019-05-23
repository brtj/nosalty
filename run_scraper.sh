#!/bin/bash


appPATH="$(pwd)"
pythonENV="$appPATH/venv/"
source $pythonENV/bin/activate

cities=(
     Poznan
     Wroclaw
     Gdansk
     Lodz
     Gdynia
     Lublin
     Katowice
     Trojmiasto
     Gliwice
     Krakow
     Warszawa
)
categories=(
    devops
    backend
    fullstack
    frontend
    mobile
    testing
    support
    project-manager
    hr
    ux
    business-analyst
    business-intelligence
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