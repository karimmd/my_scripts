```

#############  Deploy Outbound NAT Gateway  ##############

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

Linux Gateway Machine (Private Network):
---------------------------------------
[root@serverX network-scripts]# ip addr
[root@serverX network-scripts]# vim ifcfg-eth1
DEVICE="eth1"
HWADDR="00:01:2E:38:54:C3" <=============== Veryfied (enXX/enXX)
IPADDR=192.168.X.1
NETMASK=255.255.255.0
BOOTPROTO=none
ONBOOT=yes

[root@serverX network-scripts]# systemctl restart network.service 

[root@serverX network-scripts]# ip addr

########### Client Setting (Windows/Linux) ##############

IP: 192.168.X.2
MASK: 255.255.255.0
GW: 192.168.X.1
DNS1: 8.8.8.8
DNS2: 4.2.2.2

>ping 192.168.X.1

Enable IP Forwarding between Interfaces (Routing):
-------------------------------------------------

[root@serverX ~]# cat /proc/sys/net/ipv4/ip_forward
 0

[root@serverX ~]# vim /etc/sysctl.conf
 :set nu

 5   net.ipv4.ip_forward = 1

[root@serverX ~]# systemctl restart network.service
[root@serverX ~]# cat /proc/sys/net/ipv4/ip_forward
 1

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

 59 http_port 3128 transparent

 62  cache_dir ufs /var/spool/squid 100 16 256    ; remove '#'
 63  cache_mem 256 MB

 67  visible_hostname proxy.example.com            ; add new line

Note:
=====
100 - MB
16 - Folder
256 - Subfolder

Step03: Restart Squid Service and enable during system boot:
------------------------------------------------------------
[root@serverX squid]# systemctl restart squid.service
[root@serverX squid]# systemctl enable squid.service

Step04: Checking Squid running or not:
-------------------------------------
[root@serverX squid]# squid -z
[root@serverX squid]# netstat -tlnp | grep 3128

Step05: Allow squid port in IPtables:
--------------------------------------
[root@serverX ~]# systemctl stop firewalld
[root@serverX ~]# systemctl disable firewalld
[root@serverX ~]# systemctl mask firewalld
[root@serverX ~]# yum install iptables-services
[root@serverX ~]# systemctl enable iptables
[root@serverX ~]# systemctl unmask iptables
[root@serverX ~]# systemctl restart iptables

Enable Masquareding:
----------------------------
[root@serverX ~]# iptables -F
[root@serverX ~]# iptables -t nat -nL                                                                         
[root@serverX ~]# iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
[root@serverX ~]# iptables -A FORWARD -i eth1 -j ACCEPT

Enable Port Redirect:
---------------------
[root@serverX ~]# iptables -t nat -A PREROUTING -i eth1 -p tcp --dport 80 -j REDIRECT --to-port 3128 
[root@serverX ~]# service iptables save
[root@serverX ~]# systemctl restart iptables
[root@serverX ~]# iptables -t nat -nL

########### Client Setting (Windows/Linux) ##############

IP: 192.168.X.2
MASK: 255.255.255.0
GW: 192.168.X.1
DNS1: 8.8.8.8
DNS2: 4.2.2.2

>ping www.google.com

Visit site: 
-----------
 1) www.apple.com
 2) www.bdjobs.com
 3) www.cricinfo.com

Step06: Monitoring Live access:
-------------------------------
[root@serverX ~]#  tail -f /var/log/squid/access.log 
