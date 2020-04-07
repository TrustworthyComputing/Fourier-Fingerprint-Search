#!/bin/bash

d=$1
echo "$d"
filename=$(basename -- "$d")
filename_no_ext="${filename%.*}"

echo "Average of "$filename_no_ext" with neighborhoods"
count=0;
sum=0;
res=$(awk 'NR % 16 == 11' "$d" | cut -f4)
for i in $res
    do
    sum=$(echo $sum+$i | bc )
    ((count++))
done
echo "scale=3; $sum / $count" | bc
echo

echo "Average of "$filename_no_ext" naive"
count=0;
sum=0;
res=$(awk 'NR % 16 == 3' "$d" | cut -f4)
for i in $res
    do
    sum=$(echo $sum+$i | bc )
    ((count++))
done
echo "scale=3; $sum / $count" | bc

echo

