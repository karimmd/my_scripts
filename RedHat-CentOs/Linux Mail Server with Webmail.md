```sh

 Mail Server:
 ============
  => MUA (Mail user Agent): outlook, thunderbird, eudora, webmail, apps(gmail)
  => MTA (Mail Transfer Agent): MS exchange,qmail,postfix,sendmail 
  => MDA (Mail Delivery Agent): POP3 Server (Dovecot)
	
Reference Table:
----------------
Prerequisite - DNS Ready, Static IP for Mail Server

Packages:
	=> postfix(smtp), 
	=> dovecot(pop3&IMAP), 
	=> squirrelmail (webmail), 
	=> httpd, 
	=> telnet (testing)
	=> epel (Extra package for Enterprise Linux)

Daemon - postfix (SMTP), dovecot (POP3 & IMAP), httpd
Ports  -  
  	=> SMTP 25 : client to Server, server to server
	=> PoP3 110: server to client
	=> IMAP 143: server to client (Interactively used)

Configuration files:
	=> /var/named/example.com.for  (DNS)
	=> /etc/postfix/main.cf
	=> /etc/dovecot/dovecot.conf 
	=> /etc/dovecot/conf.d/10-mail.conf 
	=> /etc/dovecot/conf.d/10-auth.conf 
	=> /etc/dovecot/conf.d/10-master.conf
	=> /usr/share/squirrelmail/config/conf.pl  - squirrelmail 
	=> /etc/httpd/conf/httpd.conf   - (web mail) 

DNS Part:
----------
[root@nsX ~]# hostname
[root@nsX ~]# nslookup nsX.example.com

[root@nsX ~]# cat /etc/resolv.conf

[root@nsX ~]# cd /var/named
[root@nsX named]# ls
[root@nsX named]# vim example.com.for 
      
8	IN NS   ns1.example.com.         ; no change
9       IN A   172.25.11.200+X           ; no change

11       IN MX 10 mail.example.com.       ; new entry
12       IN MX 20 mail2.example.com.      ; (optional for 2nd Mail server)

14  ns1     IN A    172.25.11.200+X     ; no change 
15  mail    IN CNAME ns1.example.com.   ; new entry

16  mail2   IN A    172.25.11.Y         ;(optional for 2nd Mail server)

[root@ns1 named]# systemctl restart named.service

Note: CNAME - Canonical Name ( If we want to configure multiple server like DNS, FTP, MAIL, Web in same machine then, we can use CNAME insted of "A" record.

[root@ns1 named]# nslookup mail.example.com
Server:		172.25.11.200+X
Address:	172.25.11.200+X#53

mail.example.com	canonical name = ns1.example.com.
Name:	ns1.example.com
Address: 172.25.11.200+X

Step 01:
--------
[root@nsx ~]# yum install postfix* -y

Step 02:
--------
[root@nsx ~]# cd /etc/postfix
[root@ns1 postfix]# ls
[root@nsx postfix]# vim main.cf

 75 myhostname = mail.example.com
 83 mydomain = example.com
 99 myorigin = $mydomain
 113 inet_interfaces = all
 116 #inet_interfaces = localhost 
 164 #mydestination = $myhostname, localhost.$mydomain, localhost
 165 mydestination = $myhostname, localhost.$mydomain, localhost, $mydomain
 250  mynetworks_style = subnet
 264 mynetworks = 172.25.11.0/24, 127.0.0.0/8 
 419 home_mailbox = Maildir/
 572  smtpd_banner = $myhostname ESMTP $mail_name

[root@ns1 postfix]# systemctl restart postfix.service
[root@ns1 postfix]# systemctl enable postfix.service

Allow port through firewall-cmd:
-------------------------------
[root@nsx postfix]# systemctl restart firewalld
[root@nsx postfix]# systemctl enable firewalld
[root@nsx postfix]# firewall-cmd --permanent --add-service=smtp 
success
[root@nsx postfix]# firewall-cmd --reload
success

[root@nsx postfix]# yum install telnet -y

Step 03: SMTP Testing
=====================
[root@nsx postfix]# telnet mail.example.com 25
Trying 172.25.11.200+X...
Connected to mail.example.com.
Escape character is '^]'.
220 mail.example.com ESMTP Postfix
quit
221 2.0.0 Bye
Connection closed by foreign host.

Step 04: dovecot install
========================:
[root@nsx ~]# yum install dovecot* -y

Step 05: dovecot configure 
========================:

[root@nsx ~]# vim /etc/dovecot/dovecot.conf 
 24 protocols = imap pop3 lmtp
 30 listen = *
 42 login_greeting = Welcome to Example Inc. Mail 

[root@nsx ~]#  vim /etc/dovecot/conf.d/10-mail.conf 
 24    mail_location = maildir:~/Maildir

[root@nsx ~]#  vim /etc/dovecot/conf.d/10-auth.conf 
 10  disable_plaintext_auth = no
 100 auth_mechanisms = plain login

[root@nsx ~]#  vim /etc/dovecot/conf.d/10-master.conf

 91     user = postfix
 92     group = postfix

[root@nsx ~]# systemctl enable dovecot.service
[root@nsx ~]# systemctl restart dovecot.service

Allow port through firewall-cmd:
-------------------------------
[root@nsx ~]# firewall-cmd --permanent --add-port 110/tcp
success
[root@nsx ~]# firewall-cmd --reload
success

Step 06: POP Testing
=====================
[root@nsx ~]# telnet mail.example.com 110
Trying 172.25.11.200+X...
Connected to mail.example.com.
Escape character is '^]'.
+OK Welcome to Example Inc. Mail 
quit
+OK Logging out
Connection closed by foreign host.

Mail User Create:
-------------------
[root@nsx ~]# useradd -s /sbin/nologin sadia.afroz
[root@nsx ~]# useradd -s /sbin/nologin rose
[root@nsx ~]# useradd -s /sbin/nologin jack

[root@nsx ~]# passwd jack
[root@nsx ~]# passwd rose
[root@nsx ~]# passwd sadia.afroz

Web Mail Configure with Squirrelmail: 
=====================================

Step 01: EPEL Install 
---------------------
[root@serverX ~]# yum install epel-release 

or
[root@nsx ~]# yum install wget -y
[root@nsx ~]# wget http://dl.fedoraproject.org/pub/epel/7/x86_64/e/epel-release-7-5.noarch.rpm
[root@nsx ~]# ls
[root@nsx ~]# rpm -ivh epel-release-7-5.noarch.rpm

[root@nsx ~]# cd /etc/yum.repos.d
[root@nsx yum.repos.d]# ls   

Step 02: Install Squirrelmail
------------------------------
[root@nsx ~]# yum install squirrelmail -y

Step 03: Configure Squirrelmail
-----------------------------
[root@ns1 ~]# cd /usr/share/squirrelmail/config/
[root@ns1 config]# ls
[root@ns1 config]# ./conf.pl 
  
 Command >> Press 1  and Enter (Orgnization) 
 Command >> Press 1  and Enter (Squirrelmail)
 [SquirrelMail]: Example Inc.  ;press Enter

 Command >> 4    (Organizationn Ttile)
 [SquirrelMail $version]: Webmail

 Command >> Press 8     ;and Press Enter 

 [SquirrelMail]: Example Inc.

 Command >> S
 Command >> R
 Command >> Press 2
 Command >> Press 1 (Domain)
 [localhost]: example.com

 Command >> Press 3
Your choice [1/2] [1]: 2 (SMTP)

Command >> S
Command >> R

Command >> Press 4 (General Options)
Command >> 7 ( Hide SM attributions)
Hide SM attributions (y/n) [n]: y

Command >> S

Command >> Q  

Step 04: Apache HTTP Install 
----------------------------
[root@nsx ~]# yum install httpd -y

Step 05: Add following lines at the end of configuration files ####
-------------------------------------------------------------------
[root@nsx ~]# vim /etc/httpd/conf/httpd.conf 

 [add the following lines end of the file]

Alias /webmail /usr/share/squirrelmail
<Directory /usr/share/squirrelmail>
Options Indexes FollowSymLinks
RewriteEngine On
AllowOverride All
DirectoryIndex index.php
Order allow,deny
Allow from all
</Directory>

[root@nsx ~]# systemctl restart httpd.service
[root@nsx ~]# systemctl enable httpd.service

Allow port through firewall-cmd:
-------------------------------
[root@nsx ~]# firewall-cmd --permanent --add-service=http 
success
[root@nsx ~]# firewall-cmd --reload
success

Step 06: Test
-------------
 -> open browser
 -> http://mail.example.com/webmail   or -> http://172.25.11.200+X/webmail 

===============================
