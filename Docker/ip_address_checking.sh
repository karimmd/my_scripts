#!/bin/bash

docker inspect --format '{{ .NetworkSettings.IPAddress }}' $(docker ps -a -q)

read -p "Press key to continue.. " -n1 -s
