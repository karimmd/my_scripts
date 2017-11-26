```sh

Linux Scheduling using Crontab
---------------------------------
 Daemon: crond
 Package: crontabs

[root@serverX ~]# rpm -qa | grep crontabs 

[root@serverX ~]# yum install crontabs -y

Crontab Format:
==============
 	*  *  *  *  *  <cmd>
	1  2  3  4  5
	
	1 = Minutes 	(0-59)
	2 = Hour 	      (0-23)
        3 = day of month(1-31)
        4 = Months 	(1-12)  
 	5 = Day of Week (0-6) here 0 or 7 is sunday
        <cmd> = command to be execute 

List of current Cronjob
-----------------------
[root@serverX ~]# crontab -l   ; list of current job for root

Crontab Remove:
--------------
[root@serverX ~]# crontab -r
[root@serverX ~]# crontab -l 

Crontab Edit
--------------
[root@serverX ~]# crontab -e

Example 01:  Schedule a job every night 11.59 PM to shutdown the system: 
------------------------------------------------------------------------
[root@serverX ~]# crontab ?e
59  23   *   *   *   /usr/sbin/poweroff 

[root@serverX ~]# crontab ?l

Set the date 23.57 for job testing: 
-----------------------------------

[root@serverX ~]# date 
[root@serverX ~]# date +%T%p -s "23:57:00"
[root@serverX ~]# date 

or

[root@serverX ~]# date MMDDHHMMYY
[root@serverX ~]# date 

[root@serverX ~]# systemctl restart crond.service
[root@serverX ~]# systemctl enable crond.service

[root@serverX ~]# watch date 

Example 02: Take etc backup in .tar format under /backup directory on every Thrusday at midnight:
-------------------------------------------------------------------------------------------------
[root@serverX ~]# date +\%Y-\%m-\%d

[root@serverX ~]# mkdir /backup
[root@serverX ~]# crontab ?e

 59 23 * * 4  tar -cvf /backup/etc_$(date +\%Y-\%m-\%d).tar  /etc

[root@serverX ~]# date
[root@serverX ~]# cal              ; verify recent Thrusday
[root@serverX ~]# date MMDDHHMMYY 
[root@serverX ~]# date

[root@serverX ~]# systemctl restart crond.service

[root@serverX ~]# watch date 

[root@serverX ~]# cd /backup
[root@serverX ~]# ls

Example 03: Schedule job to run every five minute. Who are currently logged in server:
-------------------------------------------------------------------------------------
[root@serverX ~]# crontab ?e 
*/5  *  *  *  *  who >> /backup/login_$(date +\%Y-\%m-\%d-\%T)

*/5 * * * *  ping -c 4 172.25.11.254 >> /backup/ping

[root@serverX ~]# systemctl restart crond.service
[root@serverX ~]# cd /backup
[root@serverX ~]# ls

Example 04:  Schedule a job to run every six hours in a day:
------------------------------------------------------------
[root@serverX ~]# crontab ?e
* 0,6,12,18  *  *  *  cat /proc/meminfo >> /backup/meminfo

* 0,6,12,18  *  *  *  cat /proc/meminfo | mail -s "Memory Status" admin@example.com

Example 05: Run a script at 01:00 am each weekday [Monday ? Friday]: 
------------------------------------------------------------------
00  01  *  *  1-5   /backup/db_backup.sh 

Example 06:  Schedule job to run every minute:
----------------------------------------------

 */1  *  *  *  *   /backup/system_status.sh

Example 07: Run a cronjob december 31 every year:
-------------------------------------------------
 * * 31 12 * /backup/backup.sh

Remove all cron jobs: 
----------------------------
[root@serverX ~]# crontab ?r
[root@serverX ~]# crontab ?l

User based cron job:
--------------------
[root@serverX ~]# crontab ?e -u student

===================== ===================
