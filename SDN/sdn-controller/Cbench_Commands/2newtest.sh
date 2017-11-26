#!/bin/bash

{

###################################### Throughput ##################################


cbench -c 192.168.84.147 -p 6633 -s 2 -l 20  -m 10000 -M 100 -w 2 -C 2 -D 2 -i 2 -I 2 -t

read -p 'Pausing for 30 seconds' -t 30

cbench -c 192.168.84.147 -p 6633 -s 4 -l 20  -m 10000 -M 100 -w 2 -C 2 -D 2 -i 2 -I 2 -t

read -p 'Pausing for 30 seconds' -t 30

cbench -c 192.168.84.147 -p 6633 -s 8 -l 20  -m 10000 -M 100 -w 2 -C 2 -D 2 -i 2 -I 2 -t

read -p 'Pausing for 30 seconds' -t 30

cbench -c 192.168.84.147 -p 6633 -s 16 -l 20  -m 10000 -M 100 -w 2 -C 2 -D 2 -i 2 -I 2 -t


} | tee  /home/userx/MEGA/MEGA/scripts/sdn-controller/results/3/results_throughput.dat  


read -p "Press key to continue.. " -n1 -s