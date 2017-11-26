```sh


 Proxy Server
==============
 => Caching 
 => Monitoring
 => Filtering & Access Control 
 => BW control
 => Authentication
 => Gateway 
 => Log
 
Proxy Types:
=========
 => normal proxy (user can by pass)
 => transparent proxy (user cannot bypass)
 => reverse proxy 

packages:
-------------
 => squid 
 => daemon: squid
 => configuration file: /etc/squid/squid.conf
 => port: 3128 (Default)

Disable NetworkManager Service:
-------------------------------
[root@serverX ~]# systemctl stop NetworkManager.service
[root@serverX ~]# systemctl disable NetworkManager.service
[root@serverX ~]# systemctl status NetworkManager.service

Linux Gateway Machine (Public Network):
--------------------------------------
[root@serverX ~]# ip addr

 **** verify MAC

[root@serverX ~]# cd /etc/sysconfig/network-scripts
[root@serverX network-scripts]# ls 
[root@serverX network-scripts]# vim ifcfg-eth0

DEVICE="eth0"
HWADDR="00:01:2E:38:54:C2"  <=============== Veryfied (eth0)
IPADDR=172.25.11.200+X
NETMASK=255.255.255.0
GATEWAY=172.25.11.1
DNS1=8.8.8.8
DNS2=4.2.2.2
BOOTPROTO=none
ONBOOT=yes

[root@serverX network-scripts]# systemctl restart network
[root@serverX network-scripts]# ip addr
[root@serverX network-scripts]# ping 8.8.8.8
[root@serverX network-scripts]# ping www.google.com 

Step 01: Package Installation
-----------------------------
[root@serverX ~]# rpm -qa | grep squid
[root@serverX ~]# yum install squid* -y

[root@serverX ~]# cd /etc/squid/
[root@serverX squid]# ls

Step 02: Basic Configure:
------------------------
[root@serverX squid]# vim squid.conf

 :set nu

  8 #acl localnet src 10.0.0.0/8    # RFC1918 possible internal network
  9 #acl localnet src 172.16.0.0/12 # RFC1918 possible internal network
 10 #acl localnet src 192.168.0.0/16        # RFC1918 possible internal network
 11 #acl localnet src fc00::/7       # RFC 4193 local private network range
 12 #acl localnet src fe80::/10      # RFC 4291 link-local (directly plugged) mac    hines

 13  acl mylan src 192.168.X.0/24

 52 # http_access allow localnet       ; add '#'
 54   http_access allow mylan          ; add new line (allow local network)

 62  cache_dir ufs /var/spool/squid 100 16 256    ; remove '#'

 67  visible_hostname proxy.example.com            ; add new line

Note:
=====
100 - MB
16 - Folder
256 - Subfolder

Step03: Service Restart:
-----------------------
[root@serverX squid]# systemctl restart squid.service
[root@serverX squid]# systemctl enable squid.service

Step 04: Enable Firewall service and allow squid servie
-------------------------------------------------------

[root@serverX squid]# systemctl enable firewalld.service
[root@serverX squid]# systemctl restart firewalld.service

[root@serverX ~]# firewall-cmd --permanent --add-port=3128/tcp
[root@serverX ~]# firewall-cmd --permanent --add-service=squid
[root@serverX ~]# firewall-cmd --reload

Step04: Chekcing:
-----------------
[root@serverX squid]# squid -z
[root@serverX squid]# netstat -tlnp | grep 3128

Step05: Proxy Setting: (DesktopX)
----------------------------------
# ======================= Proxy Setting (If Required) ===============
# => DesktopX)
# => Firefox => Edit > Preference => Advanced => Network => Settings
# => Manual Proxy Configuration
# => HTTP Proxy: 172.25.11.200+X, Port: 3128
# => Check the box [*] for 'Use the proxy for all protocols'
# => OK 
# ===================================================================

Visit site: 
-----------
 1) www.apple.com
 2) www.bdjobs.com
 3) www.cricinfo.com

Step06: Monitoring Live access:
-------------------------------
[root@serverX squid]#  tail -f /var/log/squid/access.log 

Step06: Site Block:
-------------------
[root@serverX ~]# vim /etc/squid/badsite.txt

www.bdnews24.com
www.bdjobs.com
www.porn.com

[root@serverX ~]# vim /etc/squid/squid.conf 

29 acl badsite dstdomain "/etc/squid/badsite.txt"
35 http_access deny badsite

[root@serverX squid]# systemctl reload squid.service

======== Test =========

Step 07: Keyword Block:
----------------------
[root@serverX ~]# vim /etc/squid/keywords.txt

movie
bdnews
sex

[root@serverX ~]# vim /etc/squid/squid.conf 

29 acl keywords url_regex -i "/etc/squid/keywords.txt"
35 http_access deny keywords

[root@serverX squid]# systemctl reload squid.service

Step 08: IP Block:
------------------
[root@serverX ~]# vim /etc/squid/badip.txt

172.25.11.100
172.25.11.150
172.25.11.200

[root@serverX ~]# vim /etc/squid/squid.conf 

29 acl badip src "/etc/squid/badip.txt"
35 http_access deny badip

[root@serverX squid]# systemctl reload squid.service

Step 09: Block HTTPs Site: 
-------------------------
[root@serverX ~]# vim /etc/squid/https.txt

Note: ******

www.facebook.com
www.youtube.com 
www.twitter.com

[root@serverX ~]# vim /etc/squid/squid.conf 

29 acl https_site dstdomain "/etc/squid/https.txt "
35 http_access deny CONNECT https_site

[root@serverX squid]# systemctl reload squid.service

Step 10: Allow Exceptional
--------------------------
[root@serverX ~]# vim /etc/squid/allowip.txt

172.25.11.251
172.25.11.252
172.25.11.253

[root@serverX squid]# systemctl reload squid.service

*** Note: Youtube allowed in www.youtube.com 

[root@serverX ~]# vim /etc/squid/squid.conf 

28 acl allowip src "/etc/squid/allowip.txt" 

35 http_access deny badsite !allowip 
35 http_access deny CONNECT https_site !allowip 
35 http_access deny keywords !allowip 

[root@serverX squid]# systemctl reload squid.service

