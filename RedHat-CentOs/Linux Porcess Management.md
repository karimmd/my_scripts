 ```sh
 
 Linux Process Management:
 ========================
 => Login DesktopX
   : root
   : centos

 [root@desktopX ~]# ps
 [root@desktopX ~]# ps -au        ; pid, process, mem, cpu, tty, cmd
 [root@desktopX ~]# ps -au | less 

 [root@desktopX ~]# ps -u root  ; list of process for specifc user
 [root@desktopX ~]# ps -ef         ; pid, ppid, time, cmd
 [root@desktopX ~]# ps -ef | grep http

   => list of prcocess
   => PID
   => NICE Value
   => CPU%
   => Memory%
   => Process time
   => Process name
   => User's Process information 

Process ID: (1-65,535)

RHEL/CentOS- 7 
      => PID 1 (systemd) 

RHEL/CentOS- 6 
      => PID 1 (init ) 

 [root@desktopX ~]# pidof systemd
  1

 Graphical Process Tools:
 ------------------------
 Application => System Tools => System Monitor

Process Dealing:
---------------
 ps - list the processes running on the system
 kill - send a signal to one or more processes (usually to "kill" a process)
 jobs - an alternate way of listing your own processes
 bg - put a process in the background
 fg - put a process in the forground
 nice - new process with specific nice value
 renice - reset process priority

[root@desktopX ~]# firefox

=> Run Firefox to test (ctrl+z, Ctrl+c)

[root@desktopX ~]# sleep 10

[root@desktopX ~]# sleep 500 & 
[root@desktopX ~]# firefox &
[root@desktopX ~]# top (ctrl+Z)
[root@desktopX ~]# ping 172.25.11.1 (ctrl+c)

[root@desktopX ~]# ping 172.25.11.1 (ctrl+Z)

[root@desktopX ~]# jobs 
[root@desktopX ~]# fg %1 (sleep)
[root@desktopX ~]# (Ctrl+c)
[root@desktopX ~]# jobs 

 Process Dealing:
 =================
	=> End  : "Ctrl + c"
	   -> Kill
	=> stop : "Ctrl + z"
	   -> process continue: 

  (ctrl+Z) - send to bra
  (ctrl+C) - Terminate 

 List of Stoped process:
 ========================
 [root@desktopX ~]# jobs  [shows all stoped process]
 [root@desktopX ~]# ps    [shows stoped process with PID]

 Process Findout:
 ================
[root@desktopX ~]# firefox &
[root@desktopX ~]# pidof firefox
 2869

Process Kill
=================
[root@desktopX Desktop]# kill 2869        ; Normal kill
[root@desktopX Desktop]# kill -9 2869     ; Forcely killed
				  	  ; "-9" killing frequecy (highest)
	
Nice Value Range:
----------------
(Low) 19.................. 0 ................ -20 (High)

Nice Value:
----------
[root@desktopX ~]# ps axo pid,comm,nice --sort=-nice
[root@desktopX ~]# firefox &
[root@desktopX ~]# ps axo comm,nice | grep firefox
 firefox   0
New Process Priority:
---------------------
[root@desktopX ~]# nice -n 15 firefox &
[root@desktopX ~]# ps axo comm,nice | grep firefox
firefox    15
Existing Process Priority:
-------------------------
[root@desktopX ~]# pidof firefox
[root@desktopX ~]# renice -n -7 [pid]
[root@desktopX ~]# ps axo comm,nice | grep firefox

```
