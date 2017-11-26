```

Linux Firewall with Firewalld:
------------------------------
 Types of Linux Firewall:
------------------------
	=> Application based (squid/PAM/tcpwrappers)
	=> kernel based: firewalld

 firewalld which also called linux firewall/netfilter integrated with linux kernel.

 Filtering:
 ---------
 => layer3: IP/Subnet/icmp
 => layer4: tcp/udp/port/tls/ssl or 21,22,25,53,80,443,161,110,123,
 => Layer7: dns,ftp,http,smtp,pop3,squid,imap,snmp,nfs,tftp,ntp,ssh,https

 NAT & Portforwarding:
---------------------
 => Masquerading   (PAT/NAT Overload)
 => Portforwarding (port map)

Working with Firewalld:
-----------------------
=> By directly editing configuration files in '/etc/firewalld/'.
=> By using the graphical firewall-config tool
=> By using firewall-cmd from the command line

Firealld enabled and check:
---------------------------
[root@serverX ~]# systemctl enable firewalld
[root@serverX ~]# systemctl restart firewalld
[root@serverX ~]# systemctl status firewalld

=================== Optional ===============

Mask the iptables to avoid conflict:
------------------------------------
[root@serverX ~]# systemctl status iptables
[root@serverX ~]# systemctl mask iptables
[root@serverX ~]# systemctl mask ip6tables

===========================================

[root@serverX ~]# firewall-cmd --state

Check the Firewalld in GUI Mode:
--------------------------------
[root@desktopX ~]# systemctl enable firewalld
[root@desktopX ~]# systemctl restart firewalld
[root@desktopX ~]# systemctl status firewalld

=================== Optional ===============

Mask the iptables to avoid conflict:
------------------------------------
[root@desktopX ~]# systemctl mask iptables
[root@desktopX ~]# systemctl mask ip6tables

===========================================

Applications > Sundry > Firewall

or

[root@serverX ~]# firewall-config

Firewalld Zones:
---------------
 -> public (default)
 -> internal
 -> external
 -> trusted
 -> home
 -> DMZ
 -> block
 -> work
 -> drop

Check the firewall configure in CMD Mode:
-----------------------------------------
[root@serverX ~]# firewall-cmd --state

[root@serverX ~]# firewall-cmd --get-default-zone
   public (output)

[root@serverX ~]# firewall-cmd --permanent --zone=public --list-all
  interfaces: 
  sources: 
  services: dhcpv6-client ssh 
  ports: 
  masquerade: no
  forward-ports: 
  icmp-blocks: 
  rich rules: 

To get the current configuration of the public zone, type:
----------------------------------------------------------
[root@serverX ~]# firewall-cmd --zone=public --list-all

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
[root@serverX ~]# firewall-cmd --permanent --zone=public --add-port 443/tcp
success
[root@serverX ~]# firewall-cmd --reload
success

Allow service through firewall-cmd:
----------------------------------
[root@serverX ~]# firewall-cmd --permanent --zone=public --add-service=https
success
[root@serverX ~]# firewall-cmd --reload
success

Remove port through firewall-cmd: (Optional)
--------------------------------
[root@serverX ~]# firewall-cmd --permanent --zone=public --remove-port 443/tcp
success
[root@serverX ~]# firewall-cmd --reload
success

Remove service through firewall-cmd: (Optional)
----------------------------------- 
[root@serverX ~]# firewall-cmd --permanent --zone=public --remove-service=https
success

[root@serverX ~]# firewall-cmd --reload
success

[root@serverX ~]# firewall-cmd --zone=public --list-all

****** Move to Graphical

 => Open Firefox
 => http://172.25.11.200+X
 => https://172.25.11.200+X

Configure Firewalld in GUI Mode:
--------------------------------
[root@desktop0 ~]# firewall-config

Applications > Sundry > Firewall

Configuration: Permanent
Zone: public
Ports => add => port & protocol (443) => ok
Options => Reload firewalld

Testing:
--------
=> http://172.25.11.X or http://serverX.example.com (should fail)
=> https://172.25.11.X or http://serverX.example.com (should succeed)

Filtering & Port Forwarding:
===========================

01. SSH Reject Configure:
-------------------------
[root@desktopX~]# Firewall-config (GUI)
        => Rich Rule: 
        => Rich Rule => Add => Family [IPv4]=> Element [Port]: 22
        => Action: Reject
        => Source: X.X.X.X 
        => OK
        => Reload Firewall

02. Local Port Forward (Basic Rule):
------------------------------------
[root@desktopX~]# Firewall-config (GUI)
   =><= Permanent => Public
                  => Port Forwarding
                  => Add 
		  => Source => Protocol: tcp, Port: 5080 (src)
		  => Local Forwarding: Yes 
                  => Port: 22
		  => Reload Firewall
Note: Remove ssh

[root@serverX ~]# ssh 172.25.11.100+X (refused)
[root@serverX ~]# ssh -p 5080 172.25.11.100+X 

03. Remote Port Forward (Basic Rule):
-------------------------------------
[root@desktopX~]# Firewall-config (GUI)
   =><= Permanent => Public
                  => Port Forwarding
                  => Add 
		  => Source => Protocol: tcp, Port: 5080 (src)
		  => Local Forwarding: [No] 
		  => Forward to Another Port - Yes
                  => IP Address:  172.25.11.100+X  (Neibourg)
		  => Port: 22
		  => Reload Firewall

Note: SSH Must Enabled on Destination

[root@serverX ~]# ssh 172.25.11.200+X (refused)
[root@serverX ~]# ssh -p 5080 172.25.11.200+X  
 
04. Port Forward (Rich Rule):
-----------------------------
   =><= Permanent => Public
                  => Rich Rule
                  => Add => Family (IPv4) => [Element] => Forward Port
		  => Source => Protocol: tcp, Port: 5080 (src)
		  => Local Forwarding: 22
		  => Source: Source IP - 172.25.11.100+X  (Neibourg)
	          => Reload Firewall

[root@server200 ~]# ssh 172.25.11.200+X (refused)
[root@server100 ~]# ssh -p 5080 172.25.11.200+X (allowed)

Or:
--
[root@server100 ~]# firewall-cmd --add-rich-rule 'rule family="ipv4" source address="192.168.X.0/24" 
service name="ssh" -j reject' --permanent

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

[root@serverX ~]# reboot

[root@serverX ~]# cat /proc/sys/net/ipv4/ip_forward
 1

Enable NAT/MASQUERADE:
---------------------
[root@serverX ~]# systemctl restart firewalld.service
[root@serverX ~]# systemctl enable firewalld.service
[root@serverX ~]# systemctl status firewalld.service

[root@serverX ~]# firewall-cmd --permanent --direct --passthrough ipv4 -t nat 
-I POSTROUTING -o eth0 -j MASQUERADE -s 192.168.X.0/24

[root@serverX ~]# firewall-cmd --permanent --direct --passthrough ipv4 -I FORWARD -i eth1 -j ACCEPT

[root@serverX ~]# firewall-cmd --reload


 Client
 ------
  XP> ping 192.168.X.1 
  XP> ping 172.25.11.1 
  XP> ping 8.8.8.8
