#!/bin/bash

docker stop $(docker ps -a -q)

docker rm $(docker ps -a -q)

docker inspect --format '{{ .NetworkSettings.IPAddress }}' $(docker ps -a -q)
