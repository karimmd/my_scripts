```sh

RPM Installation:
-----------------
 => Manually (rpm command)
 => Automatically (YUM Server)

Yum Server Configure:
---------------------
 => Requirments:
    ------------
	=> DVD (centos/redhat)
	=> 5GB Free Space in "/var"
	=> Default FTP Dir: "/var/ftp/pub"
  	=> Packages: 
		1) createrepo - server (already installed)
		2) vsftpd (for yum client)

 Step 01: Check free space "/var"
 ======= ------------------------
[root@desktopX ~]# df -HT
Filesystem    Type     Size   Used  Avail Use% Mounted on
/dev/sda6     ext4      16G   7.1G   7.7G  48% /

            Note: By default "/var location under "/" partition"

 Step 02: Mount DVD under "/mnt"
 ======= -------------------------  		
[root@desktopX ~]# mount /dev/sr0 /mnt   ; here "sr0" is dvd device
mount: block dvice /dev/sr0 is write-protected, monting read-only
[root@desktopX ~]# cd /mnt
[root@desktopX mnt]# ls
[root@desktopX mnt]# cd Packages
[root@desktopX Packages]#  ls

ISO Mount:
----------
[root@desktopX ~]# mount -t iso9660 /root/Desktop/C(Tab-.iso)  /mnt
[root@desktopX ~]# cd /mnt 
[root@desktopX mnt]# ls
[root@desktopX mnt]# cd Packages
[root@desktopX Packages]#  ls

 Step 03: Dependency Install 
 ======= -------------------
[root@desktopX Packages]# rpm -ivh vsftpd-Tab....
[root@desktopX Packages]# systemctl restart vsftpd.service
[root@desktopX Packages]# systemctl enable vsftpd.service

 Step 04: RPM copy to "/var/ftp/pub"
 ======= ---------------------------  
[root@desktopX Packages]# cd /var/ftp/pub
[root@desktopX pub]# ls
[root@desktopX pub]# rm -rf * 
[root@desktopX pub]# ls
[root@desktopX pub]# cd /mnt
[root@desktopX mnt]# cp -rv Packages /var/ftp/pub

Note: All "Packages" will be copy to "/var/ftp/pub". If old 
rpm exist, please delete first.

Step 05: yum server confiugraiton file 
======= ------------------------------
[root@desktopX mnt]# cd /etc/yum.repos.d
[root@desktopX yum.repos.d]# ls
[root@desktopX yum.repos.d]# mkdir old
[root@desktopX yum.repos.d]# ls
[root@desktopX yum.repos.d]# mv * old
[root@desktopX yum.repos.d]# ls
[root@desktopX yum.repos.d]# vim server.repo
 [server]
 name = yum server
 baseurl = file:///var/ftp/pub/Packages
 enabled = 1
 gpgcheck = 0

:x (save and exit)

[root@desktopX yum.repos.d]# createrepo -v /var/ftp/pub/Packages
[root@desktopX yum.repos.d]# yum clean all  ; Previous yum server cache clear
[root@desktopX yum.repos.d]# yum list all   ; list of available rpm current repo

[root@desktopX yum.repos.d]# yum repolist  

[root@desktopX yum.repos.d]# systemctl disable firewalld.service
[root@desktopX yum.repos.d]# systemctl stop firewalld.service
[root@desktopX yum.repos.d]# setenforce 0
[root@desktopX yum.repos.d]# systemctl restart vsftpd.service
[root@desktopX yum.repos.d]# ifconfig br0
       
YUM Server Test:
----------------
[root@desktopX yum.repos.d]# yum info ftp
[root@desktopX yum.repos.d]# yum install ftp -y  ; test command
[root@desktopX yum.repos.d]# yum install gnote -y 

====> move to virtual machine 
 
YUM client Configure:
--------------------
[root@serverX ~]# ping 172.25.11.100+X    ;(your yum desktopX br0 IP)

[root@serverX ~]# cd /etc/yum.repos.d
[root@serverX yum.repos.d]# ls
[root@serverX yum.repos.d]# rm -rf *
[root@serverX yum.repos.d]# vi client.repo
 [client]
 name = yum client
 baseurl = ftp://172.25.11.100+X/pub/Packages               ;X=Server's IP
 enabled = 1    
 gpgcheck = 0
:x
[root@serverX yum.repos.d]# yum clean all  ; cache clear
[root@serverX yum.repos.d]# yum list all   ;list of available rpm
[root@serverX yum.repos.d]# yum install php -y   ; test installation 

		================ The End =====================

========== Configure DVD as YUM Repos =========

[root@serverX ~]# cd /etc/yum.repos.d
[root@serverX yum.repos.d]# ls
[root@serverX yum.repos.d]# mkdir old
[root@serverX yum.repos.d]# ls
[root@serverX yum.repos.d]# mv * old
[root@serverX yum.repos.d]# vim dvd.repo
[dvd]
name=dvd repo
baseurl=file:///mnt
enabled=1
gpgcheck=0

DVD:
----
[root@serverX yum.repos.d]# mount /dev/sr0 /mnt

ISO:
---
[root@serverX yum.repos.d]# mount -t iso9660 /root/Desktop/CentOS7.1.iso /mnt

[root@serverX yum.repos.d]# yum list all
