#!/bin/sh

# WARNING: comment this out to avoid deleting images
#rm images1.txt images2.txt

for x in {1..20}
do
    echo 50 > value1.txt
    echo 50 > value2.txt
    python run_game.py -d 0
    echo '=' >> images1.txt
    echo '=' >> images2.txt
done
