```sh

Lab Setup:
----------
Application => systemtools => Vritual Machine Manager

 desktopX# virsh snapshot-revert serverX rh200

 LVM (Logical Volume Manager)
-----------------------------

 Storage:
 	=> Local  (Limited) - HDD 
	=> Network (Unilimited)- SAN

[root@localhost ~]# fdisk -l

[root@localhost ~]# fdisk /dev/vda  
 
Command (m for help): n

Select (default e): e
Selected partition 4
First sector (12314624-16777215, default 12314624): {Press Enter}
Using default value 12314624
Last sector, +sectors or +size{K,M,G} (12314624-16777215, default 16777215): {Press Enter}
Using default value 16777215
Partition 4 of type Extended
Command (m for help): p

Command (m for help): n
First sector (902815744-976771071, default 902815744):  [press Enter]
Last ... +size{K,M,G} (902815744-976771071, default 976771071): +250M 
Command (m for help): p
Command (m for help): t
Command (m for help): Enter your patition no
Command (m for help): l
Command (m for help): 8e
Command (m for help): p
Command (m for help): w

Note: Do 2 more parttion for LVM 

[root@localhost ~]# lsblk

[root@localhost ~]# partprobe /dev/vda 

Physical Volume Create:
-----------------------

[root@localhost ~]# pvcreate /dev/vda5 
[root@localhost ~]# pvcreate /dev/vda6 
[root@localhost ~]# pvcreate /dev/vda7

[root@localhost ~]# pvdisplay 

Group Volume Create:
-----------------------
[root@localhost ~]# vgcreate vg1 /dev/vda5 /dev/vda6 /dev/vda7
[root@localhost ~]# vgdisplay 

Note for Exam: vgcreate �s 32M vg1 /dev/vda5 /dev/vda6 /dev/vda7

Logical Volume Create:
----------------------
[root@localhost ~]# lvcreate -n lv1 -L 400M vg1

or  (note: Defautl PE Size 4MiB)

[root@localhost ~]# lvcreate -n lv1 -l 100 vg1

[root@localhost ~]# lvdisplay
[root@localhost ~]# mkfs.xfs /dev/vg1/lv1 
[root@localhost ~]# mkdir /lvdata
[root@localhost ~]# mount /dev/vg1/lv1 /lvdata
[root@localhost ~]# df -HT 
[root@localhost ~]# 

Parmanent Mount:
----------------
[root@localhost ~]# vim /etc/fstab
/dev/vg1/lv1	/lvdata     xfs    defaults  0 0

[root@localhost ~]# mount -a
[root@localhost ~]# mount 

VG Extended:
------------
=> fdisk /dev/vda   (300 MB) 
=> partprobe /dev/vda

[root@localhost ~]# pvcreate /dev/vda8 

=> vgextend

[root@localhost ~]# vgextend vg1 /dev/vda8   
[root@localhost ~]# vgdisplay

=> lvextend

[root@localhost ~]# lvextend -L +100M /dev/vg1/lv1 
[root@localhost ~]# df -HT 
[root@localhost ~]# xfs_growfs /lvdata
[root@localhost ~]# df -HT

Lv remove:
----------
[root@localhost ~]# vim /etc/fstab           ;remove fstab entery
[root@localhost ~]# umount /lvdata
[root@localhost ~]# lvremove /dev/vg1/lv1

VG Remove:
----------
[root@localhost ~]# vgremove vg1

PV Remove:
----------
[root@localhost ~]# pvremove /dev/vda5           
[root@localhost ~]# pvremove /dev/vda6           
[root@localhost ~]# pvremove /dev/vda7          
[root@localhost ~]# pvremove /dev/vda8           

[root@localhost ~]# fdisk /dev/vda
Command (m for help): d
Partition number (1-8, default 8): 4
Command (m for help): w

[root@localhost ~]# partprobe /dev/vda 
[root@localhost ~]# fdisk -l
 /dev/vda1
 /dev/vda2
 /dev/vda3

[root@localhost ~]# reboot

```
