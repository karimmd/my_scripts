```sh


 =====: Linux Package Management: ===

 #######################################

 Windows: .exe, .bin, .msi, .rar., .zip, 
 Linux: .rpm(fedora/oracle/redhat/centos)

 .deb (ubuntu,mint,backtrack,Debian),
 .tar.gz, .tar.bz2, .tar (all linux)

 Common Linux Package:
 ---------------------
 .rpm (Redhat Package Manager)- Redhat, centos, fedora, oracle, SUSE
 .deb (debian,ubuntu,mint,backtrack)
 .tar.gz
 
 RPM Source:
 --------------------
 => DVD
 => Internet
 => ISO

Lab RPM Location:
-----------------
 => Open your Firefox Browser
 => ftp://172.25.11.254/pub/ (Packages)

or

=> ftp://172.25.11.254 

 => click rpm directory

 RPM Format:
 -----------
 vsftpd-3.0.2-9.el7.x86_64.rpm
    1      2    3    4      5
 1 - rpm name
 2 - rpm version
 3 - linux platform
 4 - processor arc
 5 - .extention

 Rpm Query:
------------
[root@desktop1 ~]# rpm -qa
[root@desktop1 ~]# rpm -qa | grep cups          ; [cups is rpm name]

 ex: 
[root@desktop1 ~]# rpm -qa | grep vsftpd  
[root@desktop1 ~]# rpm -qa | grep openssh 

 RPM Install/Remove:
 -------------------
 => Manually (RPM)
 => Automatically (YUM)

RPM Remove:
-----------
[root@desktop1 ~]# rpm -qa | grep vsftpd 
[root@desktop1 ~]# rpm -e vsftpd 
[root@desktop1 ~]# rpm -qa | grep vsftpd 

 COmmon Linux RPM for Linux Server:
 ----------------------------------
 1) ssh - openssh-server, openssh-client
 2) telnet - xinetd, telnet-server
 3) cron - crontab
 4) proxy - squid, sarg
 5) DHCP - dhcp
 6) FTP - vsftpd, ftp
 7) Mail - postfix, dovecot, squirrelmail
 8) NFS - nfs, nfs-utils, 
 9) Samba - samba, smbclient, cifs-utils
 10) Web - httpd, openssl, mod_ssl
 11) DNS - bind, bind-utils
 12) cacti - cacti, snmp
 13) Time - ntp
 14) Virtualization - libvirt, qemu-kvm, virt-manager

Database: mysql, mariadb, postgresql
Other: firefox, thunderbird, wireshark-gnome, libreoofice

Linux OS Kernel Info:
---------------------
[root@serverX ~]# uname -r
[root@serverX ~]# uname 
[root@serverX ~]# cat /etc/redhat-release 

DVD Mount:
 ---------------
 => insert ur DVD in DVD ROM
 => [root@desktop1 ~]# mount /dev/sr0 /media   ; show readonly
    [root@desktop1 ~]# cd /media
    [root@desktop1 media]# ls
    [root@desktop1 media]# cd Packages
    [root@desktop1 Packages]# ls

or

ftp://172.25.11.254/rpm]

Note: Download vsftpd rpm from FTP Server ;[ftp://172.25.11.254/rpm]

[root@desktop1 Packages]# cd 
[root@desktop1 ~]# cd Downloads
[root@desktop1 Downloads]# ls
vsftpd-3.0.2-9.el7.x86_64.rpm 

[root@desktop1 Downloads]# rpm -qpi vsftpd-3. (press tab) 
[root@desktopX Downloads]# rpm -qp --scripts vsftpd-3.0.2-9.el7.x86_64.rpm 

[root@desktopX Downloads]# rpm -vK vsftpd-3.0.2-9.el7.x86_64.rpm 

Install GPG Pub key (optional):
-------------------------------
[root@desktopX ~]# rpm --import RPM-GPG-KEY-CentOS-7    ; from DVD
[root@desktopX ~]# rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-7
[root@desktopX ~]# rpm -qa gpg-pubkey
gpg-pubkey-f4a80eb5-53a7ff4b

RPM check for specific file:
----------------------------
[root@desktopX ~]# ifconfig
[root@desktopX ~]# ip addr

[root@desktopX ~]# which ifconfig
/sbin/ifconfig

[root@desktop1 ~]# rpm -qf /sbin/ifconfig 
net-tools-2.0-0.17.20131004git.el7.x86_64

RPM Install:
-------------
 1) Manually (rpm)
 2) Automatically (YUM Server): Yellow Dog Updater Modifier
      (yum repository required)

 RPM :
 ----
 1) Queiry : -qa
 2) Install: -ivh
 3) Remove: -e
 4) Upgrade: -U
 
 RPM Query:
 ----------
[root@desktopX Downloads]# rpm -qa | grep vsftpd

 Manual Install:
 --------------
[root@desktopX Downloads]# ls
[root@desktopX Downloads]# rpm -ivh vsftpd-3.0.2-9.el7.x86_64.rpm      ; press tab 

 i - install
 v - verbosely
 h - hash (#####)

[root@desktopX Downloads]# rpm -qa | grep vsftpd

[root@desktopX Downloads]# rpm -ivh gnote-3.8.1-3.el7.x86_64.rpm   ; dependency failed 

[root@desktopX Downloads]# rpm -ivh --nodeps gnote-3.8.1-3.el7.x86_64.rpm ; without dependencies

[root@desktopX Downloads]# rpm -qa | grep gnote

Confiugration files for specific RPM:
------------------------------------
[root@desktopX ~]# rpm -qc vsftpd 
[root@desktopX ~]# rpm -qc openssh-server 

RPM Remove:
----------------
[root@desktopX ~]# rpm -e vsftpd
[root@desktopX ~]# rpm -e gnote

[root@desktopX ~]# rpm -qa | grep vsftpd 
[root@desktopX ~]# rpm -qa | grep gnote

Yum CLient COnfiugre:
---------------------
[root@serverX ~]# ping 172.25.11.254
[root@serverX ~]# cd /etc/yum.repos.d
[root@serverX yum.repos.d]# ls
[root@serverX yum.repos.d]# mkdir old
[root@serverX yum.repos.d]# mv * old
[root@serverX yum.repos.d]# ls         ; remove moved
[root@serverX yum.repos.d]# vim client.repo
 [client]
 name=yum client
 baseurl=ftp://172.25.11.254/pub/Packages     ; yum server IP
 enabled=1
 gpgcheck=0

 :x     (SAVE & exit) 

[root@serverX yum.repos.d]# yum clean all
[root@serverX yum.repos.d]# yum list all 
[root@serverX yum.repos.d]# yum repolist 

YUM Client Test: 
----------------
[root@serverX yum.repos.d]# yum install gnote -y
[root@serverX yum.repos.d]# yum install elinks -y
[root@serverX yum.repos.d]# rpm -qa | grep elinks


Details RPM Information :
-------------------------
[root@serverX ~]# yum info elinks 

 Package Remove:
----------------
 [root@serverX yum.repos.d]# yum remove elinks
 [root@serverX yum.repos.d]# yum remove gnote

[root@serverX yum.repos.d]# rpm -qa | grep gnote
[root@serverX yum.repos.d]# rpm -qa | grep elinks
