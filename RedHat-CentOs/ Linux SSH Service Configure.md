```sh


 SSH - Secure Shell
-------------------
 Application - Remotely server/router/firewalld administration using CLI mode
 Port no: 22 (default)
 Package: openssh-server (server), openssh-client(client)
 Daemon: sshd
 configuration file: /etc/ssh/sshd_config 

Step by step configuration:
==========================

Step 01: RPM Query, install
---------------------------------
[root@serverX ~]# rpm -qa | grep openssh-server
openssh-server-6.4p1-8.el7.x86_64

[root@serverX ~]# yum install openssh* -y  [if not found]

[root@serverX ~]# systemctl restart sshd.service
[root@serverX ~]# systemctl enable sshd.service
[root@serverX ~]# systemctl status sshd.service

[root@serverX ~]# ifconfig

(Optional)
----------
Temporary IP Configure:  ifconfig eth0 172.25.11.200+X netmask 255.255.255.0

SSH Client:
-----------
 => Linux Client (defautl installed)
 => Windows Client (putty, ssh client)
    > putty > ssh > ip > port (22)

Testing:
=======

Move to DesktopX
----------------

 > ping 172.25.11.200+X   (ssh server)

SSH Login with Root User
---------------------------------
[root@desktopX ~]# ssh root@172.25.11.200+X

Are you sure you want to continue connecting (yes/no)? yes
root@172.25.11.200+X's password: ****** (remote PC) 

[root@serverX ~]# who
[root@serverX ~]# useradd user1
[root@serverX ~]# passwd user1
 : 123
 : 123

[root@serverX ~]# exit 

Linux with user1:
-------------------------
[root@desktopX ~]# ssh  user1@172.25.11.200+X

[user1@serverX~]$ su -
 : ********

[root@serverX ~]# who
[root@serverX ~]# exit
[root@desktopX ~]# 

Secure Copy (scp) from server:
-------------------------------
[root@desktopX ~]# scp root@172.25.11.200+X:/etc/passwd /root/Desktop

Secure Copy (scp) to serverX:
-------------------------------
[root@desktopX ~]# scp /etc/passwd root@172.25.11.200+X:/root

Password Less ssh login:
------------------------
[root@desktopX ~]# cd
[root@desktopX ~]# ls 
[root@desktopX ~]# ls -la
[root@desktopX ~]# cd .ssh
[root@desktopX .ssh]# ls 
 known_host (list of known hosts)  id_rsa.pub   id_rsa

[root@desktopX .ssh]# rm -rf * 

[root@desktopX .ssh]# ls
[root@desktopX .ssh]# ssh user1@172.25.11.200+X

Are you sure you want to continue connecting (yes/no)? yes

 Ctlrl+C
 
[root@desktopX .ssh]# ls
 known_host (created)

[root@desktopX .ssh]# ssh-keygen  ; (Enter 3 Times)
id_rsa.pub id_rsa

[root@desktopX .ssh]# cat id_rsa
[root@desktopX .ssh]# cat id_rsa.pub

[root@desktopX .ssh]# ssh-copy-id user1@172.25.11.200+X  (serverX)
[root@desktopX .ssh]# ssh user1@172.25.11.200+X

[root@serverX ~]# cd .ssh 
[root@serverX .ssh]# ls
 authorized_keys
[root@serverX .ssh]# cat authorized_keys   ; same as public key of desktopX

=====>  Move to serverX (Virtual)

Change Default Port:
-------------------
[root@serverX ~]# vim /etc/ssh/sshd_config 
:set nu

 17 #Port 22         ; old
 17  Port 2015       ; remove '#'

[root@serverX ~]# systemctl restart sshd.service
[root@serverX ~]# setenforce 0
[root@serverX ~]# systemctl stop firewalld
[root@serverX ~]# systemctl disable firewalld

Verify curren SSH port:
-----------------------
[root@serverX ~]# netstat -ntlp | grep ssh

=====>  Move to desktopX (Physical)

SSH Server Login with Specif Port:
---------------------------------
[root@desktopX ~]# ssh user1@172.25.11.200+X   (default port)  - Refused

[root@desktopX ~]# ssh -p  2015  user1@172.25.11.200+X	; if user1 user

[user1@serverX ~]$ exit

Disabled Root Login:
--------------------
[root@serverX ~]# vim /etc/ssh/sshd_config 
:set nu

 48 #PermitRootLogin yes        ;old
 48  PermitRootLogin no         ;new

[root@serverX ~]# systemctl restart sshd.service

Test:
----
[root@desktopX ~]# ssh -p 2015 root@172.25.11.200+X

[root@desktopX ~]# ssh -p 2015 user1@172.25.11.200+X
