```sh

 Linux Partition Management:
============================
 Window File System: FAT32, NTFS
 Linux File sytem: ext2, ext3, ext4, XFS (current), 
		   vfat, swap, ZFS, GlusterFS.

 All device files location: /dev/*
 			   * hdd, dvd, cdrom, usb, serial, swap, tty

 BIOS (Basic Input Output System)
 UEFI (United Extensibel Firmware Interface)

 Partition Table Stucture:
 ------------------------
 BIOS ==> MBR (Master Boot Record)   
 UEFI ==> GPT(GUID Partition Table) 

 Type of HDD Data store Sectors:
 -------------------------------
 => 512 Byte   (87% used)
 => 4096 or 4k (96% used)

 MBR ==> 512-byte sectors, 2TB Max Partition Size
 GPT ==> 512-byte sectors, 9.4 Zettabytes Max Partition Size

 Total Partition: MBR - BIOS
 ----------------------------------------------------------
  Linux Partition = 15 (4 Primary + 11 Logical)
  Windows Partition: 63 C-Z, A- Floppy, B-zip

 Total Partition: GPT 
 ----------------------------------------------------------------------
 Total Partition: 128

 IDE/SATA/SAS/SCSI HDD: sda, sdb, sdc
 Virtual Machine: vda, vdb
 USB: sda1, sdb1
 DVD: dvd/sr0 
  
[root@desktopX ~]# fdisk -l ; all partition

 sda = 1st sata
 sdb = 2nd stata
 sdc = 3rd sata
 vda = 1st virtual disk
 vdb = 2nd virtual disk

SI Unit:
--------
1 kilobyte = 1000 bytes
1 megabyte = 1000 kilobytes
1 gigabyte = 1000 megabytes

IEC Unit:
--------
1 kibibyte (KiB) = 1024 bytes
1 mebibyte (MiB) = 1024 kilobytes
1 gibibyte (GiB) = 1024 megabytes

Convert from sectors to megabytes/gigabytes:
--------------------------------------------
1 kilobyte = 1024 bytes
1 megabyte = 1024 kilobytes
1 gigabyte = 1024 megabytes

500MB = 1024000 Sector

1024000 sectors can be converted to 500 megabytes as follows:
------------------------------------------------------------
1024000 sectors * 512 bytes per sector = 524288000 bytes
524288000 bytes / 1024 bytes per kilobyte = 512000 kibibytes
512000 kilobytes / 1024 kilobytes per megabyte = 500 Mebibytes

 Linux partition ID:
 ------------------
 NTFS - 7
 Extended - 5
 ext3/ext4/xfs  - 83
 swap - 82
 LVM - 8e
 vfat - f
 RAID - fd

[root@desktopX ~]# lsblk
[root@desktopX ~]# df -HT

[root@serverX ~]# fdisk -l

[root@serverX ~]# df -HT | grep vda

/dev/vda2      xfs       5.3G  1.1G  4.2G  20% /
/dev/vda1      xfs       521M   94M  427M  19% /boot

[root@serverX ~]# lsblk

Create New Extended Partition:
-----------------------------
[root@serverX ~]# fdisk -l

[root@serverX ~]# fdisk /dev/vda           ; MBR based 

 Command (m for help): m

   d   delete a partition
   l   list known partition types
   m   print this menu
   n   add a new partition
   p   print the partition table
   q   quit without saving changes
   t   change a partition's system id
   w   write table to disk and exit

 Command (m for help): p
 Command (m for help): n

Partition type:
   p   primary (3 primary, 0 extended, 1 free)
   e   extended

Select (default e): e

Selected partition 4
First sector (12314624-16777215, default 12314624): {press Enter}
Using default value 12314624
Last sector, +sectors or +size{K,M,G} (12314624-16777215, default 16777215): {press Enter}
Using default value 16777215
Partition 4 of type Extended and of size 4.1 GiB is set

 Command (m for help): p
 Command (m for help): w

[root@serverX ~]# fdisk -l

[root@serverX ~]# partprobe /dev/vda       ; partition table update

Create New Logical Partition:
-----------------------------
[root@serverX ~]# fdisk /dev/vda

Command (m for help): n
All primary partitions are in use
Adding logical partition 5
First sector (12316672-16777215, default 12316672): {press Enter}

Last .. +sectors or +size{K,M,G}. default 16777215): +350M {press Enter}  
Partition 5 of type Linux and of size 350 MiB is set

Command (m for help): p
Command (m for help): w

[root@serverX ~]# partprobe /dev/vda

Partition Format Command:
-------------------------
[root@serverX ~]# mkfs.xfs  /dev/vda5

Partition Mount:
----------------- 
[root@serverX ~]# mkdir /dataX
[root@serverX ~]# df -HT | grep vda

[root@serverX ~]# mount /dev/vda5 /dataX

[root@serverX ~]# df -HT | grep vda

Filesystem    Type     Size   Used  Avail Use% Mounted on
/dev/vda2      xfs       5.3G  1.1G  4.2G  20% /
/dev/vda1      xfs       521M   94M  427M  19% /boot
/dev/vda5      xfs       364M   19M  345M   6% /dataX

[root@serverX ~]# umount /dataX
[root@serverX ~]# df -HT | grep vda

Filesystem    Type     Size   Used  Avail Use% Mounted on
/dev/vda2      xfs       5.3G  1.1G  4.2G  20% /
/dev/vda1      xfs       521M   94M  427M  19% /boot

Parmanent Mount:
---------------
[root@serverX ~]# blkid /dev/vda5

[root@serverX ~]# vim /etc/fstab 

:set nu

UUID=1b42c7df-717a-420d-b054-81d5a48594b5   /dataX  xfs   defaults  0 0

or 
  
########### Add the following lines ############

 /dev/vda5    				/dataX    xfs     defaults    0  0

    1					2	3         4          5  6
  
 1 - partition
 2 - mountpoint
 3 - filesystem
 4 - options(quota,acl,ro,luks)
 5 - Dumping 

 *** specifies the option that need to be used by the dump program. 
 If the value is set to 0, then the partition is execluded from 
 taking backup and if the option is a nonzero value, the device will be backed up

 6 - file system check options

 *** mentions the fsck option. That is if the value is set to zero, 
 the device or partition will be excluded from fsck check and if 
 it is nonzero the fsck check will be run in the order in which 
 the value is set. The root partition will have this value set to
 one so that it will be checked first by fsck.

[root@serverX ~]# mount -a  ;fstab file update
[root@serverX ~]# mount 

[root@serverX ~]# reboot

[root@serverX ~]# df -HT | grep vda

 Partition delete
=====================

*** Warning ****

=> Remove fstab entry  (vim /etc/fstab)

=> Unmount        

=> Then delete

[root@serverX ~]# vim /etc/fstab

[root@serverX ~]# umount /dataX

[root@serverX ~]# df -HT

[root@serverX ~]# fdisk /dev/vda

Command (m for help): d
Partition number (1-5): 5

Command (m for help): p
Command (m for help): d
Partition number (1-4):4
Command (m for help): w

 Note: Before delete, you should unmount partion and delete fstab entry.

[root@serverX ~]# partprobe /dev/vda

[root@serverX ~]# fdisk -l
 /dev/vda1
 /dev/vda2
 /dev/vda3

Mount USB pendrive:
-------------------
[root@desktopX ~]# fdisk -l
Disk /dev/sdb: 32.2 GB, 32176472064 bytes
[root@desktopX ~]# mount /dev/sdb1 /mnt
[root@desktopX ~]# cd /mnt
[root@desktopX mnt]# ls
[root@desktopX mnt]# cp cv.docx /root/Desktop
[root@desktopX mnt]# cp /etc/passwd /mnt
[root@desktopX mnt]# cd
[root@desktopX ~]# umount /mnt
[root@desktopX ~]# cd /mnt
[root@desktopX mnt]# ls

 Mount DVD:
------------
[root@desktopX ~]# mount /dev/sr0 /media
[root@desktopX ~]# cd /media
[root@desktopX media]# ls
[root@desktopX media]# cd Packages
[root@desktopX Packages]# ls
[root@desktopX Packages]# cd 
[root@desktopX ~]# umount /media
[root@desktopX ~]# 

```
