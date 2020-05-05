#!/bin/bash

DATASET_PATH=benchmarks/FabWave
MODE="$1"
SLICES=2
FANOUT=10
MINSIGS=6

if [ "$MODE" = "learn" ]; then
    echo "Destroying the database"
    python3 main.py --stl $DATASET_PATH/Bearings/00ed2536-3d80-4f07-8851-4f49f1606498-ascii.stl --mode search --destroyDB
fi

for d in $DATASET_PATH/*/ ; do
    echo "$d"
    filename=$(basename -- "$d")

    if [ "$MODE" = "learn" ]; then
        echo "Learn $filename slices:$SLICES fanout:$FANOUT"
        (time python3 main.py --stl "$d" --mode learn --slices $SLICES --fanout $FANOUT ) &> results/learn_"$filename"_s"$SLICES"_f"$FANOUT".txt
    else
        echo "Search $filename slices:$SLICES fan-out:$FANOUT minimum-sigs-in-neighborhood:$MINSIGS"
        (time python3 main.py --stl "$d" --mode search --slices $SLICES --fanout $FANOUT --print_naive --neighborhoods --sigs_in_neighborhood $MINSIGS) &> results/search_"$filename"_s"$SLICES"_f"$FANOUT"_min"$MINSIGS".txt
    fi

done
