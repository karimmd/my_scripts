```sh

Text Processing tools: (Grep/tail/cat/head/less)
-----------------------------------------------
 X = Station No
 Y = Batch No
 
[student@desktopX ~]$ cd 
[student@desktopX ~]$ mkdir linuxY/lesson03 -p
[student@desktopX ~]$ cd linuxY/lesson03/
[student@desktopX lesson03]$ ls
[student@desktopX lesson03]$ cp /etc/passwd .
[student@desktopX lesson03]$ ls
[student@desktopX lesson03]$ touch test
[student@desktopX lesson03]$ ls

[student@desktopX lesson03]$ cat test    
[student@desktopX lesson03]$ cat passwd
[student@desktopX lesson03]$ clear
[student@desktopX lesson03]$ echo hello         
[student@desktopX lesson03]$ echo hello > test
[student@desktopX lesson03]$ cat test
[student@desktopX lesson03]$ echo hi > test        ; replace
[student@desktopX lesson03]$ cat test
[student@desktopX lesson03]$ echo hello world ! >> test    ; append 
[student@desktopX lesson03]$ cat test
[student@desktopX lesson03]$ history
[student@desktopX lesson03]$ history > command-list
[student@desktopX lesson03]$ ls
[student@desktopX lesson03]$ cat command-list

[student@desktopX lesson03]$ cat passwd     ; concatinate
[student@desktopX lesson03]$ cat -n passwd     ; concatinate
[student@desktopX lesson03]$ less passwd    ; Scrolling 
[student@desktopX lesson03]$ more passwd    ; file reading without cat (down)
[student@desktopX lesson03]$ head  passwd   ; 1st 10 l ines
[student@desktopX lesson03]$ tail passwd    ; last 10 lines read

[student@desktopX lesson03]$ tail  -n 5 passwd ; last 5 lines
[student@desktopX lesson03]$ head -n  5 passwd   ; 1st 5 lines

[student@desktopX lesson03]$ grep -n root passwd  ; search root keyword in passwd file
root:x:0:0:root:/root:/bin/bash
operator:x:11:0:operator:/root:/sbin/nologin

[student@desktopX lesson03]$ tail passwd | grep root  ;search root keyword in last 10 lines
[student@desktopX lesson03]$ head passwd | grep root

[student@desktopX lesson03]$ cut -d ":" -f 1 passwd 
[student@desktopX lesson03]$ cut -d ":" -f 1,3 passwd 
[student@desktopX lesson03]$ cut -d ":" -f 1-4 passwd 
[student@desktopX lesson03]$ cut -d ":" -f 1 passwd > userlist
[student@desktopX lesson03]$ cat userlist

[student@desktopX lesson03]$ head passwd | grep root | cut -d ":" -f 1
 root 
 operator 
 
[student@desktopX lesson03]$ su 
  :****** 

[root@desktopX lesson03]# locate hosts
[root@desktopX lesson03]# updatedb 
[root@desktopX lesson03]# locate sshd_config 
[root@desktopX lesson03]# locate -i .jpg  ;including case sensitve
[root@desktopX lesson03]# find / -name root  ; root name file    
[root@desktopX lesson03]# find /etc -type d -name selinux   
[root@desktopX lesson03]# find / -type f -name passwd 
[root@desktopX lesson03]# find / -size +10M   ; size more than 10MB
[root@desktopX lesson03]# find / -size -10M  ; size less than 10M 
[root@desktopX lesson03]# find /home -name student -exec cp -rf {} /opt \;
[root@desktopX lesson03]# cd /opt
[root@desktopX opt]# ls
[root@desktopX lesson03]# man find    ; command manual for find (press 'q' for quiet)
[root@desktopX lesson03]# info cat    ; 
[root@desktopX lesson03]# useradd --help 
[root@desktopX lesson03]# exit  
