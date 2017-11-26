```sh

X = Virtual Machine no
Y = Batch No

Working with Linux File/Directory permission & owernship:
==========================================================
[student@serverX ~]$ su 
 password: ******

[root@serverX ~]# mkdir linuxY
[root@serverX ~]# cd linuxY
[root@serverX linuxY]# ls
[root@serverX linuxY]# mkdir lesson06
[root@serverX linuxY]# cd lesson06
[root@serverX lesson06]# touch test1
[root@serverX lesson06]# mkdir newdir
[root@serverX lesson06]# cp /etc/passwd  .          ; copy to current dir
[root@serverX lesson06]# ls -l

d rwxr-xr-x. 2 root root 4096 Sep 26 09:33 newdir
- rw-r--r--. 1 root root    0 Sep 26 09:33 test1
- rw-r--r--. 1 root root 1389 Sep 26 09:33 passwd
1      2     3   4   5     6          7      8

1 - Linux File/dir types
2 - user/group/others permission, (.) => Special Permission
3 - file Hard link
4 - file/dir owner 
5 - file/dir group owner
6 - file/dir size
7 - created/modify date & Time
8 - file/dir name

1 - Linux File/dir types: (5 types) common + 2(uncommon) 
--------------------------------------------------------
 - = regular file (text/image/audio/video/software/doc)
 d = directory     (folder)
 b = device file  (hdd/usb/fd/cd/iso)
 c = character device (com/parallel/lpt)
 l = link file        (link file)
 p = prcoess
 s = socket

Verify Different Types of File in Linux:
---------------------------------------
[root@serverX lesson06]# cd /dev
[root@serverX lesson06]# ll
[root@serverX dev]# ls -l | less        ; press 'q' for quiet
[root@serverX dev]# cd -
[root@serverX lesson06]# 


working with link file:
========================

Type of link file:
------------------
 1) hard link  - same inode number (backup)
 2) soft link - different inode number (if original file delete, linked file delete too).

[root@serverX lesson06]# ls -li 
[root@serverX lesson06]# cat passwd
[root@serverX lesson06]# ln -s  passwd passwd-soft        ;softlink
[root@serverX lesson06]# ln passwd passwd-hard		;hardlink
[root@serverX lesson06]# ll
[root@serverX lesson06]# cat passwd-hard
[root@serverX lesson06]# cat passwd-soft
[root@serverX lesson06]# ls -li
[root@serverX lesson06]# echo goodbye >> passwd
[root@serverX lesson06]# tail passwd
[root@serverX lesson06]# tail passwd-hard
[root@serverX lesson06]# tail passwd-soft
[root@serverX lesson06]# rm -f passwd
[root@serverX lesson06]# ll
[root@serverX lesson06]# tail passwd-soft
[root@serverX lesson06]# ln -s documents /home/student/Documents

 Hardlink - file
 softlink - file & folder (start with 'l')

 Field no: 2 (Permission) 
 -----------------------
[root@serverX lesson06]#  ll

 - rw-r--r--. 1 root root    0 Sep 26 09:52 test1
 d rwxr-xr-x. 2 root root 4096 Sep 26 09:33 newdir
     2

 subfield:
 ---------
  - rw- r-- r-- .  = 644 (file)
  d rwx r-x r-x .  = 755 (dir)  
     u   g   o  A 

 u = user 
 g = group
 o = others
 r = read (4)
 w = write (2)
 x = execute (1)
 - = no permission (0)
 . = ACL Permission (+)

   **** Special Permission (S,s,T,t)


 Group:      users                   others
 ======     =========               ========
 support:   rana, liza, sujan    all (except group members)

 File/dir permission for new file/dir:
=====================================
 dir: 755
 file: 644

Maximum File Permission: 666      =>  (rw-rw-rw-)
Maximum Directory Permission: 777 =>  (rwxrwxrwx)

[root@serverX lesson06]# groupadd support
[root@serverX lesson06]# useradd -G support rana
[root@serverX lesson06]# useradd -G support liza
[root@serverX lesson06]# useradd -G support sujan
[root@serverX lesson06]# useradd sakib

[root@serverX lesson06]#  cat /etc/group | grep support
support:x:5005:rana,liza,sujan

 user: (rana) : full permission
 group: support: read
 oters: others : no

[root@serverX lesson06]# ls -l
 -rw-r--r--. 1 root root 0 Jun 14 19:55 test1

[root@serverX lesson06]# chmod 740 test1
[root@serverX lesson06]# ls -l
-rwxr-----. 1 root root 0 Jun 14 19:55 test1

[root@serverX lesson06]# chown rana test1
[root@serverX lesson06]# ls -l
-rwxr-----. 1 rana root 0 Jun 14 19:55 test1

[root@serverX lesson06]# chgrp support test1
[root@serverX lesson06]# ls -l 
-rwxr-----. 2 rana support 0 Sep 26 09:52 test1

 Testing:
 --------
 (user)
[root@serverX lesson06]# su rana
[rana@serverX lesson06]$ ls
[rana@serverX lesson06]$ echo this is rana > test1       ; rana can rw
[rana@serverX lesson06]$ cat test1
[rana@serverX lesson06]$ exit

 (Group)
[root@serverX lesson06]# su liza
[liza@serverX lesson06]$ ls
[liza@serverX lesson06]$ cat test1
[liza@serverX lesson06]$ echo this is liza > test1       ; read only
[liza@serverX lesson06]$ exit

 (Others)
[root@serverX lesson06]# su sakib
[sakib@serverX lesson06]$ cat test1   ; access denied 
[sakib@serverX lesson06]$ echo this is sakib > test 
[sakib@serverX lesson06]$ exit

 Linux Umask Value:
 -----------------
[root@serverX lesson06]# umask 
 0022

 permission value:
 ------------
 dir: 755
 file: 644
 
 Directory: (umask Calculation for Dir)
 -----------
  777
 0022
 ------
 0755

 File: (umask Calculation for File)
 ------
 666
0022
-----
 0644

New Mask: (0044)
---------
 0777
 0044
 -----
 0733

 File:
------
 0666
 0044
 -----
 0622

[root@serverX lesson06]# umask 0044     
[root@serverX lesson06]# umask 
0044
[root@serverX lesson06]# mkdir mydir
[root@serverX lesson06]# touch myfile
[root@serverX lesson06]# ll
drwx-wx-wx. 2 root root 4096 Jun 14 20:51 mydir (733)
-rw--w--w-. 1 root root    0 Jun 14 20:52 myfil (622)

 Note: File never support execute value for umask
 
 Parmanent Umask Value Change:
 ----------------------------
 [root@serverX lesson06]# cat -n /etc/profile
  :set nu

  62 umask 044   (don't change)

 [root@serverX lesson06]# reboot
 [root@serverX lesson06]# umask 
  0044

Linux SUID, SGID and Sticky Bit Concept:
----------------------------------------

 1 = sticky bit (t, T)
 2 = SGID  (s,S)
 4 = SUID (s,S)

 [root@serverX lesson06]# ls -ld /tmp
 [root@serverX lesson06]# which passwd
 [root@serverX lesson06]# ls -l /usr/bin/passwd
 -rwsr-xr-x. 1 root root 27832 Jun 10  2014 /usr/bin/passwd

 [root@serverX lesson06]# mkdir mydir
 [root@serverX lesson06]# ll
 [root@serverX lesson06]# chmod 777 mydir     ; regular permission
 [root@serverX lesson06]# ll
 [root@serverX lesson06]# chmod 1777 mydir    ; sticky bit
 [root@serverX lesson06]# ll
 [root@serverX lesson06]# chmod 2770 mydir    ; SGID Permission
 [root@serverX lesson06]# ll
 

 [root@serverX lesson06]# su student
 [student@serverX lesson06]$ ls /root
 [student@serverX lesson06]$ exit
 [root@serverX lesson06]# ls -l /usr/bin/ls
 -rwxr-xr-x. 1 root root 117616 Jun 10  2014 /usr/bin/ls

[root@serverX lesson06]# chmod 4755 /usr/bin/ls       ; SUID Permission

 [root@serverX lesson06]# ls -l /usr/bin/ls
 -rwsr-xr-x. 1 root root 117616 Jun 10  2014 /usr/bin/ls
  
 [root@serverX lesson06]# su student
 [student@serverX lesson06]$ ls /root
 [student@serverX lesson06]$ exit

```
