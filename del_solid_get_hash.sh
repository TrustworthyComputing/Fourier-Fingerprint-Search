#!/bin/bash

for dir in ~/Downloads/FabWave/* ; do

    # echo "$dir"
    for file in $dir/* ; do
        # echo -e "\t$file"
        sed -i '/solid*/d' $file
        sha1sum $file
    done
done
