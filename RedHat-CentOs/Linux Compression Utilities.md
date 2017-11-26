```sh

Linux Archive & Compression Utilities:
======================================

Working Machine: DesktopX

compression:
-------------- 
 Windows: zip, rar, 7zip
 linux: .gz, .bz2, .xz  optional (.zip, .rar) 
 
 Archive:
---------
 .tar
 
 Archive + compression:
------------------------
 .tar.gz
 .tar.bz2
 .tar.xz
 
 10 MB: .gz(4MB)compress, .bz2(3 MB)more compress, .xz(2MB)more and compress,

[root@desktopX ~]# mkdir /linuxY/lesson08 -p
[root@desktopX ~]# cd /linuxY/lesson08
[root@desktopX lesson08]# cp /etc/passwd .
[root@desktopX lesson08]# cp -rv /etc /linuxY/lesson08
[root@desktopX lesson08]# ls
[root@desktopX lesson08]# du -ch *  ; view size of file and dir
[root@desktopX lesson08]# du -sh etc

Archive (tar):
=============
[root@desktopX lesson08]# tar -cvf etcarchive.tar  etc  
[root@desktopX lesson08]# ls
[root@desktopX lesson08]# du -ch *
[root@desktopX lesson08]# rm -rf etc
[root@desktopX lesson08]# ls

 c = Create
 v = verbose
 f = files 
 x = extract 
 
Arcive extract:
--------------- 
[root@desktopX lesson08]# tar -xvf etcarchive.tar 
[root@desktopX lesson08]# ll

archive + compress:
-------------------
[root@desktopX lesson08]# tar -czvf etcbackup.tar.gz etc
[root@desktopX lesson08]# ll
[root@desktopX lesson08]# du -ch etcbackup.tar.gz
 
 extract:
---------
[root@desktopX lesson08]# rm -rf etc
[root@desktopX lesson08]# tar -xzvf etcbackup.tar.gz
[root@desktopX lesson08]# ll
 
archive + more compress:
----------------------
[root@desktopX lesson08]# tar -cjvf etc.tar.bz2 etc
[root@desktopX lesson08]# ll
[root@desktopX lesson08]# du -ch etc.tar.bz2

extract: (.bz2)
========
[root@desktopX lesson08]# rm -rf etc
[root@desktopX lesson08]# tar -xjvf etc.tar.bz2
[root@desktopX lesson08]# ls

New: (More and More Compress)
------------------------------
[root@desktopX lesson08]# tar -cJvf etc.tar.xz etc
[root@desktopX lesson08]# ll
[root@desktopX lesson08]# du -ch etc.tar.xz

extract: (.xz)
========
[root@desktopX lesson08]# tar -xJvf etc.tar.xz 
[root@desktopX lesson08]# ls

Only compress:
--------------
[root@desktopX lesson08]# seq 10000000 > number
[root@desktopX lesson08]# ls 
[root@desktopX lesson08]# du -sh number

[root@desktopX lesson08]# gzip number      ;[file name]
[root@desktopX lesson08]# ls
etc  passwd number.gz

[root@desktopX lesson08]# du -sh number.gz

extract:
---------
[root@desktopX lesson08]# gunzip number.gz
[root@desktopX lesson08]# ls
etc  passwd number

more compress:
--------------	
[root@desktopX lesson08]# bzip2 number
[root@desktopX lesson08]# ls
etc  passwd number.bz2

[root@desktopX lesson08]# du -sh number.bz2

extract:
---------
[root@desktopX lesson08]# bunzip2 number.bz2
[root@desktopX lesson08]# ls
etc  passwd  number 

more and more compress:
-----------------------
[root@desktopX lesson08]# xz number 
[root@desktopX lesson08]# ls
 etc passwd number.xz

[root@desktopX lesson08]# du -sh number.xz

extract:
--------
[root@desktopX lesson08]# unxz number.xz
[root@desktopX lesson08]# ls 
etc  passwd  number 

Extra:
-----
[root@desktopX lesson08]# tar -tvf etcarchive.tar    ;view content
[root@desktopX lesson08]# tar -cvf archive.tar dir1 dir2 dir3 
[root@desktopX lesson08]# tar -xvf archive.tar 

(optional)
[root@desktopX lesson08]# mkdir new
[root@desktopX lesson08]# tar -xvf etcarchive.tar -C new

```
