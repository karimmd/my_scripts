```sh

Working with Linux CLI:
=======================
=> Introduction to Linux Terminal
=> Introducing with Linux Shells
=> Linux Physical consoles
=> Psuedo Consoles
=> Remote Connection using SSH and Telnet
=> Bash History Commands 

[student@desktopX Desktop] $ 
[root@desktopX    Desktop] # 
  1       2        3       4 
 
 	1: user name
 	2: hostname
	3: user's current locaiton
	4: user types (root: #, regular user: $)

Linux User's Types:
-------------------
 => root user: Administrator (#)
 => system user: service (mail/ftp/games/daemon)-cannot login 
 => regular user: student, guest, sakib ($)

Working with Linux Shells & Terminal:
------------------------------------
[student@desktopX Desktop] $ echo $SHELL
[student@desktopX Desktop] $ chsh -l

Ref: Picture

Working with linux CLI:
-----------------------
 => Physical Consoles (Alt + Ctrl+ F1 - Alt + Ctrl + F6) 
	=> Alt + Ctrl + F1: GUI
	=> Alt + Ctrl + F2-F6: CMD

 => Pseudo Consoles (/dev/pts/x) or connection from GUI 
 => Telnet (unencrypted, TCP port 23)
 => SSH (encrypted, TCP Port 22)

 Alt + Ctrl + F1 => GUI                       - :0
 Alt + Ctrl + F2 => new CMD terminal (F2-F6)  - tty2-tty6
 
 Login: student
 pass: ****** 

 [student@desktopX ~]$ exit

 [student@desktopX Desktop]$ su 
 Password: ******

 [root@desktopX ~]# exit 

 screen:
 ------
 $ ctrl + l = srceen clear
 $ ctrl + shift  +++  = screen size increase (GUI)
 $ ctrl + "----" = screen size decrease  (GUI)
 $ ctrl + shift + "t" => new terminal (tab) (GUI)
 $ Alt+F2 (type gnome-terminal)

Linux Command Syntax/Pattern:
-----------------------------
    # command [optoin (-)] argument

 ex # userdel -r ikbal 

[student@desktopX Desktop]$ cd 
[student@desktopX ~]$ ls      ;list of files and dir.
[student@desktopX ~]$ ll      ;file and dir properties
[student@desktopX ~]$ ls -l
[student@desktopX ~]$ ls -la  ; details list with hidden files and dir
[student@desktopX ~]$ ls -li  ; list of inode no
[student@desktopX ~]$ ls -lZ  ; shows SELinux Context
[student@desktopX ~]$ ls -lh  ; size in Human Readable

      blue - dir  
      b&w - file
      red - compress (rpm/zip/rar)
      green - execute file
      yellow - device (terminal/cd/dvd/usb/hdd)
      cyan - link file
      magenta - Picture/image/media

[student@desktopX ~]$ pwd   ; present working directory

  "~" 	  => home dir
  "/" 	  => root partition
  "/root" => root's home dir
  "/home" => user's home
    i.e.: /home/student

[student@desktopX ~]$ => user's home dir 

 Working with Linux More Commands:
 ================================
[student@desktopX ~]$ who
[student@desktopX ~]$ whoami 
[student@desktopX ~]$ hostname
[student@desktopX ~]$ tty
[student@desktopX ~]$ date
[student@desktopX ~]$ cal 
[student@desktopX ~]$ cal 2016

[root@desktopX    ~]# lastb			  ; unsuccessful login user 
[student@desktopX ~]$ runlevel     		  ;(5-GUI, 3-CMD, n-none)
[student@desktopX ~]$ uname -r       	  	  ; kernel version
[student@desktopX ~]$ uname        		  ; OS name
[student@desktopX ~]$ cat /etc/redhat-release     ; redhat/centos version
[student@desktopX ~]$ top			  ; task manager
[student@desktopX ~]$ lastlog			  ; login details
[student@desktopX ~]$ free -m			  ; RAM Info
[student@desktopX ~]$ df -HT			  ; Disk info
[student@desktopX ~]$ uptime			  : system UPtiem info
[student@desktopX ~]$ ip addr
[root@desktopX ~]# fdisk -l
[student@desktopX ~]$ arp
[student@desktopX ~]$ logout

[student@desktopX ~]$ history  			; list of privious command
[student@desktopX ~]$ !292 			; 292 no command
[student@desktopX ~]$ !!   			; last command repeat agin
[student@desktopX ~]$ history -c 		; clear all previous history
[student@desktopX ~]$ history

 Shutdown
===========
[root@desktopX ~]# init 0
[root@desktopX ~]# poweroff
[root@desktopX ~]# shutdown -h now

restart:
=======
[root@desktopX ~]# reboot
[root@desktopX ~]# init 6
[root@desktopX ~]# shutdown -r now
[root@desktopX ~]# shutdown -r 5 now ; shutdown after 5 min
   
Linux Directory Structure:
-------------------------
[student@desktopX ~]$ cd /
[student@desktopX /]$ ls

bin   dev  home  lib64  mnt  proc  run   srv  tmp  var
boot  etc  lib   media  opt  root  sbin  sys  usr

 bin - user binary files ( executed by normal user)
 boot - system boot related file 
 dev - system device files (dvd/cd/hdd/fd)
 etc - all server configuration file
 home - regular user home dir
 lib - system libary files locations. libraries needed to execute the binaries in /bin/ and /sbin/. 
 media - system defaut mount point (DVD/ISO/SOFTware)
 mnt - mount point (DVD/HDD/USB)
 opt - optional (empty)
 proc - Also called 'proFS' system process related info (CPU,RAM, Process, Driver, Modules and Kernel)
 root - root user (superuser) home dir.
 run - service running data. Runtime data for processes started since the last boot.  
 sbin  - system binary ( used by root user)
 srv - Sort for Service. User's (/home/*) service related data. Like WWW, FTP etc.
 sys - Sort for system. '/sys' directory as a virtual filesystem (sysfs) mounted under /sys. similar as proc.
 tmp - temporary files (deleted after 10 days)
 usr - thirdparty software install location
 var - varibale file (mail/log/hosting/ftpdata)

 Important: /boot, /root, /etc, /mnt, /var, /dev, /usr, /proc, /sbin, /bin

   
[student@desktopX ~]$ cd  [enter]  ; back to home dir
[student@desktopX ~]$ cd /
[student@desktopX /]$ ls
[student@desktopX /]$ cd opt
[student@desktopX opt]$ pwd
[student@desktopX opt]$ cd
[student@desktopX ~]$

        =>  cd  /dir1/dir2/dir3 [path]  ; Linux

	=>  C:\di1\dir2\dir3>       ; Windows 

 => Absolute path /var/ftp/pub ; starting with "/"
 => Rlative path  var/ftp/pub  ; not starting with "/"

[student@desktopX ~]$ cd /var/log
[student@desktopX log]$ ls
[student@desktopX log]$ cd  ..  ; one step/dir back 
[student@desktopX var]$ cd  -  ; back to previous dir
[student@desktopX log]$ cd  /  ; to go root partion "/"
[student@desktopX /]$ cd  [dirname]  ; change to any dir
[student@desktopX ~]$ cd
[student@desktopX ~]$ ls
[student@desktopX ~]$ cd Music
[student@desktopX Music]$ cd ../Videos
[student@desktopX Videos]$ ls
[student@desktopX Videos]$ pwd
[student@desktopX Videos]$ cd 
[student@desktopX ~]$ mkdir linuxY
[student@desktopX ~]$ ls
[student@desktopX ~]$ cd linuxY
[student@desktopX linuxY]$ ls
[student@desktopX linuxY]$ pwd
[student@desktopX linuxY]$ mkdir lesson02
[student@desktopX linuxY]$ cd lesson02
[student@desktopX lesson02]$ ls
[student@desktopX lesson02]$ pwd

Test: Graphically (home/...........)

 class work:
 -----------
[student@desktopX lesson02]$ touch mycv               ; file create
[student@desktopX lesson02]$ ll
[student@desktopX lesson02]$ touch test1 test2 test3    ; multiple files create with single command
[student@desktopX lesson02]$ ll
[student@desktopX lesson02]$ mkdir dir1 dir2 dir3 ; multiple dirs create with single command
[student@desktopX lesson02]$ ll
[student@desktopX lesson02]$ touch file{1..10}
[student@desktopX lesson02]$ ll
[student@desktopX lesson02]$ mkdir cv_{rasel,sazib,liton}
[student@desktopX lesson02]$ ll
[student@desktopX lesson02]$ mkdir centos\ linux
[student@desktopX lesson02]$ ll
[student@desktopX lesson02]$ mkdir soft/windows/office -p
[student@desktopX lesson02]$ ll soft
[student@desktopX lesson02]$ touch soft/windows/test
[student@desktopX lesson02]$ cd soft/windows
[student@desktopX windows]$ pwd
[student@desktopX windows]$ ll 
[student@desktopX windows]$ cd /home/student/linuxX/lesson02

or
[root@desktopX windows]$ cd ../../
[root@desktopX lesson02]$ rm -rf *
[root@desktopX lesson02]$ ls

Working with Hidden file/dir:
----------------------------
[student@desktopX ]$ mkdir linux51/lesson02 -p
[student@desktopX ]$ cd linux51/lesson02
[student@desktopX lesson02]$ mkdir .training
[student@desktopX lesson02]$ touch .csl
[student@desktopX lesson02]$ ll
[student@desktopX lesson02]$ ls -la   ; a for hidden file/dir
[student@desktopX lesson02]$ mv .training training	 ; file rename
[student@desktopX lesson02]$ ll

[student@desktopX lesson02]$ touch test1
[student@desktopX lesson02]$ mkdir linux1

[student@desktopX lesson02]$ ll

 d rwx r-x  r-x .  2   student student   6 	Feb  4 18:06 	linux1
 - rw- r--  r-- .  1   student student   0 	Feb  4 18:06 	test1

 1 2a  2b   2c 2d  3    4        5       6 	    7	          8

 1: file/dir types
 2: file/dir permission:   2a: user permission, 2b: group permission, 2c: others permission 2d: Special Permission
 3: file/dir link (Hard Link)
 4: file/dir owner
 5: file/dir group owner
 6: file/dir size (byte)
 7: file/dir modify date
 8: file/dir name

Linux FIle & Dir types:
------------------------------
 d = directory     : regular directory
 l = link file    : /dev/stdin 
 s = socket        : /dev/log     
 - = regular file : text/any file
 p = Pipe file  : /dev/initctl        
 b = device CD/DVD/HDD : /dev/sdb, /dev/sr0
 c = character device (serial/prallel/printer): /dev/tty

s - A socket file is used to pass information between applications/process for communication purpose

[root@desktopX lesson02]$ cd /dev
[student@desktopX dev]$ ls -l | less
[student@desktopX dev]$ cd -  

 Note: press 'q' to quit 

 FIle/dir Permission:
 ---------------------------
 r = read
 w = write
 x = execute
 - = no permission
 . = Special Permission (+)

Copy/paste/remove/rename/delete
===============================
[student@desktopX lesson02]$ touch mycv
[student@desktopX lesson02]$ cp mycv myresume          ; file copy
[student@desktopX lesson02]$ ll
[student@desktopX lesson02]$ cp mycv /home/student       ; same name
[student@desktopX lesson02]$ cp mycv /home/student/newcv  ; diffrent name
[student@desktopX lesson02]$ cd /home/student
[student@desktopX student]$ ls
[student@desktopX student]$ cd -
[student@desktopX lesson02]$ cp /etc/passwd  .  ; copy to current dir
[student@desktopX lesson02]$ ls 
[student@desktopX lesson02]$ rm mycv            ; file remove 
[student@desktopX lesson02]$ ls 
[student@desktopX lesson02]$ rm  -f  test1      ; file delete without confirmation
[student@desktopX lesson02]$ ll  
[student@desktopX lesson02]$ mv myresume biodata   ; move or rename
[student@desktopX lesson02]$ mv myresume /home/student
[student@desktopX lesson02]$ ls
[student@desktopX lesson02]$ cp -r linux1 linux3   ; copy directory 
[student@desktopX lesson02]$ cp -rv /etc  .     ; copy directory with content to current
[student@desktopX lesson02]$ ls 
[student@desktopX lesson02]$ rmdir linux1     ; delete empty dir
[student@desktopX lesson02]$ rm -r etc   ; delete dir with content and confirmation
 C^
[student@desktopX lesson02]$ rm -rf  etc   ; delete dir with contains and without confirmation

[student@desktopX lesson02]$ ls
[student@desktopX lesson02]$ rm -rf  *  ; delete everything from curent dir
[student@desktopX lesson02]$ ls
