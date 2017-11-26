```sh

 IPV4 (LAN/MAN/WAN)
 ----------------------
 Class A: 0.0.0.0  - 126.255.255.255
 Class B: 128.0.0.0 - 191.255.255.255
 Class C: 192.0.0.0 - 223.255.255.255

 Private:
 --------
  A: 10.0.0.0 - 10.255.255.255
  B: 172.16.0.0 - 172.31.255.255
  C: 192.168.0.0 - 192.168.255.255

  Linux Network Management
 ----------------------------
  Windows NIC1: Local Area Netowrk 
  Windows NIC2: Local Area Network 2

[root@desktopX ~]# ip link 
[root@desktopX ~]# ip addr show         ; CMD or GUI 
[root@desktopX ~]# ifconfig             ; (active)
[root@desktopX ~]# ifconfig -a          ; all

[root@desktopX ~]# ifconfig  br0 ; sepecific LAN (br0, eth0, ens33, enp2s0)
 
  Linux (RHEL/CentOS-7)
 ---------------------
  Physical NIC : enp2s0 or ens33 (start with 'en')
  Virtual Machine NIC: eth0
  Virtual IP: enp2s0:1 or ens33:1 or eth0:1
  loopback: lo
  Bridge  : br0
  Wireless: wl
  VMware NIC: eno16777736 - ethernet card information 

Check Physical Connectivity:
----------------------------
[root@desktopX ~]# ip link 
[root@desktopX ~]# mii-tool enp2s0    ;(physical Machine)

enp2s0 : negotiated 1000baseT-FD flow-control, link ok
enp2s0 : no link (not connected)

Host Name Configure (server)
---------------------------
[root@localhost ~]# hostname 

[root@localhost ~]# vim /etc/hostname
serverX.example.com 

[root@localhost ~]# logout   ;(ctrl+d)
[root@localhost ~]# reboot   ;(if required)

or

[root@localhost ~]# hostname
[root@localhost ~]# hostnamectl status
[root@localhost ~]# hostnamectl --static set-hostname serverX.example.com
[root@localhost ~]# reboot

[root@serverX ~]# ip link
[root@serverX ~]# ip addr 

  ether 8C:89:A5:E4:F3:64 => MAC
  inet addr:172.25.11.X => IP Address
  Bcast:172.25.11.255
  Mask:255.255.255.0
  inet6 addr: IPv6 Link Local address 

[root@serverX ~]# ifconfig 

N.B: (For Command Mode)

     [root@serverX ~]# yum install net-tools -y  (#ifconfig)
     [root@serverX ~]# yum install setuptool -y   (GUI interface)

 IP Configure 
 --------------------------
  => Tempoary  (IP remove after system reboot)
  => Parmanet 

Temporary IP Address Configure:
-------------------------------
[root@serverX ~]# ifconfig 
[root@serverX ~]# ifconfig eth1  172.25.11.200+X 
[root@serverX ~]# ifconfig eth1  172.25.11.200+X  netmask 255.255.255.0
[root@serverX ~]# ifconfig 

[root@serverX ~]# ifconfig 

Gateway Testing
--------------------------
[root@serverX ~]# ping 172.25.11.1 
64 bytes from 172.25.11.1 : icmp_seq=1 ttl=64 time=0.451 ms
64 bytes from 172.25.11.1 : icmp_seq=2 ttl=64 time=0.317 ms
C^

[root@serverX ~]# ping -c 4 172.25.11.1 

Check Default Gateway:
---------------------
[root@serverX ~]# route -n
[root@serverX ~]# route add default gw 172.25.11.254
[root@serverX ~]# echo nameserver 8.8.8.8 > /etc/resolv.conf 
[root@serverX ~]# echo nameserver 4.2.2.2 >> /etc/resolv.conf 
[root@serverX ~]# cat /etc/resolv.conf 
[root@serverX ~]# ping www.google.com

Delete: 
-------
[root@serverX ~]# route del default gw 172.25.11.254 
[root@serverX ~]# route -n

[root@serverX ~]# reboot

 IP Client Configure
 -------------------
  => Static
  => dhcp : autmatically ip configure

[root@serverX ~]# systemctl stop NetworkManager.service 
[root@serverX ~]# systemctl disable NetworkManager.service 
[root@serverX ~]# systemctl status NetworkManager.service 

Static (parmanent) IP configure:
--------------------------------
[root@serverX ~]# ifconfig eth0           ; notedown eth0 ether(MAC) Address 

[root@serverX ~]# cd /etc/sysconfig/network-scripts/
[root@serverX network-scripts]# ls
[root@serverX network-scripts]# vim ifcfg-eth0

	DEVICE=eth0                    ; no change
	TYPE=Ethernet                 ; no change
        HWADDR=AA:BB:CC:DD:EE:FF      ; no change
	BOOTPROTO=none               ; none/static=static, dhcp for dynamic 
	IPADDR=X.X.X.X    (172.25.11.200+X)  ;X is your IP address
	NETMASK=Y.Y.Y.Y   (255.255.255.0)
	GATEWAY=X.X.X.G   (172.25.11.1)
	DNS1=A.A.A.A      (4.2.2.2)
	DNS2=B.B.B.B	  (8.8.8.8)
	ONBOOT=yes                   ; must yes 

[root@serverX network-scripts]# systemctl restart network.service
[root@serverX network-scripts]# systemctl enable network.service

[root@serverX network-scrip]# ifconfig 

[root@serverX network-scrip]# ifup eth0

[root@serverX network-scrip]# ifconfig 

[root@serverX ~]# ping 172.25.11.254 or ping 172.25.11.1

Enable and Disable:
-------------------
[root@desktopX ~]# ifdown eth0

[root@desktopX ~]# ifconfig

[root@desktopX ~]# ifup eth0 

[root@desktopX ~]# ifconfig

Working with NetworkManager:
---------------------------
[root@serverX ~]# systemctl restart NetworkManager 
[root@serverX ~]# systemctl enable NetworkManager

[root@serverX ~]# nmcli connection show 

[root@serverX ~]# nmcli con del 'eth1'
[root@serverX ~]# systemctl restart NetworkManager 

[root@serverX ~]# nmcli connection show 
NAME        	    UUID                                     TYPE        DEVICE 
Wired connection 1  5fb06bd0-0bb0-7ffb-45f1-d6edd65f3e03  802-3-ethernet        eth1

[root@localhost ~]# nmcli connection mod 'Wired connection 1' ipv4.addresses 
                   192.168.11.200+X/24 
[root@localhost ~]# nmcli con mod 'Wired connection 1' ipv4.gateway 192.168.2.1

[root@localhost ~]# nmcli connection mod 'Wired connection 1'  ipv4.method manual
[root@localhost ~]# nmcli connection up "Wired connection 1"
[root@localhost ~]# ip addr

===========================================
