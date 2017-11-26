```

  SAMBA Server  (File Server)
  ---------------------------------
   => Windows to non-windows (Linux/UNIX/MAC) File share
   => Use CIFS file system
   
    Package Name: samba, samba-client, cifs-utils
    Daemon: smb, nmb
    port: 445, 137, 139, 138
    Protocol: TCP & UDP
    Configuration File: /etc/samba/smb.conf
    
  Setp 01: (RPM installation)
 ----------
 [root@serverX ~]# hostname
 [root@serverX ~]# echo samba.example.com > /etc/hostname
 [root@serverX ~]# logout

 [root@samba ~]# ifconfig 
 [root@samba ~]# ip addr add 172.25.11.200+X/24 dev eth0
 [root@samba ~]# ip addr
 
 or 

[root@samba ~]# ifdown eth0
[root@samba ~]# ifup eth0

 [root@samba ~]# rpm -qa | grep samba 

 [root@samba ~]# yum install samba samba-client cifs-utils -y

 [root@samba ~]# rpm -qa | grep samba

samba-common-4.1.1-31.el7.x86_64
samba-4.1.1-31.el7.x86_64          ======> Main RPM
samba-client-4.1.1-31.el7.x86_64   ======> smbpasswd
samba-libs-4.1.1-31.el7.x86_64

[root@samba ~]# rpm -qa | grep cifs-utils
 cifs-utils------                   =======> client mount 

Step 02: Preparing Samba Users and Directory
--------------------------------------------
[root@samba ~]# groupadd samba-users
[root@samba ~]# mkdir -p /sambashare
[root@samba ~]# echo welcome to samba > /sambashare/welcome
[root@samba ~]# chgrp samba-users /sambashare
[root@samba ~]# chmod 775 /sambashare
[root@samba ~]# chmod 2775 /sambashare
[root@samba ~]# ls -ld /sambashare

[root@samba ~]# useradd -s /sbin/nologin -G samba-users toufiq    
[root@samba ~]# useradd -s /sbin/nologin -G samba-users lima
[root@samba ~]# useradd -s /sbin/nologin rakib
[root@samba ~]# smbpasswd -a toufiq
[root@samba ~]# smbpasswd -a lima
[root@samba ~]# smbpasswd -a rakib

 Step 03: server configure
 ---------------------------
[root@samba ~]# vim /etc/samba/smb.conf
 :set nu
      89     workgroup = EXAMPLE-X              ; MYHOME to EXAMPLE (BLOCK Letter)
      90     server string = Samba Server       ; Server Name
      92     netbios name = Fileserver          ; remove comment ";"
      95     hosts allow = 127. 172.25.11.      ; netowrk ID with '.'
     123     security = user 

  Note:
  -----
   security = server or share  ; no password required
   security = user   	       ; password required
 
  # write down as following share

    322 [project]                                                ; share display name
    323          comment = RW for samba-users  and RO for rakib  ; share comment
    324          path = /sambashare	                         ; share path
    325		 browseable = yes
    326          writable = yes                                  ; user write access
    327          write list = @samba-users                       ; user print access
    328          read only = yes                                 ; access for everyone
    329          read list = rakib
		 hosts allow = 


   :x (save and quit) 

[root@serverX /]# testparm              ;verify 

Step 04: SELinux Disabled and Firewall Configure
------------------------------------------------
[root@serverX /]# setenforce 0    ;disable SELinux

[root@serverX /]# systemctl restart smb.service
[root@serverX /]# systemctl enable smb.service 

[root@serverX /]# systemctl restart nmb.service 
[root@serverX /]# systemctl enable nmb.service 

[root@serverX /]# systemctl enable firewalld.service
[root@serverX /]# systemctl start firewalld.service

[root@serverX /]# firewall-cmd --permanent --add-service=samba
[root@serverX /]# firewall-cmd --reload

Step 05: Browsing (Client Part)
------------------------------
	Browse from Windows PC:
	-----------------------
	=> Start menu => run => \\172.25.11.200+X

	Linux Desktop (Client) to Linux ServerX Access:
	----------------------------------------------
	[root@desktopX ~]# smbclient -L //172.25.11.200+X -U toufiq
         : 123

 	* [-N|--no-pass]
 	* [-L|--list HOST]
        * [-U] -- user

	 Mount:
	-------
[root@desktopX ~]#  mount -t cifs //172.25.11.200+X/project  /media -o username=toufiq
 Paasswd: toufiq's passwd

[root@serverX ~]# df -HT 

[root@serverX ~]# cd /media
[root@serverX media]# ls
[root@serverX media]# cd
[root@serverX ~]# umount /media
[root@serverX ~]# df -HT 

Permanent Mount:
----------------
[root@serverX ~]# vim /etc/fstab
 //172.25.11.X/project	  /media  cifs	defaults,username=toufiq,pass=123  0 0

Mount Windows Share from Linux:
-------------------------------
=> Create a folder name 'dataX' in windows desktop
=> create some files in 'dataX' folder
=> share the directory
=> move to desktopX linux system

[root@desktopX ~]# smbclient -L //172.25.11.XP(IP) -N 
[root@desktopX ~]# mount -t cifs //172.25.11.XP(IP)/dataX  /mnt
[root@desktopX ~]# df -HT 
[root@desktopX ~]# cd /mnt
[root@desktopX mnt]# ls


[backup]                         -> Share name which will be displayed.
comment = Access files stores 	 -> Comment displayed in Network.
path = /samba/backup             -> Path of directory associated with the share.
host allow = IP address          -> Specify which domain can access this share ( Also you can make entry of it in global section).
host deny= IP address            -> Specify which domain can't access this share.
valid users = username           -> Name of users who can access the share.
public = No/Yes                  -> Specify whether guest user can access this share or not.
writable = No/yes                -> Specify whether the shared directory is writable or not.
browseable = No/Yes              -> specify whether the shared directory should be visible or not.
