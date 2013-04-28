#!/bin/sh

echo "RUNNING SIMPLE NETWORK..."
python neural_net_main.py -e 100 -r 0.1 -t simple >> simple-1_0.txt
wait
#python neural_net_main.py -e 100 -r 0.1 -t simple >> simple-0_1.txt
#wait
#python neural_net_main.py -e 100 -r 0.001 -t simple >> simple-0_001.txt
#wait

#echo "RUNNING HIDDEN NETWORK..."
#python neural_net_main.py -e 100 -r 1.0 -t hidden >> hidden30-1_0.txt
#wait
#python neural_net_main.py -e 100 -r 0.1 -t hidden >> hidden30-0_1.txt
#wait
#python neural_net_main.py -e 100 -r 0.01 -t hidden >> hidden30-0_01.txt
#wait
#python neural_net_main.py -e 100 -r 0.001 -t hidden >> hidden30-0_001.txt
#wait

#python neural_net_main.py -e 100 -r 1.0 -t hidden >> hidden15-1_0.txt
#wait
#python neural_net_main.py -e 100 -r 0.1 -t hidden >> hidden15-0_1.txt
#wait
#python neural_net_main.py -e 100 -r 0.01 -t hidden >> hidden15-0_01.txt
#wait
#python neural_net_main.py -e 100 -r 0.001 -t hidden >> hidden15-0_001.txt
#wait

#git add simple-1_0.txt
#git add simple-0_1.txt
#git add simple-0_001.txt

#git add hidden30-1_0.txt
#git add hidden30-0_1.txt
#git add hidden30-0_01.txt
#git add hidden30-0_001.txt

#git add hidden15-1_0.txt
#git add hidden15-0_1.txt
#git add hidden15-0_01.txt
#git add hidden15-0_001.txt
