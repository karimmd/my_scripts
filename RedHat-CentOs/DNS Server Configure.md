```

Application: Name Resulation

Name => IP (www.btcl.gov.bd => 180.211.129.60)
IP => Name (180.211.129.60=> www.btcl.gov.bd)

Resolver:
---------
 => Global (DNS) - Automatically
 => Local (hosts) - Manually 

Types of DNS Server:
--------------------
 => Recursive DNS Servers
 => Authoritative DNS Servers
 => Caching DNS Server

Daemon: named
Packages: bind,bind-utils
Port: 53
Protocol: TCP and UdP
Configuration file:
	=> /etc/sysconfig/network-scripts/ifcfg-eth0
 	=> /etc/hosts
 	=> /etc/hostname
 	=> /etc/named.conf
 	=> /etc/named.rfc1912.zones 
 	=> /var/named/named.localhost (Forward Zone)
 	=> /var/named/named.looback (Reverse Zone)

Step 01: Set Static Host Name and Reboot:
----------------------------------------
[root@serverX ~]# hostname
[root@serverX ~]# vim /etc/hostname
nsX.example.com

[root@serverX ~]# logout
[root@nsX ~]# hostname 

Step 02: Set Static IP Address and DNS:
--------------------------------------
[root@nsX ~]# ifconfig

or

[root@nsX ~]# ip addr

[root@nsX ~]# cd /etc/sysconfig/network-scripts/
[root@nsX network-scripts]# ls
[root@nsX network-scripts]# vim ifcfg-eth0        ; your Interface name
 
 DEVICE=eth0
 HWADDR=AA:BB:CC:DD:EE:FF
 TYPE=Ethernet
 BOOTPROTO=none
 IPADDR=172.25.11.200+X         
 NETMASK=255.255.255.0
 GATEWAY=172.25.11.1
 ONBOOT=yes
 DNS1=172.25.11.200+X         

[root@nsX network-scripts]# systemctl stop NetworkManager.service
[root@nsX network-scripts]# systemctl disable NetworkManager.service

[root@nsX network-scripts]# systemctl restart network.service 

[root@nsX network-scripts]# ip addr
[root@nsX network-scripts]# ping 172.25.11.1
[root@nsX network-scripts]# ping 8.8.8.8

[root@nsX network-scripts]# cat /etc/resolv.conf   ;verify
 
nameserver 172.25.11.200+X   
search example.com 

Step 02: Local resolver entry:
------------------------------
[root@serverX ~]# vim /etc/hosts

1   127.0.0.0 	   localhost.localdomain	localhost.localdomain
2   ::1
==================== New Entry ========================

3   172.25.11.200+X       nsX.example.com              nsX   
4   172.25.11.100+x       desktopX.example.com        desktopX  
5   172.25.11.1           gw.example.com        	gw

***save and exit

[root@serverX ~]# ping nsX
[root@serverX ~]# ping gw
[root@serverX ~]# ping desktopX

Step 03: Install Required RPM:
------------------------------
[root@nsX ~]# yum install bind* -y

Step 04: Allow DNS Server IP and Network:
----------------------------------------
[root@nsX ~]# vim /etc/named.conf

11         listen-on port 53 { 127.0.0.1; 172.25.11.200+X; };
12  #      listen-on-v6 port 53 { ::1; };
17         allow-query     { localhost; 172.25.11.0/24; };

Step 06: Set Forward and Reverse Zones:
---------------------------------------
[root@nsX ~]# vim /etc/named.rfc1912.zones 
:set nu

 19 zone "example.com" IN {
 20         type master;
 21         file "example.com.for";
 22         allow-update { none; };
 23 };

 31 zone "11.25.172.in-addr.arpa" IN {
 32         type master;
 33         file "example.com.rev";
 34         allow-update { none; };
 35 };

Step 07: Create Forward and Reverse Zone Files:
-----------------------------------------------
[root@nsX ~]# cd /var/named/
[root@nsX named]# ls 
[root@nsX named]# cp named.localhost example.com.for
[root@nsX named]# cp named.loopback example.com.rev
[root@nsX named]# ls -l 

Step 08: Set Ownership to Forward and Reverse Zone Files:
---------------------------------------------------------
[root@nsX named]# ll example.com.*
-rw-r-----. 1 root root 152 Mar 21 13:59 example.com.for
-rw-r-----. 1 root root 168 Mar 21 13:59 example.com.rev

[root@nsX named]# chgrp named example.com.*

[root@nsX named]# ll example.com.*
-rw-r-----. 1 root named 152 Mar 21 13:59 example.com.for
-rw-r-----. 1 root named 168 Mar 21 13:59 example.com.rev

Step 09: Edit Forward Zone File:
--------------------------------
[root@nsX named]# vim example.com.for

$TTL 1D
@       IN SOA  nsX.example.com. root.example.com. (
                                        0       ; serial
                                        1D      ; refresh
                                        1H      ; retry
                                        1W      ; expire
                                        3H )    ; minimum
        IN NS nsX.example.com.
        IN A 172.25.11.200+X

nsX     IN A 172.25.11.200+X

www     IN A 172.25.11.202 		;(optional)
ftp     IN A 172.25.11.203 		;(optional) 
blog	IN CNAME nsX.example.com. 	;(optional)
webmail	IN CNAME nsX.example.com. 	;(optional)

Note:
-----
  SOA  - Start of Authority
   IN  - Internet 
   NS  - Name Server (DNS Server)
    A  - Host Record (IP Address)
  AAAA - Host Record (IPv6 Address) 
 root  - email admin (root@example.com)
  PTR  - Pointer (Reverse Lookup)
 CNAME - Canonical Name
    MX - Mail Exchanger Record
 
Step 10: Edit Reverse Zone File:
--------------------------------
[root@nsX named]# vim example.com.rev

$TTL 1D
@       IN SOA nsX.example.com. root.example.com. (
                                        0       ; serial
                                        1D      ; refresh
                                        1H      ; retry
                                        1W      ; expire
                                        3H )    ; minimum
        IN NS nsX.example.com.

200+X      IN PTR nsX.example.com.

Step 11: Service restart and configured active at boot time:
------------------------------------------------------------
[root@nsX named]# systemctl restart named.service
[root@nsX named]# systemctl enable named.service

Check Status:
-------------
[root@nsX named]# systemctl status named.service

Allow DNS Through Firewall:
---------------------------
[root@nsX named]# systemctl enable firewalld.service
[root@nsX named]# systemctl restart firewalld.service

[root@nsX named]# firewall-cmd --permanent --add-service=dns
[root@nsX named]# firewall-cmd --reload

Step 12: Checking DNS 
---------------------
[root@nsX named]# nslookup nsX.example.com
Server:		172.25.11.200+X
Address:	172.25.11.X#53

Name:	nsX.example.com
Address: 172.25.11.200+X

[root@nsX named]# dig -x 172.25.11.200+X      ; here -X is option 

 status: NOERROR 

[root@nsX named]# dig nsX.exampleX.com

 status: NOERROR

[root@nsX named]# ping www.google.com
