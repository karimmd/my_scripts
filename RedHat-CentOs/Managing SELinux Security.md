```sh

What is SELinux Security?
-------------------------
 SElinux:
 --------
  => Security Enhanced Linux
  => Devloped by NSA on RedHat Enterprise Linux

Linux Security:
 => Firewall - iptables (layer3 and Layer4) - IP,TCP,ICMP,UDP,
 => SELinux - Directory based (samba, ftp, http, nfs)

MAC (Mandatory Access Control) - User and Group Permission, ACL, PAM
DAC (Discretionary Access Control) - SELinux 

SELinux Modes:
--------------
=> Enforcing Mode (1)
=> Permissive Mode (0)
=> Disable Mode

SELinux Information:
--------------------
[root@serverX ~]# getenforce
Enforcing

Current SELinux Status: 
-----------------------
[root@serverX ~]# sestatus 

SELinux status:                 enabled
SELinuxfs mount:                /sys/fs/selinux
SELinux root directory:         /etc/selinux
Loaded policy name:             targeted
Current mode:                   permissive
Mode from config file:          enforcing
Policy MLS status:              enabled
Policy deny_unknown status:     allowed
Max kernel policy version:      28

SELinux Temporary Disable/enable:
--------------------------------
[root@serverX ~]# 

[root@serverX ~]# setenforce 
[root@serverX ~]# setenforce 0 | 1
[root@serverX ~]# setenforce permissive | enforcing 
[root@serverX ~]# getenforce

SELinux Permanent Change:
------------------------
[root@serverX ~]# grep '^SELINUX' /etc/selinux/config 

[root@serverX ~]# vim /etc/sysconfig/selinux
SELINUX=disabled

[root@serverX ~]# reboot

[root@serverX ~]# getenforce 

View SELinux Context:
--------------------
[root@serverX ~]#  cd /
[root@serverX ~]# ls -Z

user:role:type[:range]

SELinux Contexts:
-----------------
=> user
=> role
=> type
=> sensitivity (range)

SELinux Contexts:
-----------------
 user: 		=> system_u
 role: 		=> object_r
 type:		=> admin_home_t
 sensitivity	=> s0

User:
-----
The SELinux user identity. This can be associated to one or more roles that the SELinux user is allowed to use.

Role:
------
The SELinux role. This can be associated to one or more types the SELinux user is allowed to access.

[root@serverX ~]# yum install httpd -y

[root@serverX ~]# ls -lZ /var/www/
drwxr-xr-x. root root system_u:object_r:httpd_sys_content_t:s0 html

[root@serverX ~]# ls -lZ /etc/passwd
-rw-r--r--. root root system_u:object_r:passwd_file_t:s0 /etc/passwd

[root@serverX ~]# ls -dZ /tmp/
drwxrwxrwt. root root system_u:object_r:tmp_t:s0       /tmp/

[root@serverX ~]# ls -lZ /home
drwx------. student 1000 unconfined_u:object_r:user_home_dir_t:s0 student
drwx------.    5001 5001 unconfined_u:object_r:user_home_dir_t:s0 tarek

[root@serverX ~]# ls -Z 
-rw-------. root root system_u:object_r:admin_home_t:s0 anaconda-ks.cfg

SELinux Testing: Example: 01
----------------------------
[root@serverX ~]# cd
[root@serverX ~]# ls -Zd ~
dr-xr-x---. root root system_u:object_r:admin_home_t:s0 /root

[root@serverX ~]# cal
[root@serverX ~]# cal > calender
[root@serverX ~]# cat calender
[root@serverX ~]# ls -Z calender
-rw-r--r--. root root unconfined_u:object_r:admin_home_t:s0 calender

[root@serverX ~]# cp calender /var/www/html/calender2
[root@serverX ~]# mv calender /var/www/html/
[root@serverX ~]# ls -Zd /var/www/html/
drwxr-xr-x. root root system_u:object_r:httpd_sys_content_t:s0 /var/www/html/

[root@serverX ~]# ls -Z /var/www/html/*
-rw-r--r--. root root unconfined_u:object_r:admin_home_t:s0 calender
-rw-r--r--. root root unconfined_u:object_r:httpd_sys_content_t:s0 calender2

[root@serverX ~]# echo "HEllo World" >> /var/www/html/index.html 

[root@serverX ~]# ls -Z /var/www/html/*
-rw-r--r--. root root unconfined_u:object_r:admin_home_t:s0 calender
-rw-r--r--. root root unconfined_u:object_r:httpd_sys_content_t:s0 calender2
-rw-r--r--. root root unconfined_u:object_r:httpd_sys_content_t:s0 index.html 

Change SELinux Security Context:
-------------------------------
[root@serverX ~]# yum install setools* -y
[root@serverX ~]# yum install policycoreutils-python -y

[root@serverX ~]# ls -lZ /var/www/html/* 
-rw-r--r--. root root unconfined_u:object_r:admin_home_t:s0 calender
-rw-r--r--. root root unconfined_u:object_r:httpd_sys_content_t:s0 calender2
-rw-r--r--. root root unconfined_u:object_r:httpd_sys_content_t:s0 index.html 

[root@serverX ~]# restorecon /var/www/html/calender
[root@serverX ~]# ls -Z /var/www/html/calender
-rw-r--r--. root root unconfined_u:object_r:httpd_sys_content_t:s0 calender

Note: semanage fcontext -a -t httpd_sys_content_t '/var/www/html(/.*)?'

SELinux Testing: Example: 02
============================
[root@serverX ~]# mkdir /websites
[root@serverX ~]# ls -Zd /websites
drwxr-xr-x. root root unconfined_u:object_r:default_t:s0 /websites

[root@serverX ~]# restorecon /websites
[root@serverX ~]# ls -Zd /websites
drwxr-xr-x. root root unconfined_u:object_r:default_t:s0 /websites

[root@serverX ~]# touch /websites/index.html
[root@serverX ~]# echo "HEllo SELinux World" >> /websites/index.html 

[root@serverX ~]# ls -Z /websites
-rw-r--r--. root root unconfined_u:object_r:default_t:s0 index.html

[root@serverX ~]# vim /etc/httpd/conf/httpd.conf 

119 #DocumentRoot "/var/www/html"
120  DocumentRoot "/websites"
131 <Directory "/websites">

[root@serverX ~]# systemctl restart firewalld
[root@serverX ~]# firewall-cmd --permanent --add-port=80/tcp
[root@serverX ~]# firewall-cmd --reload 

=> Switch to DesktopX
=> Open Firefox Browser 
=> http://172.25.11.200+X

[root@serverX ~]# chcon -t httpd_sys_content_t /websites/index.html 
[root@serverX ~]# ls -lZ /websites/index.html 

[root@serverX ~]# systemctl restart httpd

=> Switch to DesktopX
=> Open Firefox Browser 
=> http://172.25.11.200+X

======================================================
