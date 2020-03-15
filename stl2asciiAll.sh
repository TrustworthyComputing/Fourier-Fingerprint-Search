#!/bin/bash

for fullfile in $1/* ; do
    filename=$(basename -- "$fullfile")
    extension="${filename##*.}"
    filename_no_ext="${filename%.*}"
    basedirectory="${fullfile%$filename}"

    if [ "$extension" != "stl" ]; then
        echo $fullfile" is not STL, skipping..."
        continue
    else
        echo "Converting "$fullfile" to ASCII."
    fi
    stl2ascii $fullfile $basedirectory$filename_no_ext"-ascii.stl"
    rm -f $fullfile
done
