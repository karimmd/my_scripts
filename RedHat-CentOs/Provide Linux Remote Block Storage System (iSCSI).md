```sh


Reference Table:
===============

Packages: targetcli (server),  iscsi-initiator-utils (Client) 
Daemon: target (server), iscsi (client)
Port: 3260
Protocol: TCP 
Configuraiton file (client): /etc/iscsi/initiatorname.iscsi (Client)
New Commands: targetcli (server), iscsiadm(client)  

Step 01: Package Install and Service enable
-------------------------------------------
[root@serverX ~]# yum install targetcli
[root@serverX ~]# systemctl enable target.service
[root@serverX ~]# systemctl start target.service

Step 02: Port Open on System Firewall 
------------------------------------------
[root@serverX ~]# firewall-cmd --permanent --add-port=3260/tcp
[root@serverX ~]# firewall-cmd --reload

Step 03: Create a 1GB Diks Space for LVM 
----------------------------------------
[root@serverX ~]# fdisk -l
[root@serverX ~]# fdisk /dev/vda

=> Create 1GB Partition primary partition (n, p (primary), (Press Enter), +1G, p, w)

[root@serverX ~]# partprobe /dev/vda

 => Make a PV for VG
 => Create a VG (iscsi_vg1)
 => Create a LV (iscsi_lv1)

[root@serverX ~]# pvcreate /dev/vda4                   ;(yum install lvm2)
[root@serverX ~]# vgcreate iscsi_vg1 /dev/vda4
[root@serverX ~]# lvcreate -n iscsi_lv1 -L 500M iscsi_vg1

Step 04: Configure iSCSI Target
-------------------------------
[root@serverX ~]# targetcli 
/> ls
o- / ........................................... [...]
  o- backstores ................................ [...]
  | o- block ................................... [Storage Objects: 0]
  | o- fileio .................................. [Storage Objects: 0]
  | o- pscsi ................................... [Storage Objects: 0]
  | o- ramdisk ................................. [Storage Objects: 0]
  o- iscsi ..................................... [Targets: 0]
  o- loopback .................................. [Targets: 0]

Creating block storage:
----------------------
/> /backstores/block create serverX.disk1 /dev/iscsi_vg1/iscsi_lv1 

Create IQN for the target: (iSCSI Qualified Name)
--------------------------
/> /iscsi create iqn.2015-11.com.example:serverX

Create a ACL for desktopX:
--------------------------
/> /iscsi/iqn.2015-11.com.example:serverx/tpg1/acls create
                                             iqn.2015-11.com.example:desktopX

LUN Mapping:
-----------
/> /iscsi/iqn.2015-11.com.example:serverx/tpg1/luns create /backstores/block/serverX.disk1

Create a Portal for Server on port 3260:
----------------------------------------
/> /iscsi/iqn.2015-11.com.example:serverx/tpg1/portals create 172.25.11.200+X (server)

Note1: Here 'X' is server IP (vm)

/> saveconfig
/> exit

Note: /> /iscsi/iqn.2015-11.com.example:serverx/tpg1/portals delete 0.0.0.0 3260

Client Configuration Part:
=========================

Step 05: Package Installation
-----------------------------

[root@desktopX ~]# rpm -qa | grep iscsi-initiator-utils

[root@desktopX ~]# yum install iscsi-initiator-utils

Step 06: Change default Initiator Name (Defined in ACL)
-------------------------------------------------------

[root@desktopX ~]# vim /etc/iscsi/initiatorname.iscsi

InitiatorName=iqn.2015-11.com.example:desktopX

Step 07: Service Restart and Check Status
-----------------------------------------
[root@desktopX ~]# systemctl enable iscsi
[root@desktopX ~]# systemctl restart iscsi
[root@desktopX ~]# systemctl status iscsi

Step 08: Target Discover
------------------------

[root@desktopX ~]# iscsiadm -m discovery -t st -p 172.25.11.200+X  

172.25.11.200+X:3260,1 iqn.2015-11.com.example:serverx (output)

Step 09: Connect the iSCSI Target and Verify:
---------------------------------------------
[root@desktopX ~]# lsblk 
[root@desktopX ~]# iscsiadm -m node -T iqn.2015-11.com.example:serverx 172.25.11.200+X -l
[root@desktopX ~]# lsblk  
[root@desktopX ~]# systemctl restart iscsi
[root@desktopX ~]# fdisk -l 

Step 10: Create a Partition and Mount
-------------------------------------

[root@desktopX ~]# fdisk /dev/sdb          (i.e: sdb)
[root@desktopX ~]# mkfs.xfs /dev/sdb       (i.e: sdb1)
[root@desktopX ~]# partprobe /dev/sdX      (i.e: sdb)
[root@desktopX ~]# mkdir /iscsidisk1
[root@desktopX ~]# mount /dev/sdX /iscsidisk1
[root@desktopX ~]# df -HT

Step 11: Parmanent Mount:
------------------------
[root@desktopX ~]# vim /etc/fstab

/dev/sdX	/iscsidisk1        xfs    defaults        0 0

[root@desktopX ~]# mount -a


