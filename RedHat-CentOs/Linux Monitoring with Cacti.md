```sh

What is Cacti?
--------------
Cacti tool is an open source web based network monitoring and system monitoring
graphing solution for IT business. Cacti enables a user to poll service at regular
intervals to create graps on resulting data using RRDtool. Generally, it is used 
to graph time-series data of metrics such as network bandwidth utilization, CPU load,
running process, disk space etc.

Cacti Required Packages:
------------------------
 => Apache   : A Web server to display network graphs created by PHP and RRDTool.
 => MySQL:   : A Database server to store cacti information.
 => PHP      : A script module to create graphs using RRDTool.
 => PHP-SNMP : A PHP extension for SNMP to access data.
 => NET-SNMP : A SNMP (Simple Network Management Protocol) is used to manage network.
 => RRDTool  : A database tool to manage and retrieve time series 

Step 01: Install Required Packages:
-----------------------------------
[root@serverX ~]# yum install httpd httpd-devel mariadb-server php-mysql php-pear 
   php-common php-gd php-devel php php-mbstring php-cli -y

[root@serverX ~]#  yum install php-snmp net-snmp-utils net-snmp-libs rrdtool -y

Step 02: Service Restart and Onboot on:
---------------------------------------
[root@serverX ~]# systemctl restart httpd.service
[root@serverX ~]# systemctl enable httpd.service
[root@serverX ~]# systemctl restart snmpd.service
[root@serverX ~]# systemctl enable snmpd.service
[root@serverX ~]# systemctl restart mariadb.service
[root@serverX ~]# systemctl enable mariadb.service

Step 03: Enable EPEL Repo:
--------------------------
[root@serverX ~]# cd /opt/
[root@serverX ]# yum install epel-release -y
[root@serverX ]# cd /etc/yum.repos.d/
[root@serverX yum.repos.d]# ls
 CentOS-Base.repo
 CentOS-Debuginfo.repo
 CentOS-Sources.repo
 CentOS-Vault.repo
 epel.repo
 epel-testing.repo

Step 04: Install Cacti through EPEL:
------------------------------------
[root@serverX ~]# yum install cacti -y
[root@serverX ~]# rpm -qa | grep cacti
 cacti-0.8.8b-7.el7.noarch

Step 05: Set MySQL Password:
----------------------------
[root@serverX ~]# mysqladmin -u root password centos    ;here password is 'centos'

Step 06: Create MySQL Cacti Database:
-------------------------------------
[root@serverX ~]#  mysql -u root -p

 Enter password: ****** (centos)

 ########################################################################################
 #                                                                                      #
 #  MariaDB [(none)]> create database cacti;                                            #
 #         Query OK, 1 row affected (0.00 sec)                                          #
 #                                                                                      #
 #  MariaDB [(none)]> GRANT ALL ON cacti.* TO cacti@localhost IDENTIFIED BY 'centos';  
 #
 #         Query OK, 0 rows affected (0.00 sec)                                         #
 #                                                                                      #
 #  MariaDB [(none)]> FLUSH privileges;                                                 #
 #         Query OK, 0 rows affected (0.00 sec)                                         #
 #                                                                                      #
 #  MariaDB [(none)]> quit;                                                             #
 #         Bye                                                                          #
 #                                                                                      #
 ########################################################################################

Step 07: Install Cacti Tables to MySQL:
---------------------------------------
[root@serverX ~]# rpm -ql cacti | grep cacti.sql
 /usr/share/doc/cacti-0.8.8b/cacti.sql

 Now we�ve of the location of Cacti.sql file, type the following command to install tables, 
 here you need to type the Cacti user password.

[root@serverX ~]# mysql -u root -p cacti < /usr/share/doc/cacti-0.8.8b/cacti.sql

Step 08: Configure MySQL settings for Cacti:
--------------------------------------------
[root@serverX ~]# vim /etc/cacti/db.php

/* make sure these values refect your actual database/host/user/password */
 $database_type = "mysql";
 $database_default = "cacti";
 $database_hostname = "localhost";
 $database_username = "cacti";            ;change name
 $database_password = "centos";           ;change password 
 $database_port = "3306";
 $database_ssl = false;

Step 09: Configuring Firewall for Cacti:
----------------------------------------
[root@serverX ~]# firewall-cmd --permanent --zone=public --add-service=http
[root@serverX ~]# firewall-cmd --reload

or

[root@serverX ~]# systemctl stop firewalld
[root@serverX ~]# systemctl disable firewalld

Step 10: Configuring Apache Server for Cacti:
--------------------------------------------- 
[root@serverX ~]# vim /etc/httpd/conf.d/cacti.conf

 17                 Require all granted
 23                 Allow from 172.25.11.0/24

[root@serverX ~]# systemctl restart httpd.service

Step 11: Setting Cron for Cacti:
--------------------------------
[root@serverX ~]# vim /etc/cron.d/cacti

 */5 * * * *     cacti   /usr/bin/php /usr/share/cacti/poller.php > /dev/null 2>&1

[root@server254 ~]# systemctl restart crond.service
[root@server254 ~]# systemctl enable crond.service

Step 12: Running Cacti Installer Setup:
---------------------------------------
 => Open your browser and browse http://X.X.X.X/cacti

          username: admin
	  password: admin 



Step 13: Create a Bandwidth Graph:
----------------------------------
 => Click Device 
 => Add
 => Description: Linux-Server
 => Host Name: 172.25.11.X
 => Host Template: Local Linux Machine 
 => SNMP Version: 2
 => Community: public
 => Click Create

=> Create Graph Template for Linux-Server host:
   -------------------------------------------
 => Click Device
 => Click Linux-Server 
 => Add Associate Data Queries
 => Select "SNMP - Interface Statistics"
 => Click "Add"
 => Select "UNIX - Mounted Partition"
 => Click "Add"
 => Select "SNMP - Processor Information"
 => Click "SAVE"

Configure SNMP:
---------------
 [root@server254 ~]#  vim /etc/snmp/snmpd.conf 
     55 view    systemview    included   .1.3.6.1.2.1.1         ;[old config]
     55 view    systemview    included   .1.3.6.1.2.1  		;[new config]

 [root@server254 ~]#  systemctl restart snmpd

=> Create New Graph: 
   -----------------
 => Click New Graph for this host
 => Select: Host (Linux-Server) 
 => Selct Graph Template
 => Select Data Query: (Mounted partition: /, /boot, swap), Interface: eth0 
 => Slect 64 bit counter
 => Create 

====================================================================================================
