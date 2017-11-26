```sh

Linux Advnced File Permission (ACL)
-----------------------------------
X= VM Machine No
Y= Batch no

[root@serverX ~]# mkdir /linuxY/lesson07 -p
[root@serverX ~]# cd /linuxY/lesson07/
[root@serverX lesson07]# ls 
[root@serverX lesson07]# touch tutorial profile
[root@serverX lesson07]# ll

-rw-r--r--. 1 root root 0 Jun 28 17:00 tutorial
-rw-r--r--. 1 root root 0 Jun 28 17:00 profile
 
 [root@serverX lesson07]# useradd jack
 [root@serverX lesson07]# useradd rose
 [root@serverX lesson07]# useradd tomy

ACL Test:
----------
[root@serverX lesson07]# getfacl tutorial
 # owner: root
 # group: root
 user::rw-
 group::r--
 other::r--

User ACL:
---------
[root@serverX lesson07]# setfacl -m u:rose:rw,jack:rw  profile
[root@serverX lesson07]# ll
[root@serverX lesson07]# getfacl profile

[root@serverX lesson07]# setfacl -m u:rose:r--,u:jack:rw,u:tomy:-w-  tutorial
[root@serverX lesson07]# getfacl tutorial
[root@serverX lesson07]# getfacl profile 

[root@serverX lesson07]# ls -l  tutorial 
-rw-rw-r--+ 1 root root 0 Jun 28 17:00 tutorial

[root@serverX lesson07]# su jack
[jack41@serverX lesson07]$ cat tutorial
[jack41@serverX lesson07]$ echo hello > tutorial
[jack41@serverX lesson07]$ cat tutorial
[jack41@serverX lesson07]$ exit

[root@serverX lesson07]# su rose
[rose41@serverX lesson07]$ cat tutorial
[rose41@serverX lesson07]$ echo hi > tutorial 
[rose41@serverX lesson07]$ exit

 **** Permissin denied

Group acl:
----------
[root@serverX lesson07]# groupadd staff
[root@serverX lesson07]# setfacl -m g:staff:rw-  tutorial 
[root@serverX lesson07]# getfacl tutorial

Directory Permission:
---------------------
[root@serverX lesson07]# mkdir acldir
[root@serverX lesson07]# touch acldir/file1
[root@serverX lesson07]# touch acldir/file2
[root@serverX lesson07]# setfacl -R -m u:rose:rwx acldir    ;-R (recursively)
[root@serverX lesson07]# getfacl acldir

ACL Remove (user):
-------------------
[root@serverX lesson07]# setfacl -x u:rose: profile
[root@serverX lesson07]# getfacl profile

ACL Remove (Gruop):
------------------
[root@serverX lesson07]# setfacl -x g:staff: tutorial
[root@serverX lesson07]# getfacl tutorial 

Remove ACL from File:
---------------------
[root@serverX lesson07]# setfacl -b tutorial 
```
