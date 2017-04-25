#!/bin/bash

pull_locations[0]="/home/kyle/scripts/";
push_locations[0]="scripts";
pull_locations[1]="/home/kyle/.thunderbird/";
push_locations[1]="thunderbird";
pull_locations[2]="/home/kyle/code/";
push_locations[2]="code";
pull_locations[3]="/home/kyle/Documents/";
push_locations[3]="Documents";
pull_locations[4]="/home/kyle/.ssh/";
push_locations[4]="ssh";
pull_locations[5]="/home/kyle/.gnupg/";
push_locations[5]="gnupg";

base_path="/media/kyle/Pepper (1TB)/Backups/"

"$base_path"  2> /dev/null
media_attached=$?
# 126 returned if directory exists, 127 if it does not.
if [ "$media_attached" -eq "126" ]; then
    echo "Backup media found!"
    for i in `seq 0 5`;
    do
        pull=${pull_locations[$i]}
        push=${push_locations[$i]}
        today=`date +%Y-%m-%d_%H-%M-%S`
        push_full_path="$base_path""$push/$today-$push/"
        echo $push_full_path
        mkdir "$push_full_path"
        echo "$push_full_path"
        cp -r "$pull" "$push_full_path$push"
    done
else
    echo "No media backup media attached!";
fi
0

