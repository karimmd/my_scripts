```sh


 FTP Server:
 ============
 FTP - File Transfer Protocol
 Port: 20 (Data),21 (Control)
 Protocol: TCP
 Packages: vsftpd
 Daemon: vsftpd
 Configuration file: /etc/vsftpd/vsftpd.conf
 Directory location: /var/ftp/pub/*

 Step 01:  (RPM check)
 ---------
[root@serverX ~]# rpm -qa | grep vsftpd
[root@serverX ~]# yum install vsftp* -y
[root@serverX ~]# rpm -qa | grep vsftpd

[root@serverX Desktop]# cd /var/ftp
[root@serverX ftp]# mkdir download movie software
[root@serverX ftp]# touch file1 file2

[root@serverX ftp]# systemctl restart vsftpd.service 
[root@serverX ftp]# systemctl enable vsftpd.service 
[root@serverX ftp]# systemctl stop firewalld.service 
[root@serverX ftp]# setenforce 0           ; selinux disabled

Now Open your browser: (Client-desktopX)
---------------------
Type: ftp://172.25.11.200+x
 
[root@desktopX ~]# yum install firefox -y

      FTP Server Types:
========================
	1) Normal FTP
	2) Authentication based
 
     FTP user:
--------------
	1) Anononymous user: guest user (no password)
	2) Authentication FTP user: FTP group user
	3) local user (local user of server crated by root)

  FTP Access:
-------------
	1) Web Based: ftp://ftp.example.com or ftp://192.168.11.X
	2) Command Based: # ftp 172.25.11.200+x
	3) Software Based: Filezilla, FTPPRO
	         username: xxxxs
		 passwword: ****
		  port:      21 

 Command Mode: Anonymous Login (Client)
 -------------------------------------
[root@desktopX ~]# yum install ftp -y
[root@desktopX ~]# ftp 172.25.11.200+x           ; X is server IP 
Connected to 172.25.11.200+x (172.25.11.200+x).
220 (vsFTPd 2.2.2)
Name (172.25.11.200+x:root): anonymous
                  password: ***** (any)

ftp> help
ftp> dir
ftp> cd pub
ftp> ls
ftp> bye

User Authentic Based FTP Server:
--------------------------------------
[root@serverX ~]# cd /
[root@serverX /]# mkdir ftpdir
[root@serverX /]# touch ftpdir/file{1..10}
[root@serverX /]# groupadd ftpusers
[root@serverX /]# chgrp ftpusers ftpdir -R
[root@serverX /]# chmod 750 -R ftpdir         ; see below permisison 

[root@serverX /]# useradd -G ftpusers -d /ftpdir shakil
[root@serverX /]# useradd -G ftpusers -d /ftpdir shahin
[root@serverX /]# useradd -G ftpusers -d /ftpdir shamim

[root@serverX /]# cat /etc/group
 ftpusers:1003:shakil1,shahin,shamim

[root@serverX /]# passwd shahin
[root@serverX /]# passwd shamim
[root@serverX /]# passwd shakil

[root@serverX /]# vi /etc/vsftpd/vsftpd.conf
:set nu

  12 anonymous_enable=NO                  ; NO => YES

[root@serverX /# systemctl restart vsftpd.service

Return to Desktop:
-----------------
Try with Web Browser: ftp://172.25.11.200+x

 Chroot Jail:
--------------
 [root@serverX /]# vim /etc/vsftpd/vsftpd.conf

  101 #chroot_list_enable=YES    ; before
  101  chroot_list_enable=YES     ; after

  103 #chroot_list_file=/etc/vsftpd/chroot_list ; before
  103  chroot_list_file=/etc/vsftpd/chroot_list  ; after

 [root@serverX /]# vim /etc/vsftpd/chroot_list       ;new file 
  shakil
  shamim
  shahin

 [root@serverX /]# systemctl restart vsftpd.service

Return to Desktop:
-----------------
Try with Web Browser: ftp://172.25.11.200+x

  User Protect: 
=================
[root@serverX /]# vim /etc/vsftpd/ftpusers
 shahin           ; add below of file

[root@serverX Dektop]# systemctl restart vsftpd.service



