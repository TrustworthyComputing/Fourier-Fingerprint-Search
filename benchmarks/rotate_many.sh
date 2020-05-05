#!/bin/bash

for dir in ~/Downloads/FabWave/CAD_1_15/* ; do
    # echo "$dir"

    classname=$(basename -- "$dir")

    echo "$classname"
    for file in $dir/* ; do
        echo "Rotating $file"
        filename=$(basename -- "$file")

        deg_x=$(shuf -i 0-5 -n 1)
        deg_y=$(shuf -i 0-5 -n 1)
        deg_z=$(shuf -i 0-5 -n 1)

        openscad -o ~/rotated-FabWave/"$classname"/"$filename" -D 'model="'$file'"; degrees=['$deg_x','$deg_y','$deg_z']' ./rotate.scad
        echo
    done

done

