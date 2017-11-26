#!/bin/bash

{
cbench -c 127.0.0.1 -p 6653 -s 16 -l 10  -m 10000 -M 100 -w 2 -C 2 -D 2 -i 2 -I 2  

cbench -c 127.0.0.1 -p 6653 -s 16 -l 10  -m 10000 -M 100 -w 2 -C 2 -D 2 -i 2 -I 2 -t  

cd /home/userx/oflops/cbench/

./cbench -c 127.0.0.1 -p 6653 -s 16 -l 10  -m 10000 -M 100 -w 2 -C 2 -D 2 -i 2 -I 2  

./cbench -c 127.0.0.1 -p 6653 -s 16 -l 10  -m 10000 -M 100 -w 2 -C 2 -D 2 -i 2 -I 2 -t

} | tee  /home/userx/MEGA/MEGA/scripts/sdn-controller/results.txt 

read -p "Press key to continue.. " -n1 -s
