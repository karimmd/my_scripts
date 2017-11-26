#! /bin/bash


########### Start Docker based SDN Controller Testing VM ############


#sudo docker run -i -t sdn-controllers-ubuntu-12.04 /bin/bash

#sudo docker run -i -t odl-onos-ubuntu /bin/bash

#sudo docker run -d -p 6653 -p 8080 --name=floodlight pierrecdn/floodlight

sudo docker run --name=openmul_enet_c -p 10000:10000 -p 6653:6653 -p 8181:8181 -d --privileged ethernity/openmul_enet /bin/bash -c /openmul_start.sh
