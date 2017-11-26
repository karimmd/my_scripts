```sh

Lab Setup:
----------
Application => systemtools => Vritual Machine Manager

 desktopX# virsh snapshot-revert serverX rh200
 
 Working with Linux Swap Partition:
 ----------------------------------
[root@serverX ~]# free -m    ; memory info physical memory & swap space

 Minimum required Swap Memory:
 ------------------------------
 RAM		Recommended Swap Space:
 --------------------------------------
 up to 4GB		at least 2GB
 up to 16GB		at least 4GB
 up to 64GB		at least 8GB
 64GB to 256GB		at least 16GB

[root@serverX ~]# fdisk -l
 /dev/vda2  40183   40314  1048576   82  Linux swap / Solaris

[root@serverX ~]# lsblk

[root@serverX ~]# fdisk /dev/vda

Command (m for help): p
Command (m for help): n

Partition type:
   p   primary (3 primary, 0 extended, 1 free)
   e   extended

Select (default e): e
Selected partition 4
First sector (12314624-16777215, default 12314624): {Press Enter}
Using default value 12314624
Last sector, +sectors or +size{K,M,G} (12314624-16777215, default 16777215): {Press Enter}
Using default value 16777215
Partition 4 of type Extended and of size 4.1 GiB is set
Command (m for help): n

All primary partitions are in use
Adding logical partition 5
First sector (12316672-16777215, default 12316672): {Press Enter}
Using default value 12316672
Last sector, +sectors or +size{K,M,G} (12316672-16777215, default 16777215): +750M
Partition 5 of type Linux and of size 750 MiB is set

Command (m for help): p
Command (m for help): t
Partition number (1-5, default 5): 5
de (type L to list all codes): L
Hex code (type L to list all codes): 82
Change type of partition 'Linux' to 'Linux swap / Solaris'

Command (m for help): p

Command (m for help): w

[root@serverX ~]# partprobe /dev/vda

[root@serverX ~]# swapoff -a
[root@serverX ~]# free -m

[root@serverX ~]# mkswap /dev/vda5
Setting up swapspace version 1, size = 511996 KiB
no label, UUID=7906ac34-4e2a-4b06-b57d-79dd6c66399a

[root@serverX ~]# free -m
             total       used       free     shared    buffers     cached
Mem:           994        141        852          6          0         63
-/+ buffers/cache:         77        916
Swap:            0          0          0

[root@serverX ~]# swapon /dev/vda5
[root@serverX ~]# free -m
             total       used       free     shared    buffers     cached
Swap:          749          0        699

[root@serverX ~]# swapon -a   ;all
[root@serverX ~]# free -m
             total       used       free     shared    buffers     cached
Swap:         1260          0       1211

[root@serverX ~]# swapon -s 

Filename       Type            Size    Used    Priority
/dev/vda5      partition       716796  0       -1
/dev/vda3      partition       524284  0       -2

(Optional)
============
[root@serverX ~]# blkid /dev/vda5
/dev/vda5: UUID="ff6b7c42-f875-4562-b51b-9e245017e37a" TYPE="swap" 

[root@serverX ~]# vim /etc/fstab 
 :set nu

#UUID=aea149e5-a8b4-4fe9-be5e-fce23877468c swap defaults   0 0   ;comment with #'
/dev/vda5          swap                    swap defaults   0 0

[root@serverX ~]# mount -a
[root@serverX ~]# swapoff -a 
[root@serverX ~]# swapon -a
[root@serverX ~]# free -m 

or

[root@serverX ~]# reboot
[root@serverX ~]# free -m 

```
