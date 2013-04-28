#!/bin/sh

# WARNING: comment this out to avoid deleting images
#rm images1.txt images2.txt

for x in {1..20}
do
    echo 100 > value1.txt
    echo 100 > value2.txt
    python run_game.py
    echo '=' >> images1.txt
    echo '=' >> images2.txt
done
