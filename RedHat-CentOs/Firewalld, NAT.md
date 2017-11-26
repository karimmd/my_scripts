```sh


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

[root@serverX ~]# vim /etc/sysctl.conf
 :set nu

 5   net.ipv4.ip_forward = 1

[root@serverX ~]# systemctl restart network.service
[root@serverX ~]# cat /proc/sys/net/ipv4/ip_forward
 1

Enable NAT/MASQUERADE:
---------------------
[root@serverX ~]# systemctl restart firewalld.service
[root@serverX ~]# systemctl enable firewalld.service
[root@serverX ~]# systemctl status firewalld.service

[root@serverX ~]# firewall-cmd --permanent --direct --passthrough ipv4 
       -t nat -I POSTROUTING -o eth0 -j MASQUERADE -s 192.168.X.0/24
[root@serverX ~]# firewall-cmd --permanent --direct --passthrough ipv4 
	-I FORWARD -i eth1 -j ACCEPT

[root@serverX ~]# firewall-cmd --reload

 Client
 ------
  XP> ping 192.168.X.1 
  XP> ping 172.25.11.1 
  XP> ping 8.8.8.8

Trasparent Proxy:
----------------
# see the active zones
firewall-cmd --get-active-zones

# see the settings of the internal zone
firewall-cmd --zone=internal --list-all

# see the settings direct rules
firewall-cmd --direct --get-all-rules

##############################  Thank You  ############################

=> By directly editing configuration files in '/etc/firewalld/'.
=> By using the graphical firewall-config tool
=> By using firewall-cmd from the command line

Firealld enabled and check:
---------------------------
[root@serverX ~]# systemctl enable firewalld
[root@serverX ~]# systemctl restart firewalld
[root@serverX ~]# systemctl status firewalld

Mask the iptables to avoid conflict:
------------------------------------
[root@serverX ~]# systemctl mask iptables
[root@serverX ~]# systemctl mask ip6tables

Check the Firewalld in GUI Mode:
--------------------------------
Applications > Sundry > Firewall

or

[root@serverX ~]# firewall-config

Check the firewall configure in CMD Mode:
-----------------------------------------

[root@serverX ~]# firewall-cmd --permanent --zone=public --list-all

[root@serverX ~]# firewall-cmd --get-default-zone
   public (output)

Set the zone, if no zone defined:
---------------------------------
[root@serverX ~]# firewall-cmd --set-default-zone public

Firewalld Testing with HTTPs service:
-------------------------------------
[root@serverX ~]# yum install httpd mod_ssl -y

[root@serverX ~]# echo 'welcome to https' > /var/www/html/index.html

[root@serverX ~]# systemctl restart httpd.service
[root@serverX ~]# systemctl enable httpd.service

Allow port through firewall-cmd:
-------------------------------
[root@desktop0 ~]# firewall-cmd --permanent --zone=public --add-port 443/tcp
success
[root@desktop0 ~]# firewall-cmd --reload
success

Remove port through firewall-cmd:
--------------------------------
[root@desktop0 ~]# firewall-cmd --permanent --zone=public --remove-port 443/tcp
success
[root@desktop0 ~]# firewall-cmd --reload
success

Configure Firewalld in GUI Mode:
--------------------------------
[root@desktop0 ~]# firewalld-config

Applications > Sundry > Firewall

Configuration: Permanent
Zone: public
Ports => add => port & protocol (443) => ok
Options => Reload firewalld

Testing:
--------
=> http://172.25.11.X or http://serverX.example.com (should fail)
=> https://172.25.11.X or http://serverX.example.com (should succeed)

03. SSH Configure:
==================
[root@desktop10 ~]# Firewall-config (GUI)
        => Rich Rule: 
        => Rich Rule => Add => Family [IPv4]=> Element [Port]: 22
        => Action: Reject
        => Source: X.X.X.X
        => OK
        => Reload Firewall

Port Forward (Rich Rule):
-------------------------
3) =><= Permanent => Public
                  => Port Forwarding
                  => Add => Family (IPv4) => [Element] => Forward Port
		  => Source => Protocol: tcp, Port: 5080 (src)
		  => Local Forwarding: Yes 
                  => Port: 22
		  => Source: Source IP - 172.25.X.10 (only Allowed)
	          => Reload Firewall

