#!/bin/sh

echo "RUNNING K-MEANS ON 1000 EXAMPLES..."
for i in {1..10}
do 
    python clust.py $i 1000
done
