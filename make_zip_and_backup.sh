#!/bin/bash

pull_locations[0]="/home/kyle/scripts/";
push_locations[0]="scripts";
pull_locations[1]="/home/kyle/.thunderbird/";
push_locations[1]="thunderbird";
pull_locations[2]="/home/kyle/code/";
push_locations[2]="code";
pull_locations[3]="/home/kyle/Music/";
push_locations[3]="Music";
pull_locations[4]="/home/kyle/Documents/";
push_locations[4]="Documents";
pull_locations[5]="/home/kyle/.ssh/";
push_locations[5]="ssh";
pull_locations[6]="/home/kyle/.gnupg/";
push_locations[6]="gnupg";

echo -e "\033[0;31mCreating password protected zip of the above locations...\033[0m"

base_path="/media/kyle/Pepper (1TB)/Backups/"
today=`date +%Y-%m-%d_%H-%M-%S`
archive_name="$today""backup.7z";

for i in `seq 0 6`;
do
    pull=${pull_locations[$i]}
    file_list="$file_list $pull"
done
echo "Creating '$archive_name' from: '$file_list'"
7z a -p "$archive_name" $file_list

echo "Created archive '$archive_name'"

"$base_path"  2> /dev/null
media_attached=$?
# 126 returned if directory exists, 127 if it does not.
if [ "$media_attached" -eq "126" ]; then
    echo "Backup media found!"
    cp "$archive_name" "$base_path"
else
    echo "No media backup media attached!";
fi
