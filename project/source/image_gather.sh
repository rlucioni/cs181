#!/bin/sh

for x in {1..4}
do
    echo 100 > value1.txt
    echo 100 > value2.txt
    echo '=====================' >> images1.txt
    echo '=====================' >> images2.txt
    python run_game.py
done