```sh

Lesson: User and Group Administration
---------------------------------------------------------
[root@serverX ~]# cat  /etc/passwd  |  less

 UID
 ------
 root : 0
 system user: 1 - 999
 regular user: 1000 +

[root@serverX ~]# useradd tarek
[root@serverX ~]# tail /etc/passwd 
[root@serverX ~]# cat /etc/passwd | grep tarek

tarek: x: 1001: 1001:   :/home/tarek  :/bin/bash
  1    2   3     4    5       6           7

1 - username 
2 - user password info (/etc/shadow)
3 - userid (UID)
4 - groupid (GID): primary 
5 - user's comment/descriptions
6 - user's home dir
7 - user's shell

[root@serverX ~]# id tarek
uid=1001(tarek) gid=1001(tarek) groups=1001(tarek)

[root@serverX ~]# tail /etc/shadow    ; user password related info

[root@serverX ~]# useradd mahfuz   ; user create
[root@serverX ~]# useradd murshid

[root@serverX ~]# passwd mahfuz


Alt+F1 -- Alt+F6

login: mahfuz        ; login as regular user
pass: 123            ; (note: please numlock on)

[root@serverX ~]# grep 'mahfuz\|murshid' /etc/shadow ; 2 user information

[root@serverX ~]# groupadd trainer      ; group add
[root@serverX ~]# groupadd staff         ; group add

[root@serverX ~]# cat /etc/group     ; group related info

trainer :x:  1003: 
   1     2    3   4
 1 - group name
 2 - group password info (/etc/gshadow)
 3 - gid
 4 - group member
 
[root@serverX ~]# grep trainer /etc/group  ; check trainer group
trainer:x:1003:

[root@serverX ~]# gpasswd -M mahfuz,murshid  trainer     ; '-M' for members
[root@serverX ~]# grep trainer /etc/group 
trainer:x:1003:mahfuz,murshid

[root@serverX ~]# usermod -G trainer tarek  ;existing user modify
[root@serverX ~]# useradd -G trainer  belal  ; newuser to group

[root@serverX ~]# cat /etc/group | grep trainer  
trainer:x:1003:murshid,mahfuz,tarek,belal

[root@serverX ~]# useradd ikbal
[root@serverX ~]# passwd ikbal

[root@serverX ~]# usermod -G trainer,staff  ikbal ; single user assign to multiple groups
[root@serverX ~]# grep staff /etc/group 
[root@serverX ~]# grep trainer /etc/group 

[root@serverX ~]# id ikbal

[root@serverX ~]# useradd -u 3000 roman ; user careate with UID 
[root@serverX ~]# grep roman /etc/passwd

[root@serverX ~]# groupadd -g 3100 admin
[root@serverX ~]# tail /etc/group

[root@serverX ~]# groupmod -n faculty trainer  ;change group name
[root@serverX ~]# tail /etc/group

[root@serverX ~]# gpasswd -d ikbal staff       ; remove from group
[root@serverX ~]# grep staff /etc/group 

[root@serverX ~]# tail /etc/shadow
[root@serverX ~]# passwd -d ikbal               ; password remove 

[root@serverX ~]# tail /etc/shadow

Login regular user:
-------------------
Linux GUI terminal: 1   (Alt + Ctrl + F1)
Linux Command Terminal: (Alt+Ctrl+F2  -  Alt + Ctrl + F6)

Virtual Machine:
----------------

Alt+F1 -- Alt+F6

login: mahfuz        ; login as regular user
pass: 123            ; (note: please numlock on)

[mahfuz@serverX ~]$ tty   ; terminal [pts0 -> GUI, tty(n)-> CMD]

[mahfuz@serverX ~]$  su -   ; same location of regular user
passwd: *****  (root's password)

[root@serverX ~]# exit
[mahfuz@serverX ~]$ exit                ; exit from super user
 login: 
[root@serverX ~]# grep student /etc/passwd 
[root@serverX ~]# usermod -c "Linux X student" student 

[root@serverX ~]# grep student /etc/passwd 
student:x:1000:1000:Linux X student:/home/student:/bin/bash

[root@serverX ~]# grep roman /etc/passwd
 roman:x:1003:1003::/home/roman:/bin/bash

[root@serverX ~]#  mkdir /newhome/roman -p
[root@serverX ~]#  usermod -d /newhome/roman roman 

[root@serverX ~]#  grep roman /etc/passwd
roman:x:1003:1003: :/newhome/roman:/bin/bash

[root@serverX ~]# cat /etc/shells 

[root@serverX ~]#  grep mahfuz /etc/passwd  
[root@serverX ~]#  usermod -s /sbin/nologin  mahfuz    ;change user shell
[root@serverX ~]#  grep mahfuz /etc/passwd  
mahfuz:x:1002:1002::/home/mahfuz:/sbin/nologin

Check: Alt + F3 (use username password)

[root@serverX ~]# usermod -s /bin/bash mahfuz   ;shell enable

Check: Alt + F3 (use username password)

[root@serverX ~]#  usermod -L mahfuz     ; user  account    lock
[root@serverX ~]# grep mahfuz /etc/shadow
mahfuz: ! $.............../:16106:10:30:7:::

Check: Alt + F3 (use username password)

[root@serverX ~]#  usermod -U mahfuz     ; user  account  unlock
[root@serverX ~]#  grep mahfuz /etc/shadow
mahfuz: $.............../:16106:10:30:7:::

[root@serverX ~]# userdel tarek  ; user delete without home dir

or

[root@serverX ~]# userdel -r tarek  ; delete user with home dir
[root@serverX ~]# cat /etc/passwd

[root@serverX ~]# groupdel staff	; groupdel 
[root@serverX ~]# tail /etc/group        

[root@serverX ~]# w   ; user whats they are doing

[root@serverX ~]# useradd -u 2000 -c "BOSS" -d /opt -s /sbin/nologin boss
[root@serverX ~]# grep boss /etc/passwd 

============== Linux 51 (16-2-16) =======

[root@serverX ~]# useradd rumon
[root@serverX ~]# passwd rumon

Alt+F3

Login: rumon
pass: *****

[rumon@serverX ~]$ useradd razib
 -bash: /usr/sbin/useradd: Permission denied

 What is SUDO do ?
 -----------------
 Sudo allows a permitted user to execute a specifc command or a 
 group of commands or all commands as the superuser.
 
  regular user: rumon, rony, sathi
	=> rm,cp,mv,
	=> mkdir,touch
	=> pwd,free -m,
	=> lsblk, df -HT
	=> ip addr, tail

 Command run from: /bin/

  super user: root
	=> useradd, passwd, groupadd
	=> setup, systemctl 
	=> shutdown, poweroff
 	=> systemctl restart network.service 

 Command run from: /sbin

Note:  [root@serverX ~]# which useradd  ; command for location of   useradd command 

 Editing sudo configuration File:
 --------------------------------

 Rules 1: permit for all
 -----------------------
 [root@serverX ~]# visudo 

 :set nu
 
 98   root    ALL=(ALL)    ALL
 99   rumon   ALL=(ALL)    ALL    ; rummon allow for any command

:X (save and exit)
 
Test:
-----
[root@serverX ~]# su rumon
[rumon@serverX ~]$ useradd razib

[rumon@serverX ~]$ sudo useradd razib
[sudo] password for rumon: ****
[rumon@serverX ~]$ tail /etc/passwd
[rumon@serverX ~]$ exit

Working with /etc/shadow file:
------------------------------
[root@serverX ~]# useradd sathi
[root@serverX ~]# passwd sathi

[root@serverX ~]# tail /etc/shadow | grep sathi
sathi:$6$ciiMIfom$cPpqBIf2NOwan2byi5BUA.G6D0iM/g.tw7fcUyLDWIs.nbp0:16592:0:99999:7:::

Alt+F2

Login: sathi
passL: 123

[root@serverX ~]# chage -l sathi          ;password info 

Last password change                                    : MM DD, YYYY
Password expires                                        : never
Password inactive                                       : never
Account expires                                         : never
Minimum number of days between password change          : 0
Maximum number of days between password change          : 99999
Number of days of warning before password expires       : 7

password: P@ssword123  (new password)

[root@serverX ~]# chage sathi
 Minimum Password age [0]: 3
 Maximum Password age [99999]: 30
 Last Password Changed (YYYY-MM-DD): Press Enter (today)
 Password Expiration Warning [7]: 5 
 Password Inactive [-1]: 5 
 Account Expiration Date (YYYY-MM-DD) [-1]: YYYY-MM-DD

 note: If press Enter account never expire 

[root@serverX ~]# date
[root@serverX ~]# date MMDDHHMMYY 
[root@serverX ~]# date

============= More commands ==============

[root@serverX ~]# grep sathi /etc/shadow
[root@serverX ~]# chage -l sathi
[root@serverX ~]# date -d "+30 days"  

[root@serverX ~]# chage -M 90 sathi       ;every 90 days
[root@serverX ~]# chage -l sathi
[root@serverX ~]# grep sathi /etc/shadow
[root@serverX ~]# chage -d 0 sathi       ;must changed password in next login

[root@serverX ~]# vim /etc/login.defs  ;user password related info 

 25  PASS_MAX_DAYS   99999
 26  PASS_MIN_DAYS   0
 27  PASS_MIN_LEN    5
 28  PASS_WARN_AGE   7

===================================  x  ===========================

 Rules 2: shutdown disallow
 --------------------------
 52  Cmnd_Alias SHUTDOWN = /usr/sbin/shutdown, /usr/sbin/poweroff, /usr/sbin/reboot
 99 rumon ALL=(ALL) ALL, !SHUTDOWN
 
  Rules 3: permit for specific command
 ------------------------------------
 52  Cmnd_Alias RUMON = /usr/sbin/useradd, /usr/sbin/userdel 
 99 rumon ALL=(ALL) RUMON

Rules 4: permit group (support) for specific command
 ----------------------------------------------------

 52  Cmnd_Alias SUPPORT = /usr/sbin/fdisk, /usr/sbin/passwd, 
 109 %support  ALL=(ALL)       SUPPORT
