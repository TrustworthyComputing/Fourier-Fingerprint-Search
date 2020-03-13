#!/bin/bash

for fullfile in $1/* ; do
    filename=$(basename -- "$fullfile")
    extension="${filename##*.}"
    filename_no_ext="${filename%.*}"
    basedirectory="${fullfile%$filename}"

    echo $filename
    # echo $filename_no_ext
    # echo $basedirectory
    # echo $basedirectory$filename_no_ext"-ascii.stl"
    stl2ascii $fullfile $basedirectory$filename_no_ext"-ascii.stl"
done
