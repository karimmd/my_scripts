#!/bin/bash

{
cbench -c 192.168.84.143 -p 6653 -s 16 -l 10  -m 10000 -M 100 -w 2 -C 2 -D 2 -i 2 -I 2  

cbench -c 192.168.84.143 -p 6633 -s 16 -l 10  -m 10000 -M 100 -w 2 -C 2 -D 2 -i 2 -I 2 -t  

cd /home/userx/github/cbench/

./cbench -c 192.168.84.143 -p 6653 -s 16 -l 10  -m 10000 -M 100 -w 2 -C 2 -D 2 -i 2 -I 2  

./cbench -c 192.168.84.143 -p 6653 -s 16 -l 10  -m 10000 -M 100 -w 2 -C 2 -D 2 -i 2 -I 2 -t

} | tee  /home/userx/MEGA/MEGA/scripts/sdn-controller/resultsOpenMUL.txt 

read -p "Press key to continue.. " -n1 -s
