```sh

Check VT Support
-----------------
[root@desktopX ~]# grep -i vmx /proc/cpuinfo --color

[root@desktopX ~]# cat /proc/cpuinfo 
[root@desktopX ~]# cat /proc/meminfo 
[root@desktopX ~]# free -m

Packages
========
 => virt-manager (GUI interface)
 => libvirt (daemon + API collection)
 => qemu-kvm (emulator for virtual OS)

Package Installation
--------------------
[root@desktopX ~]# yum install virt-manager* libvirt* qemu-kvm* -y

[root@desktopX ~]# systemctl restart libvirtd.service  
[root@desktopX ~]# systemctl enable libvirtd.service 

Run Virtual Machine Mananger:
-----------------------------
Application => System Tools => Virtual Machine Manager (VMM)

Download CentOS ISO:
--------------------
=> Open Mozila Firefox
=> ftp://172.25.11.254/pub

Create a ISO (Optional):
------------------------ 
[root@desktopX ~]# dd if=/dev/sr0 of=/root/Desktop/centos7.iso 

Run VM:
=======
Application => System Tools => VMM

 -> VM Name: studentX

 Install Method: iso
 --------------
 -> IOS:/root/Desktop/Ce.........iso 

 Install Method: Network (FTP/HTTP/NFS)
 -----------------------

 Path: ftp://172.25.11.254/pub

 -> OS=Linux & RHEL 7
 -> Disk: /dev/sda* (10.GB)
 -> Interface: br0
 
    Time: Asia/Dhaka
    Installation Method: Minimal
    Size: /boot (500 MB), / (5 GB), swap (512)
    Hostname: serverX.example.com 

Virtual Machine Location:
=========================
 => /var/lib/libvirt/images
 
IP configure:
============
[root@serverX ~]# ip addr

[root@serverX ~]# systemctl stop NetworkManager.service 
[root@serverX ~]# systemctl disable NetworkManager.servie 

[root@serverX ~]# cd /etc/sysconfig/network-scripts
[root@serverX network-scripts]# ls
[root@serverX network-scripts]# vi ifcfg-eth0
DEVICE=eth0
TYPE=Ethernet
HWADDR=XX:XX:XX:XX:XX:XX
IPADDR=172.25.11.200+X   
NETMASK=255.255.255.0
BOOTPROTO=none
ONBOOT=yes

[root@serverX network-scripts]# systemctl restart network.service 
[root@serverX network-scripts]# systemctl enable network.service 
[root@serverX network-scripts]# ip addr

=> yum client configure

[root@serverX network-scripts]# cd /etc/yum.repos.d
[root@serverX network-scripts]# ls
[root@serverX network-scripts]# rm -rf *
[root@localhost network-scripts]# vi client.repo

 [client]
 name=yum client
 baseurl=ftp://172.25.11.254/pub/Packages     ; yum server IP
 enabled=1
 gpgcheck=0

 :x     (SAVE & exit)

=> yum install net-tools
=> yum install vim

[root@serverX network-scripts]# ifconfig 

Hostname:
---------
[root@serverX ~]# vi /etc/hostname 
 serverX.example.com 

[root@serverX ~]# reboot
