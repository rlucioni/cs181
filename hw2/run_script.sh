#!/bin/sh

echo "CLEANING..."
rm log.txt
echo "RUNNING SIMPLE NETWORK..."
python neural_net_main.py -e 100 -r 1.0 -t simple >> log.txt
python neural_net_main.py -e 100 -r 0.1 -t simple >> log.txt
python neural_net_main.py -e 100 -r 0.01 -t simple >> log.txt
python neural_net_main.py -e 100 -r 0.001 -t simple >> log.txt
python neural_net_main.py -e 100 -r 1.0 -t hidden >> log.txt
python neural_net_main.py -e 100 -r 0.1 -t hidden >> log.txt
python neural_net_main.py -e 100 -r 0.01 -t hidden >> log.txt
python neural_net_main.py -e 100 -r 0.001 -t hidden >> log.txt
