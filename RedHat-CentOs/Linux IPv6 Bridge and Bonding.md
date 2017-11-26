```sh

        ###################################
	######  Bridge Interface ##########
	###################################

Verify Bridge Interface (serverX):
----------------------------------
[root@desktopX ~]# ifconfig

          br0: IP, MASK, GW, DNS
 enp2s0/ens33: MAC

Bridge Interface Configure:
---------------------------
[root@serverX ~]# systemctl start NetworkManage r.service 
[root@serverX ~]# systemctl enable NetworkManager.servie 

[root@serverX ~]# ping 172.25.11.254
[root@serverX ~]# rpm -qa | grep bridge-utils
[root@serverX ~]# yum install bridge-utils

[root@serverX ~]# cd /etc/sysconfig/network-scripts
[root@serverX network-scripts]# ls 
ifcfg-eth0
ifcfg-eth1

[root@serverX network-scripts]# cp ifcfg-eth0 ifcfg-br0
[root@serverX network-scripts]# ls 
ifcfg-eth0
ifcfg-eth1
ifcfg-br0

[root@serverX network-scripts]# vim ifcfg-eth0          ;physical INT
DEVICE=eth0
HWADDR=aa:bb:cc:dd:ee:ff
TYPE=Ethernet
ONBOOT=yes
BRIDGE=br0

[root@serverX network-scripts]# vim ifcfg-br0           ; Bridge Int
DEVICE=br0
TYPE=Bridge
IPADDR=172.25.11.200+X   
NETMASK=255.255.255.0
GATEWAY=172.25.11.1
DNS1=8.8.8.8
BOOTPROTO=none
ONBOOT=yes
DELAY=0

[root@serverX network-scripts]# systemctl restart network.service 
[root@serverX network-scripts]# cd
[root@serverX ~]# ifconfig 

[root@desktopX ~]# ping -I br0 172.25.11.254

        ###################################
	######   IPv6 Configure  ##########
	###################################

IPv6 Addressing:
================

Description	IPv4			IPv6
-----------	----			----
No bits		32			128
Part		4			8
Format		Dot (.)			(:)
Number		Decimal			Hexa
Class		5			N/A
Example		192.168.11.10		2001:db8:0:abcd:12c::1

Types of IPv4
-------------
 => Private IP (10.0.0.0/8, 172.16.0.0 - 172.31.255.255, 192.168.0.0-192.168.255.255)
 => Public IP (except private block)

Types of IPv6:
-------------
 => :: - all IP (similar as 0.0.0.0)
 => ::1 - loopback (Similar as 127.0.0.1)
 => fe80 - Link local address (similar as 169.254....)
 => ff00 - Multicast (Similar as 224.0.0.0)
 => fd00 - Unique local address (same as IPv4 Private)
 => 2000 - Global unicast address (same as public IP)

Configure IPv6 to eth0 Interface:
=================================
[root@serverX ~]# ip addr

[root@serverX ~]# ifconfig eth1 | grep inet6

[root@serverX ~]# systemctl restart NetworkManager 
[root@serverX ~]# systemctl enable NetworkManager

[root@serverX ~]# nmcli connection show 

[root@serverX ~]# nmcli con del 'eth1'

[root@serverX ~]# systemctl restart NetworkManager 

[root@serverX ~]# nmcli connection show 

NAME        	    UUID                                  TYPE            DEVICE 
Wired connection 1  5fb06bd0-0bb0-7ffb-45f1-d6edd65f3e03  802-3-ethernet  eth1

[root@serverX ~]# nmcli connection modify "Wired connection 1" ipv6.addresses fddb:db08:abcd::1234:X/64 ipv6.method manual

[root@serverX ~]#  ifconfig eth1 | grep inet6

[root@serverX ~]# nmcli connection up "Wired connection 1"

[root@serverX ~]#  ifconfig eth1 | grep inet6

[root@serverX ~]# ping6 fddb:db08:abcd::1234:254

Test with SSH:
-------------
[root@serverX ~]# ssh fddb:db08:abcd::1234:254

IP with Defautl Gateway:
------------------------
[root@serverX ~]# nmcli connection modify "Wired connection 1" ipv6.addresses 
                                       'fddb:fe2a:ab1e::c0a8:X/64 fddb:fe2a:ab1e::c0a8:fe'

	#######################################
	######  NIC Teaming (Bonding)   ########
	########################################

Load Balacing Algorithms:
-------------------------
=> RoundRobin
=> Bonding (Teaming)
=> LACP (etherchannel) 
=> Broadcast
=> Failover (active backup) - HSRP
=> Load Balacing
=> High Availability (HA)

=================== Optional for LAB Setup ============

[root@serverX ~]# cd /etc/sysconfig/network-scripts/

(optional) - [root@serverX network-scripts]# rm -rf ifcfg-Wire*

[root@serverX ~]# systemctl restart NetworkManager.service 

[root@serverX ~]# systemctl restart network

======================  x ===============================

[root@serverX ~]# systemctl restart NetworkManager.service 
[root@serverX ~]# systemctl enable NetworkManager.servie 

[root@serverX ~]# nmcli connection show

Note: nmcli con del 'eth1'  or 'System eth0' 

[root@serverX ~]# systemctl restart NetworkManager.service 

[root@serverX ~]# nmcli connection show

NAME                UUID                                  TYPE            DEVICE 
Wired connection 1  21899a89-65e3-478a-8385-69ce38a67fa0  802-3-ethernet  eth0   
Wired connection 2  5fb06bd0-0bb0-7ffb-45f1-d6edd65f3e03  802-3-ethernet  eth1 

[root@serverX ~]# nmcli connection add con-name team0 ifname team0 type team 
                 config '{"runner": {"name": "activebackup"}}'

[root@serverX ~]# ip addr
[root@serverX ~]# nmcli connection show 

NAME                UUID                                  TYPE            DEVICE 
Wired connection 1  21899a89-65e3-478a-8385-69ce38a67fa0  802-3-ethernet  eth0   
Wired connection 2  5fb06bd0-0bb0-7ffb-45f1-d6edd65f3e03  802-3-ethernet  eth1   
team0               3a549377-21cb-40f4-9b57-22020aec388b  team            team0

[root@serverX ~]# nmcli connection modify team0 ipv4.addresses 192.168.11.X/24

[root@serverX ~]# nmcli connection modify team0 ipv4.method  manual

[root@serverX ~]# ip link 
[root@serverX ~]# ip addr

[root@serverX ~]# nmcli con add type team-slave con-name team0-port1 ifname eth0 master team0

[root@serverX ~]# nmcli con add type team-slave con-name team0-port2 ifname eth1 master team0

[root@serverX ~]# systemctl restart network
[root@serverX ~]# ip addr

[root@serverX ~]# teamdctl team0 state

[root@serverX ~]# ping -I team0 192.168.11.254

[root@serverX ~]# ip link set eth0 down
[root@serverX ~]# teamdctl team0 state view

[root@serverX ~]# teamdctl team0 state 

Connection Verify:
------------------
[root@serverX ~]# cd /etc/sysconfig/network-scripts/
[root@serverX network-scripts]# cat ifcfg-team0

