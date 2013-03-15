#!/bin/sh

echo "RUNNING clust.py ON 1000 EXAMPLES..."
for i in {1..10}
do 
    echo $i
    python clust.py $i 1000
done
