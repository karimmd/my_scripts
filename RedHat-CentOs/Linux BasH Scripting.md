```

 Shell:
=======
 input from keyboard via users
 out put to monitor from kernel
 
 Types of shell:
-----------------
 1. shell sh(.sh)
 2. bash shell (commonly used)
 3. zshell 
 4. cshell (c programming based)
 5. kshell

Check Current Shell:
--------------------
[root@serverX ~]# echo $SHELL

Current installed shell in system:
----------------------------------
[root@serverX ~]#  cat /etc/shells 
/bin/sh
/bin/bash
/sbin/nologin
/usr/bin/sh
/usr/bin/bash
/usr/sbin/nologin

 how to write a script:
 ======================

[root@server ~]# vim myshell.sh
 #!/bin/bash
 # this is shell comments
 # this is a test script

 a=CSL_Training
 echo $a
 echo "hello"

:x

shell permission
-----------------
[root@server ~]# ls
[root@server ~]# chmod u+x myshell.sh 
[root@server ~]# ls                     ; green color 

shell run:
----------
[root@server ~]# ./myshell.sh
or
[root@server ~]#  sh myshell.sh

varibale types:
----------------
 user defined: small character 
 system/env variable: block (USER/SHELL/HOME: (no=88)
 command:
[root@server ~]#  printenv ; list of common env variable

[root@server ~]# echo $SHELL
[root@server ~]# echo $HOSTNAME
[root@server ~]# echo $USER
[root@server ~]# echo $HOME
 
System Information using a shell script:
----------------------------------------
[root@server ~]# vim system.sh

#!/bin/bash
#this scripts devloped to get system information
 clear
 echo "hello"
sleep 2
 echo -n "Enter your name": 
 read name
 echo " you type, your name is" $name
 echo "my MAC address is:" `ifconfig eth0 | grep ether | cut -d " " -f 10`

sleep 2
echo "My IP address Is:" `ifconfig eth0 | grep inet | cut -d ' ' -f10 | head -1`

sleep 2

 echo "you login as " $USER
sleep 2
echo "Thank you"

[root@server ~]# chmod u+x system.sh
[root@server ~]# sh system.sh
 
yum client configure script:
----------------------------
[root@server ~]# vim yumclient.sh

#!/bin/bash
#this script for yum client configuraiotn
echo "welcome to yum client configuration"
echo "Enter your yum server IP address: "
read server
echo "you type your server ip address is:" $server
echo "pinging your server:" 
echo "`ping -c 2 $server`"
cd /etc/yum.repos.d/
`rm -rf * `
`touch client.repo`
`echo [client] > /etc/yum.repos.d/client.repo`
echo name=my yum client >> /etc/yum.repos.d/client.repo
echo baseurl=ftp://$server/pub/Packages >> /etc/yum.repos.d/client.repo
echo gpgcheck=0 >> /etc/yum.repos.d/client.repo
echo enabled=1 >> /etc/yum.repos.d/client.repo
echo "your yum client is ready"
sleep 1
echo "thank you"

[root@server ~]# chmod u+x yumclient.sh
[root@server ~]# sh yumclient.sh
[root@server ~]# 
