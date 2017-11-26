#! /bin/bash

export JAVA_HOME=/usr/lib/jvm/java-8-oracle

export JAVA_OPTS="${JAVA_OPTS:--Xms10G -Xmx11G}"

#cd /home/userx/distribution-karaf-0.6.2-Carbon/bin/

cd /home/userx/distribution-karaf-0.4.4-Beryllium-SR4/bin

./karaf clean