```sh
Linux Boot up Process:
----------------------
							      ==> CMD (tty)		
BIOS/UEFI => MBR/GPT => GRUB2 => Kernel => systemd => Target =>
						 	      ==> GUI (pts)
systemd:
--------
One of the major changes in RHEL/CentOS 7.0 is the swtich to systemd,
a system and service manager, that replaces SysV and Upstart used in previous 
releases of Red Hat Enterprise Linux. systemd is compatible with SysV and 
Linux Standard Base init scripts.

=> Fedora 17/RHEL/CentOS6 = SystemV/init
=> Ubuntu/SUSE/Debian = upstart
=> Fedora 18+/RHEL/CentOS7/Ubuntu-15 = systemd

Change Default Boot Time:
-------------------------
[root@serverX ~]#  vim /boot/grub2/grub.cfg 
 :set nu

 63   set timeout=40

[root@serverX ~]# reboot

Grub Entry Customize:
--------------------
[root@serverX ~]# vim /boot/grub2/grub.cfg 

=============== Old ==============
76 menuentry 'CentOS Linux, with Linux 3.10.0-123.el7.x86_64' 
91 menuentry 'CentOS Linux, with Linux 0-rescue-fdbe8dca6eb044b6895149fc28e4a871'

=============== New ==============
76 menuentry 'Linux Server'
91 menuentry 'CentOS Recovery mode'

[root@serverX ~]# reboot

Dual Boot Setting:
==================
[root@desktopX ~]# fdisk -l

    Device Boot      Start         End      Blocks   Id  System
 /dev/sda1   *        2048     4194303     2096128    7  HPFS/NTFS/exFAT
 /dev/sda2         4194304   360402758   178104227+   7  HPFS/NTFS/exFAT

In this example, /dev/sda1 is the recovery partition, and /dev/sda2 is the Windows OS partition. 
Since partition indexes start at zero, the Windows OS partition will be hd0,1 (sda = 0, sdb = 1; 
or first disk, second partition) when we edit the Grub file. Make note of this.

sda=hd0 (sda1...15 = hd0,1...15)
sdb=hd1 (sdb1...15 = hd1,1...15) 

**** Move to Virtual Machine

[root@serverX ~]# cd /etc/grub.d/
[root@serverX grub.d]# ls
[root@serverX grub.d]# vim 40_custom 

################# Add the Following lines ##############
 6
 7    menuentry "Windowns Se7en" {
 8            set root='(hd0,9)'
 9            chainloader +1
 10        }

[root@serverX ~]# grub2-mkconfig --output=/boot/grub2/grub.cfg

Now Once you reboot, you should see the option of booting into Windows 7

Tips-1: Windows First, then Linux:
----------------------------------
Setup: To recover windows then you will use above command:

Tips-2: Linux First, then Windows:
----------------------------------
1. Use CentOS 7 DVD
2. run linux rescue mode
3. #chroot /mnt/sysimage
3. # fdisk -l
4. #grub2-install /dev/sda1
5. exit
6. reboot

Working with Linux Kernel:
--------------------------
[root@serverX ~]# uname -r
[root@serverX ~]# yum list installed kernel-*
[root@serverX ~]# yum update kernel -y  
[root@serverX ~]# yum list installed kernel-*

RHEL6 or Old Version:
---------------------
[root@serverX ~]# ls /etc/init.d/

RHEL7 or New Version:
---------------------
[root@serverX ~]# ls /lib/systemd/system/*.service

[root@serverX ~]# systemctl -t service

Start/Stop/Restart/status Services with systemctl:
-------------------------------------------------
[root@desktopX ~]# systemctl start crond.service
[root@desktopX ~]# systemctl status crond.service

[root@desktopX ~]# systemctl stop crond.service
[root@desktopX ~]# systemctl status crond.service

[root@desktopX ~]# systemctl restart crond.service
[root@desktopX ~]# systemctl reload XXXX.service

Enable / Disable services to run at boot time:
----------------------------------------------
[root@desktopX ~]# systemctl enable crond.service
[root@desktopX ~]# systemctl disable crond.service
[root@desktopX ~]# systemctl status crond.service

Working with halt/Restart/Poweroff/Hibernate:
---------------------------------------------
[root@desktopX ~]# systemctl halt
[root@desktopX ~]# systemctl reboot
[root@desktopX ~]# systemctl poweroff
[root@desktopX ~]# systemctl hibernate 
[root@desktopX ~]# systemctl suspend

Working with Runlevels:
-----------------------
[root@desktopX ~]# systemctl get-default 
graphical.target

[root@desktopX ~]# systemctl set-default multi-user.target
[root@desktopX ~]# systemctl get-default 
multi-user.target

[root@desktopX ~]# reboot

[root@desktopX ~]# systemctl get-default 
multi-user.target

[root@desktopX ~]# systemctl set-default graphical.target

[root@desktopX ~]# reboot

Recover Root Password:
---------------------
 => Reboot your system by pressing 'Ctr+Alt+Del 
 => Edit the default boot loader entry
 => Press 'e' to edit the current entry
 => Cursor navigate to the line that starts with 'linux16'.
 => Press 'End' button to move the cursor to the end of the line.
 => Append 'rd.break' to the end of the line.
 => Press 'Ctrl+x' to boot using the modified config.

switch_root:/# mount -o remount,rw /sysroot
switch_root:/# chroot /sysroot

sh-4.2# passwd    [press enter]

  : ******* (123456)
  : ******* (123456)

sh-4.2# touch /.autorelabel 
sh-4.2# exit 

switch_root:/# exit

=> Wait 2 Min

=> Login with new password

[root@desktopX ~]# passwd   ; press Enter

  : ******* (centos)
  : ******* (centos)
```
