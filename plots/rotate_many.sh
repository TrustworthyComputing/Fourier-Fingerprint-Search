#!/bin/bash

for file in ./stl_files/Pipe_Joints/* ; do
    echo "Rotating $file"
    filename=$(basename -- "$file")
    openscad -o ./rotated/"$filename" -D 'model="'$file'"; degrees=[0,0,90]' ./rotate.scad
    echo
done

