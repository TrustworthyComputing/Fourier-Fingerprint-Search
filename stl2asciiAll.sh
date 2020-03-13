#!/bin/bash

for fullfile in ./* ; do
    filename=$(basename -- "$fullfile")
    extension="${filename##*.}"
    filename="${filename%.*}"
    echo $filename
    stl2ascii $fullfile $filename"-ascii.stl"
done
