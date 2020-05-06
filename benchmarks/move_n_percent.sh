#!/bin/bash

DATASET_PATH=FabWave

mkdir file_lists

for d in $DATASET_PATH/* ; do
    classname=$(basename -- "$d")

    ls -ld $d/* | awk '{print $NF}'> file_lists/all_"$classname"_files.txt

    lines=$(wc -l file_lists/all_"$classname"_files.txt | cut -d" " -f1)
    # echo $lines

    num_files_to_move=$((lines / 10))
    # echo $num_files_to_move

    files_to_move=$(head -n "$num_files_to_move" file_lists/all_"$classname"_files.txt)
    # echo $files_to_move

    mkdir -p test/"$classname"
    mv $files_to_move test/"$classname"/
done
