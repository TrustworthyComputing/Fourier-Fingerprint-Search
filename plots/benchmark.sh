#!/bin/bash

for d in ~/FabWave/CAD_1_15/*/ ; do
    echo "$d"
    filename=$(basename -- "$d")

    echo "Learn $filename slices 2 fanout 10"
    (time python3 main.py --stl "$d" --mode learn --slices 2 --fanout 10 --destroyDB) &> learn_"$filename"_s2_f10.txt
    echo "Search $filename slices 2 fanout 10"
    (time python3 main.py --stl "$d" --mode search --slices 2 --fanout 10 --print_naive --neighborhoods) &> search_"$filename"_s2_f10.txt

    echo "Learn $filename slices 4 fanout 10"
    (time python3 main.py --stl "$d" --mode learn --slices 4 --fanout 10 --destroyDB) &> learn_"$filename"_s4_f10.txt
    echo "Search $filename slices 4 fanout 10"
    (time python3 main.py --stl "$d" --mode search --slices 4 --fanout 10 --print_naive --neighborhoods) &> search_"$filename"_s4_f10.txt
done

