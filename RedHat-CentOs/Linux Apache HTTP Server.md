```sh

 HTTP Server:
=============
 Pakcages:httpd, mod_ssl (https), elinks 
 daemon: httpd
 port: 80 (http), 443 (https)
 Prerequisite: DNS server configure 
 Configuration file: /etc/httpd/conf/httpd.conf (HTTP)
 		     /etc/httpd/conf.d/ssl.conf (HTTPS)
		     /etc/pki/tls/certs (ssl Certificate directory)
 default index file: /var/www/html

#################################################
############                         ############
############ HTTP Based Web Server   ############
############                         ############
#################################################

Step 01: DNS Part:
-------------------
[root@nsX ~]# hostname
[root@nsX ~]# nslookup nsX.example.com

[root@nsX ~]# nslookup www.example.com

[root@nsX ~]# cd /var/named/
[root@nsX named]# ls
[root@nsX named]# vim example.com.for
 
ns1     IN A    172.25.11.X           ;old entry

=============  Append following line ==============

www     IN CNAME ns1.example.com.      ; same server

or
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+ www     IN  A    172.25.11.251         ; different srever    +
+                                                              +
+ [root@ns1 named]# vi example.com.rev                         +
+ 251     IN  PTR    www.example.com.       ; different srever +
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

[root@nsX named]# systemctl restart named.service
[root@nsX named]# nslookup www.example.com
[root@nsX named]# dig www.example.com

Step 02: Package Install 
-------: 
[root@nsX named]# yum install httpd -y

Step 03: web hosting
---------------------
[root@nsX named]# cd /var/www/html/
[root@nsX html]# ls
[root@nsX html]# vi index.html

	<html>
	<head>
	<body bgcolor="#f25dfd">
	<h1 allign="center"> ##### welcome to example.com  ### </h1>
	</body>
	</head>
	</html>

Step 04: web server configure
-----------------------------
[root@nsX httpd]# cd /etc/httpd/conf
[root@nsX conf]# ls
httpd.conf  magic
[root@nsX conf]# vim httpd.conf 

 95 ServerName www.example.com            ; remove '#' and :80
 96 ServerName 172.25.11.200+X            ; add new IP address for server

[root@nsX named]# systemctl restart httpd.service
[root@nsX named]# systemctl enable httpd.service

[root@nsX named]# systemctl enable firewalld.service
[root@nsX named]# systemctl restart firewalld.service

[root@nsX named]# firewall-cmd --permanent --add-service=dns
[root@nsX named]# firewall-cmd --permanent --add-port=80/tcp
[root@nsX named]# firewall-cmd --reload 

 Step 05: Open Browser & Test
-----------------------------

=> Return to DesktopX
=> Change your DNS Address to DNS1=172.25.11.200+X (your DNS server IP)

[root@desktopX ~]# vim /etc/sysconfig/network-scripts/ifcfg-br0
 DNS1=172.25.11.200+X

[root@desktopX ~]# systemctl restart network.service
[root@desktopX ~]# cat /etc/resolv.conf 
[root@desktopX ~]# nslookup ns1.example.com 

 http://www.example.com or http://172.25.11.200+X

#################################################
############                         ############
############ HTTPS Based Web Server  ############
############                         ############
#################################################

Creatre Self sign Certificate:
-----------------------------
[root@ns1 ~]# cd /etc/pki/tls/certs/
[root@ns1 certs]# ls
ca-bundle.crt        localhost.crt    Makefile
ca-bundle.trust.crt  make-dummy-cert  renew-dummy-cert

[root@ns1 certs]# make serverX.key      ; generate RSA Private Key

Pass: 123456

[root@ns1 certs]# ls 
[root@ns1 certs]# cat serverX.key

[root@ns1 certs]# openssl rsa -in serverX.key -out serverX.key

[root@ns1 certs]#  make serverX.csr

 : BD
 : Dhaka
 : Dhanmondi
 : CSL
 : Training
 : ns1.example.com
 : info@csltraining.com
 : Example Inc.
 : 123456
 : 123456

[root@nsX certs]#  openssl x509 -in serverX.csr -out serverX.crt -req -signkey 
	           serverX.key -days 365

[root@nsX certs]# ls
 serverX.key serverX.csr serverX.crt

[root@ns1 certs]# yum install mod_ssl -y
[root@ns1 certs]#  cd /etc/httpd/conf.d/
[root@ns1 conf.d]# vim ssl.conf 

 59 DocumentRoot "/var/www/html"             		   ; remove '#'
 60 ServerName www.example.com:443			   ; remove '#'
100 SSLCertificateFile /etc/pki/tls/certs/serverX.crt      
107 SSLCertificateKeyFile /etc/pki/tls/certs/serverX.key   ; remove verify path

[root@ns1 conf.d]#  systemct restart httpd.service

[root@ns1 conf.d]#  firewall-cmd --permanent --add-port=443/tcp
[root@ns1 conf.d]#  firewall-cmd --reload 

 https://www.example.com or http://172.25.11.200+X

#####################################################
############                             ############
############ Private Browsing:  ############
############                             ############
#####################################################

[root@server12 ~]# mkdir /var/www/html/private -p
[root@server12 ~]# echo "hello private" >> /var/www/html/private/index.html
[root@server12 ~]# vim /etc/httpd/conf/httpd.conf 

131 <Directory "/var/www/html/private">
1 	AllowOverride none 
   	Options None 
132     Require host desktop12.example.com 172.25.11.100+X
158 </Directory>

[root@server10 ]# systemctl restart httpd
[root@server10 ]# systemctl enable httpd

Test: http://www.example.com/private from DesktopX Machine


#####################################################
############                             ############
############ Name based Virtual Hosting  ############
############                             ############
#####################################################

Step 01:  Name Based Virtual Hosting : DNS Part
-----------------------------------------------
[root@nsX ~]# vim /etc/named.rfc1912.zones 

 [plase add following forward zones as per required ]

 19 zone "example.com" IN {
 20         type master;
 21         file "example.com.for";
 22         allow-update { none; };
 23 };
 24 zone "example.net" IN {
 25         type master;
 26         file "example.net.for";
 27         allow-update { none; };
 28 };
 29 zone "example.org" IN {
 30         type master;
 31         file "example.org.for";
 32         allow-update { none; };
 33 };

[root@nsX ~]# cd /var/named/
[root@nsX named]# cp example.com.for example.org.for
[root@nsX named]# cp example.com.for example.net.for
[root@nsX named]# chgrp named example.net.for
[root@nsX named]# chgrp named example.org.for

[root@nsX named]# vim example.org.for       

nsX    IN  A  172.25.11.200+X      ; old line

========== Add following Entry ============

www     IN CNAME nsX.example.org.
nsX.example.org. IN A 172.25.11.200+X

[root@nsX named]# vim example.net.for     

nsX    IN  A  172.25.11.200+X       ; old line

========== Add following Entry ============

www     IN CNAME nsX.example.net.
nsX.example.net. IN A 172.25.11.200+X

[root@nsX named]# systemctl restart named.service

[root@nsX named]# nslookup www.example.net
[root@nsX named]# nslookup www.example.org
[root@nsX named]# nslookup www.example.com 

 Step 02: (Hosting Part)
 -----------------------
[root@nsX named]# cd /var/www/html
[root@nsX html ]# mkdir example.net example.org
[root@nsX html ]# ls
[root@nsX html ]# cd example.net
[root@nsX example.net]# vi index.html

	<html>
	<head>
	<body bgcolor="#fed2fd">
	<h1 allign="center"> ##### welcome to our example.net ### </h1>
	</body>
	</head>
	</html>
[root@nsX example.net]# cd /var/www/html/example.org
[root@nsX example.org]# vi index.html

	<html>
	<head>
	<body bgcolor="#d2f8cd">
	<h1 allign="center"> ##### welcome to our example.org ### </h1>
	</body>
	</head>
	</html>

step 03: Web Server configuration Part:
--------------------------------------
[root@nsX example.org]# cd /etc/httpd/conf
[root@nsX conf]# ls
[root@nsX httpd]# vim httpd.conf

 95 ServerName www.example.com             ;server name
 96 ServerName 172.25.11.200+X              ;server IP address 

 120 # DocumentRoot "/var/www/html"          ; add '#'

356 NameVirtualHost 172.25.11.200+X
 
358 <VirtualHost 172.25.11.200+X >
359      DocumentRoot /var/www/html
360      ServerName www.example.com
361  </VirtualHost>

363 <VirtualHost 172.25.11.200+X >
364      DocumentRoot /var/www/html/example.net
365      ServerName www.example.net
366  </VirtualHost>

368 <VirtualHost 172.25.11.200+X >
369      DocumentRoot /var/www/html/example.org
370      ServerName www.example.org
371  </VirtualHost>

[root@nsX httpd]# systemctl restart httpd.service 
[root@nsX httpd]# systemctl status httpd.service 

step 04: Testing 
----------------
 => Open Firefox browser with 3 Tab
 => Type: http://www.example.com
 => Type: http://www.example.org
 => Type: http://www.example.net 

