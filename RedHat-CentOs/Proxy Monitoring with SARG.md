```sh

[root@serverX ~]# yum install epel-release 

[root@serverX ~]# cd /etc/yum.repos.d/
[root@serverX yum.repos.d]# ls
CentOS-Base.repo       CentOS-Sources.repo  epel.repo
CentOS-Debuginfo.repo  CentOS-Vault.repo    epel-testing.repo

[root@serverX yum.repos.d]#  cd /opt
[root@serverX opt]# wget http://sourceforge.net/projects/sarg/files/sarg/sarg-2.3.7/sarg-2.3.7.tar.gz

[root@serverX opt]# ls
[root@serverX opt]# tar -zxvf sarg-2.3.7.tar.gz
[root@serverX opt]# ls
sarg-2.3.7  sarg-2.3.7.tar.gz
[root@serverX opt]#  cd sarg-2.3.7
[root@serverX sarg-2.3.7]# ls
[root@serverX sarg-2.3.7]# ./configure
[root@serverX sarg-2.3.7]# make
[root@serverX sarg-2.3.7]# make install
[root@serverX sarg-2.3.7]# vim /usr/local/etc/sarg.conf
  7  access_log /var/log/squid/access.log                ;very path
  25 title "CSL Squid access report"
  45 font_size 12px
  50 header_font_size 12px
  55 title_font_size 35px
  120 output_dir /var/www/html/squid-reports
  216 date_format e
  257 overwrite_report yes

[root@opt sarg-2.3.7]# sarg -x
[root@opt sarg-2.3.7]# service httpd restart

[root@serverX squid]# firewall-cmd --permanent --add-port=80/tcp
[root@serverX squid]# firewall-cmd --reload

[root@serverX squid]# setenforece 0

Move DesktopX:
-------------
 Browse: http://x.x.x.x/squid-reports


