```sh
NFS (Network File System):
=========================
NFS, stands for Network File System, is a server-client protocol used for
sharing files between linux/unix to unix/linux systems. NFS enables you to 
mount a remote share locally. You can then directly access any of the files
on that remote share.

Reference Table:
----------------
Package: nfs-utils, nfs-utils-lib
Daemon: nfs-server, rpcbind, 

NFS Server: 172.25.11.200+X (Virtual Machine)
NFS Client: 172.25.11.100+X (Desktop Machine)

[root@hostX ~]# ssh root@172.25.11.200+X
: centos

Step 01: Query and Package Install  
----------------------------------
[root@serverX ~]# rpm -qa | grep nfs-utils
[root@serverX ~]# yum install nfs-utils nfs-utils-lib -y

Step 02: Service Restart and enable
-----------------------------------
[root@serverX ~]# systemctl enable rpcbind.service
[root@serverX ~]# systemctl enable nfs-server.service

(Optional) systemctl enable nfs-idmap.service

[root@serverX ~]# systemctl start rpcbind.service
[root@serverX ~]# systemctl start nfs-server.service

(Optional)systemctl start nfs-idmap.service

SELinux Disable:
----------------
[root@serverX ~]# setenforce 0

Allow NFS Service in Firewall:
------------------------------
[root@serverX ~]# systemctl restart firewalld.service
[root@serverX ~]# systemctl enable firewalld.service
[root@serverX ~]# firewall-cmd --permanent --add-service=nfs
[root@serverX ~]# firewall-cmd --reload

Step 03: Create a shared directory
-----------------------------------
[root@serverX ~]# mkdir /nfsshare -p
[root@serverX ~]# cd /nfsshare
[root@serverX nfsshare]# ls
[root@serverX nfsshare]# mkdir download documents software project office 
[root@serverX nfsshare]# ls
documents  download  office  project  software
[root@serverX nfsshare]# cd documents/
[root@serverX documents]# ls
[root@serverX documents]# touch doc{1..10}
[root@serverX documents]# cd ..
[root@serverX nfsshare]# cd download/
[root@serverX download]# touch file1 file2 file3
[root@serverX download]# cd ..
[root@serverX nfsshare]# cd office
[root@serverX office]# touch job cv profile
[root@serverX office]# cd ..
[root@serverX nfsshare]# cd project/
[root@serverX project]# touch project{1..5}
[root@serverX project]# cd ..
[root@serverX nfsshare]# cd software/
[root@serverX software]# touch office.exe vlc.exe skype.exe
[root@serverX software]# cd ..
[root@serverX nfsshare]# 

Step 04: Export shared directory on NFS Server:
----------------------------------------------
[root@serverX ~]# vim /etc/exports

/nfsshare/software      172.25.11.0/24(rw,sync,no_root_squash)
/nfsshare/project       172.25.11.0/24(ro,sync,no_root_squash)
/nfsshare/download      *(ro,sync,no_root_squash)
/nfsshare/documents     172.25.11.100+X(rw,sync,no_root_squash)
/nfsshare/office        *.example.com(rw,sync,no_root_squash)

Note:
====
=> /var/nfshare � shared directory
=> 172.25.11.0/24 � IP address range of clients
=> rw � Writable permission to shared folder
=> sync � Synchronize shared directory
=> no_root_squash � Enable root privilege
=> no_all_squash - Enable user�s authority

Step 05: Restart the NFS service and verify:
--------------------------------------------
[root@serverX ~]# systemctl restart nfs-server
[root@serverX ~]# exportfs -ra
[root@serverX ~]# showmount -e localhost

Client Side Confiugration:
=========================

Step 06: Install NFS packages in your client system
---------------------------------------------------
[root@desktopX ~]# yum install nfs-utils nfs-utils-lib

Step 07: Service Restart and enable
-----------------------------------
[root@desktopX ~]# systemctl enable rpcbind.service
[root@desktopX ~]# systemctl enable nfs-server.service

(Optional)
 systemctl enable nfs-idmap.service

[root@desktopX ~]# systemctl start rpcbind.service
[root@desktopX ~]# systemctl start nfs-server.service

(Optional) systemctl start nfs-idmap.service

Step 08: View NFS Share on NFS Server 
-------------------------------------
[root@desktopX ~]# showmount -e 172.25.11.200+X     ; X is your NFS Server IP

Export list for 172.25.11.X:
/nfsshare/download  *
/nfsshare/office    *.example.com
/nfsshare/project   172.25.11.0/24
/nfsshare/software  172.25.11.0/24
/nfsshare/documents 172.25.11.100+X        ; X = Specific an IP address

Step 09: Mount NFS shares On clients
------------------------------------
[root@desktopX ~]# mkdir /nfsdataY       ; Y is your batch no
[root@desktopX ~]# mount -t nfs 172.25.11.200+X:/nfsshare/project /nfsdataY
[root@desktopX ~]# cd /nfsdataY
[root@desktopX nfsdataY]# ls
[root@desktopX nfsdataY]# df -HT
[root@desktopX nfsdataY]# touch newproject
[root@desktopX nfsdataY]# cd
[root@desktopX ~]# umount /nfsdataY

[root@desktopX ~]# mount -t nfs 172.25.11.200+X:/nfsshare/software /nfsdataY
[root@desktopX ~]# cd /nfsdataY
[root@desktopX nfsdataY]# ls
[root@desktopX nfsdataY]# df -HT
[root@desktopX nfsdataY]# touch newsoft
[root@desktopX nfsdataY]# cd
[root@desktopX ~]# umount /nfsdata

Step 10: Mount NFS shares On clients
------------------------------------
[root@desktopX ~]# vim /etc/fstab 

172.25.11.200+X:/nfsshare/project /nfsdata  nfs defaults 0 0

[root@desktopX ~]# mount -a
[root@desktopX ~]# mount
```
