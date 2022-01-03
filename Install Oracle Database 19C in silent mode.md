**Install Oracle Database 19C in silent mode on OEL7**

This article presents how to install Oracle 19C on Oracle Enterprise Linux 7 (OEL7) in silent mode.

Read following article how to install Oracle Enterprise Linux 7: [Install Oracle Linux 7 (OEL7)]() (for comfort set 8G memory for your virtual machine before proceeding with Oracle software installation).

Software

Software for 19C is available on OTN or edelivery

Database software

LINUX.X64\_193000\_db\_home.zip

OS configuration and preparation

OS configuration is executed as root. To login as root just execute following command in terminal.

su - root

The “/etc/hosts” file must contain a fully qualified name for the server.

<IP-address>  <fully-qualified-machine-name>  <machine-name>

For example.

192.168.122.1 oel7 oel7.dbaora.com

Set hostname

hostnamectl set-hostname oel7.dbaora.com --static

It’s recoomended to update OS with latest packages

yum update

Extra configuration steps:

- add new OS groups
- add new OS user
- install required OS packages
- set specific kernel parameters
- disable transparent hugepages and defrag

Above steps can be done automatic or manually

**Automatic**

Execute following command

yum install -y oracle-database-preinstall-19c

Details about steps executed by above statement can be found in file

/var/log/oracle-database-preinstall-19c/backup/<DATE>/orakernel.log

**Manual**

Manual installation can give you more control on installation

Add groups

#basic groups for database management

groupadd -g 54321 oinstall

groupadd -g 54322 dba

groupadd -g 54323 oper

#extra dedicated groups can be ignored for simple installations

groupadd -g 54324 backupdba

groupadd -g 54325 dgdba

groupadd -g 54326 kmdba

groupadd -g 54327 asmdba

groupadd -g 54328 asmoper

groupadd -g 54329 asmadmin

groupadd -g 54330 racdba

Add user Oracle for database software

useradd -u 54321 -g oinstall \

-G dba,oper,backupdba,dgdba,kmdba,racdba oracle

Change password for user Oracle

passwd oracle

Install required packages

#basic packages to install
yum install -y bc 
yum install -y binutils 
yum install -y compat-libcap1 
yum install -y compat-libstdc++-33 
yum install -y elfutils-libelf 
yum install -y elfutils-libelf-devel 
yum install -y fontconfig-devel 
yum install -y glibc 
yum install -y glibc-devel 
yum install -y ksh 
yum install -y libaio 
yum install -y libaio-devel 
yum install -y libdtrace-ctf-devel 
yum install -y libXrender 
yum install -y libXrender-devel 
yum install -y libX11 
yum install -y libXau 
yum install -y libXi 
yum install -y libXtst 
yum install -y libgcc 
yum install -y librdmacm-devel 
yum install -y libstdc++ 
yum install -y libstdc++-devel 
yum install -y libxcb 
yum install -y make 
yum install -y smartmontools 
yum install -y sysstat

#following 4 not available in oel7
#yum install -y dtrace-modules 
#yum install -y dtrace-modules-headers 
#yum install -y dtrace-modules-provider-headers 
#yum install -y dtrace-utils 

#(for Oracle RAC and Oracle Clusterware)
yum install -y net-tools 

#(for Oracle ACFS)
yum install -y nfs-utils 

#(for Oracle ACFS Remote)
yum install -y python 
yum install -y python-configshell
yum install -y python-rtslib
yum install -y python-six
yum install -y targetcli

Add kernel parameters to /etc/sysctl.conf

\# kernel parameters for 19C installation

fs.file-max = 6815744

kernel.sem = 250 32000 100 128

kernel.shmmni = 4096

kernel.shmall = 1073741824

kernel.shmmax = 4398046511104

net.core.rmem\_default = 262144

net.core.rmem\_max = 4194304

net.core.wmem\_default = 262144

net.core.wmem\_max = 1048576

fs.aio-max-nr = 1048576
net.ipv4.conf.all.rp\_filter = 2
net.ipv4.conf.default.rp\_filter = 2
net.ipv4.ip\_local\_port\_range = 9000 65500

Apply kernel parameters

/sbin/sysctl -p

Add following lines to set shell limits for user oracle in file /etc/security/limits.conf

\# shell limits for users oracle 19C

oracle   soft   nofile   1024

oracle   hard   nofile   65536

oracle   soft   nproc    16384

oracle   hard   nproc    16384

oracle   soft   stack    10240

oracle   hard   stack    32768

oracle   soft   memlock  134217728

oracle   hard   memlock  134217728

Disabling Transparent Hugepages and defrag

This step is recommended by Oracle to avoid later performance problems – Doc ID 1557478.1. It can be done by adding **transparent\_hugepage=never** to /etc/default/grub

[root@oel7 ~]# cat /etc/default/grub
GRUB\_TIMEOUT=5
GRUB\_DISTRIBUTOR="$(sed 's, release .\*$,,g' /etc/system-release)"
GRUB\_DEFAULT=saved
GRUB\_DISABLE\_SUBMENU=true
GRUB\_TERMINAL\_OUTPUT="console"
GRUB\_CMDLINE\_LINUX="crashkernel=auto rd.lvm.lv=ol/root rd.lvm.lv=ol/swap rhgb quiet numa=off **transparent\_hugepage=never**"
GRUB\_DISABLE\_RECOVERY="true"

After applying and rebooting host can be checked with following command

[root@oel7 ~]# cat /sys/kernel/mm/transparent\_hugepage/enabled
**always madvise [never]**

Next steps

Create directory structure for binaries as user root

- ORACLE\_BASE – /ora01/app/oracle
- ORACLE\_HOME – /ora01/app/oracle/product/19.3.0.0/db\_1

mkdir -p /ora01/app/oracle/product/19.3.0.0/db\_1

chown oracle:oinstall -R /ora01

Disable firewall

systemctl stop firewalld

systemctl disable firewalld

Add following lines in /home/oracle/.bash\_profile for user oracle

\# Oracle Settings

export TMP=/tmp

export ORACLE\_HOSTNAME=oel7.dbaora.com

export ORACLE\_UNQNAME=ORA19C

export ORACLE\_BASE=/ora01/app/oracle

export ORACLE\_HOME=$ORACLE\_BASE/product/19.3.0.0/db\_1

export ORACLE\_SID=ORA19C

PATH=/usr/sbin:$PATH:$ORACLE\_HOME/bin

export LD\_LIBRARY\_PATH=$ORACLE\_HOME/lib:/lib:/usr/lib;

export CLASSPATH=$ORACLE\_HOME/jlib:$ORACLE\_HOME/rdbms/jlib;

alias cdob='cd $ORACLE\_BASE'

alias cdoh='cd $ORACLE\_HOME'

alias tns='cd $ORACLE\_HOME/network/admin'

alias envo='env | grep ORACLE'

umask 022

if [ $USER = "oracle" ]; then

`    `if [ $SHELL = "/bin/ksh" ]; then

`       `ulimit -u 16384 

`       `ulimit -n 65536

`    `else

`       `ulimit -u 16384 -n 65536

`    `fi

fi

envo

Install database software

Connect as user oracle

[root@oel7 ~]# su - oracle

Let’s start with database software installation as oracle user. Copy zip to ORACLE\_HOME directory and then uznip it. It’s ready binaries !

[oracle@oel7 ~]$ 

cp LINUX.X64\_193000\_db\_home.zip /ora01/app/oracle/product/19.3.0.0/db\_1


cd /ora01/app/oracle/product/19.3.0.0/db\_1

unzip LINUX.X64\_193000\_db\_home.zip

after unzip you should see following

[oracle@oel7 db\_1]$ pwd
/ora01/app/oracle/product/19.3.0.0/db\_1
[oracle@oel7 db\_1]$ ls
addnode     dbs          instantclient                 network  owm          root.sh.old.1  ucp
apex        deinstall    inventory                     nls      perl         runInstaller   usm
assistants  demo         javavm                        odbc     plsql        schagent.conf  utl
bin         diagnostics  jdbc                          olap     precomp      sdk            wwg
clone       dmu          jdk                           OPatch   QOpatch      slax           xdk
crs         drdaas       jlib                          opmn     R            sqldeveloper
css         dv           ldap                          oracore  racg         sqlj
ctx         env.ora      lib                           ord      rdbms        sqlpatch
cv          has          LINUX.X64\_193000\_db\_home.zip  ords     relnotes     sqlplus
data        hs           md                            oss      root.sh      srvm
dbjava      install      mgw                           oui      root.sh.old  suptools

check environment settings

--I defined 4 aliases in .bash\_profile of user oracle to make 

--administration easier :)

[oracle@oel7 ~]$ **alias envo tns cdoh cdob**

alias envo='env | grep ORACLE'

alias tns='cd $ORACLE\_HOME/network/admin'

alias cdoh='cd $ORACLE\_HOME'

alias cdob='cd $ORACLE\_BASE'

--run alias command envo to display environment settings

[oracle@oel7 ~]$ envo
ORACLE\_UNQNAME=ORA19C
ORACLE\_SID=ORA19C
ORACLE\_BASE=/ora01/app/oracle
ORACLE\_HOSTNAME=oel7.dbaora.com
ORACLE\_HOME=/ora01/app/oracle/product/19.3.0.0/db\_1

--run alias command cdob and cdoh 

--to check ORACLE\_BASE, ORACLE\_HOME 

[oracle@oel7 ~]$ **cdob**

[oracle@oel7 oracle]$ pwd

/ora01/app/oracle

[oracle@oel7 ~]$ **cdoh**

[oracle@oel7 db\_1]$ pwd

/ora01/app/oracle/product/19.3.0.0/db\_1

Response files

Once Oracle 19C binaries are unzipped. In following directories you can find response files that stores parameters necessary to install Oracle components:

|**directory**|**response file**| |
| :- | :- | :- |
|$ORACLE\_HOME/install/response|db\_install.rsp| |
|$ORACLE\_HOME/assistants/dbca|dbca.rsp| |
|$ORACLE\_HOME/assistants/netca|netca.rsp| |
- db\_install.rsp – used to install oracle binaries, install/upgrade a database in silent mode
- dbca.rsp – used to install/configure/delete a database in silent mode
- netca.rsp – used to configure simple network for oracle database in silent mode

[oracle@oel7 response]$ cd $ORACLE\_HOME/install/response

[oracle@oel7 response]$ pwd

/ora01/app/oracle/product/19.3.0.0/db\_1/install/response

[oracle@oel7 response]$ ls \*.rsp

**db\_install.rsp**

[oracle@oel7 dbca]$ cd $ORACLE\_HOME/assistants/dbca

[oracle@oel7 dbca]$ pwd

/ora01/app/oracle/product/19.3.0.0/db\_1/assistants/dbca

[oracle@oel7 dbca]$ ls \*.rsp

**dbca.rsp**

[oracle@oel7 dbca]$ cd $ORACLE\_HOME/assistants/netca

[oracle@oel7 netca]$ pwd

/ora01/app/oracle/product/19.3.0.0/db\_1/assistants/netca

[oracle@oel7 netca]$ ls \*.rsp

**netca.rsp**

Install Oracle binaries

It’s the best to preserve original response file db\_install.rsp before editing it

[oracle@oel7 response]$ cp db\_install.rsp db\_install.rsp.bck

Edit file db\_install.rsp to set parameters required to install binaries. This is just example and in next releases parameters can be different. Each of presented parameter is very well described in db\_install.rsp. I just give here brief explanations.

\--------------------------------------------

-- force to install only database software

\--------------------------------------------

oracle.install.option=INSTALL\_DB\_SWONLY

\--------------------------------------------

-- set unix group for oracle inventory

\--------------------------------------------

UNIX\_GROUP\_NAME=oinstall

\--------------------------------------------

-- set directory for oracle inventory

\--------------------------------------------

INVENTORY\_LOCATION=/ora01/app/oraInventory

\--------------------------------------------

-- set oracle home for binaries

\--------------------------------------------

ORACLE\_HOME=/ora01/app/oracle/product/19.3.0.0/db\_1

\--------------------------------------------

-- set oracle home for binaries

\--------------------------------------------

ORACLE\_BASE=/ora01/app/oracle

\--------------------------------------------

-- set version of binaries to install

-- EE - enterprise edition

\--------------------------------------------

oracle.install.db.InstallEdition=EE

\--------------------------------------------

-- specify extra groups for database management

\--------------------------------------------

oracle.install.db.OSDBA\_GROUP=dba

oracle.install.db.OSOPER\_GROUP=oper

oracle.install.db.OSBACKUPDBA\_GROUP=backupdba

oracle.install.db.OSDGDBA\_GROUP=dgdba

oracle.install.db.OSKMDBA\_GROUP=kmdba

oracle.install.db.OSRACDBA\_GROUP=racdba

once edition is completed. Start binaries installation.

cd /ora01/app/oracle/product/19.3.0.0/db\_1

./runInstaller -silent \

-responseFile /ora01/app/oracle/product/19.3.0.0/db\_1/install/response/db\_install.rsp

output is following

[oracle@oel7 db\_1]$ ./runInstaller -silent \ -responseFile /ora01/app/oracle/product/19.3.0.0/db\_1/install/response/db\_install.rsp
Launching Oracle Database Setup Wizard...

The response file for this session can be found at:
` `/ora01/app/oracle/product/19.3.0.0/db\_1/install/response/db\_2019-06-07\_11-13-06AM.rsp

You can find the log of this install session at:
` `/tmp/InstallActions2019-06-07\_11-13-06AM/installActions2019-06-07\_11-13-06AM.log

As a root user, execute the following script(s):
`	`1. /ora01/app/oraInventory/orainstRoot.sh
`	`2. /ora01/app/oracle/product/19.3.0.0/db\_1/root.sh

Execute /ora01/app/oraInventory/orainstRoot.sh on the following nodes: 
[oel7]
Execute /ora01/app/oracle/product/19.3.0.0/db\_1/root.sh on the following nodes: 
[oel7]

Successfully Setup Software.
Moved the install session logs to:
` `/ora01/app/oraInventory/logs/InstallActions2019-06-07\_11-13-06AM

I got warnings about memory Oracle requires 8GB ram but VirtualBox consumed 128MB for VideoMemory.

you are asked to run two scripts as user root. Once it’s done binaries are installed. I’m not sure if it’s necessary from previous logs it looks it’s already done

[root@oel7 /]# 

/ora01/app/oraInventory/orainstRoot.sh

/ora01/app/oracle/product/19.3.0.0/db\_1/root.sh

quick binary verification

[oracle@oel7 db\_1]$ sqlplus / as sysdba

SQL\*Plus: Release 19.0.0.0.0 - Production on Fri Jun 7 11:17:42 2019
Version 19.3.0.0.0

Copyright (c) 1982, 2019, Oracle.  All rights reserved.

Connected to an idle instance.

SQL>

Configure Oracle Net

Again based on response file Oracle Net will be configured

cd /ora01/app/oracle/product/19.3.0.0/db\_1/assistants/netca

cp netca.rsp netca.rsp.bck

You can edit netca.rsp to set own parameters. I didn’t changed anything here. So just start standard configuration. It will configure LISTENER with standard settings.

netca -silent -responseFile /ora01/app/oracle/product/19.3.0.0/db\_1/assistants/netca/netca.rsp

netca -silent -responseFile /ora01/app/oracle/product/19.3.0.0/db\_1/assistants/netca/netca.rsp

Parsing command line arguments:
`    `Parameter "silent" = true
`    `Parameter "responsefile" = /ora01/app/oracle/product/19.3.0.0/db\_1/assistants/netca/netca.rsp
Done parsing command line arguments.
Oracle Net Services Configuration:
Profile configuration complete.
Oracle Net Listener Startup:
`    `Running Listener Control: 
`      `/ora01/app/oracle/product/19.3.0.0/db\_1/bin/lsnrctl start LISTENER
`    `Listener Control complete.
`    `Listener started successfully.
Listener configuration complete.
Oracle Net Services configuration successful. The exit code is 0

Check LISTENER status

[oracle@oel7 db\_1]$ lsnrctl status

LSNRCTL for Linux: Version 19.0.0.0.0 - Production on 07-JUN-2019 11:32:53

Copyright (c) 1991, 2019, Oracle.  All rights reserved.

Connecting to (DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=oel7.dbaora.com)(PORT=1521)))
STATUS of the LISTENER
\------------------------
Alias                     LISTENER
Version                   TNSLSNR for Linux: Version 19.0.0.0.0 - Production
Start Date                07-JUN-2019 11:28:40
Uptime                    0 days 0 hr. 4 min. 13 sec
Trace Level               off
Security                  ON: Local OS Authentication
SNMP                      OFF
Listener Parameter File   /ora01/app/oracle/product/19.3.0.0/db\_1/network/admin/listener.ora
Listener Log File         /ora01/app/oracle/diag/tnslsnr/oel7/listener/alert/log.xml
Listening Endpoints Summary...
`  `(DESCRIPTION=(ADDRESS=(PROTOCOL=tcp)(HOST=oel7)(PORT=1521)))
`  `(DESCRIPTION=(ADDRESS=(PROTOCOL=ipc)(KEY=EXTPROC1521)))
The listener supports no services
The command completed successfully

Configure database

The last setup is to create new container database ORA19C.dbaora.com with one pluggable database PORA1891 and configure and enable oracle db express

Prepare directories for database datafiles and flash recovery area

mkdir /ora01/app/oracle/oradata

mkdir /ora01/app/oracle/flash\_recovery\_area

backup original response file for dbca

cd /ora01/app/oracle/product/19.3.0.0/db\_1/assistants/dbca

cp dbca.rsp dbca.rsp.bck

vi dbca.rsp

set own parameters

\--------------------------------------------

-- global database name

\--------------------------------------------

gdbName=ORA19C.dbaora.com

\--------------------------------------------

-- instance database name

\--------------------------------------------

sid=ORA19C

\--------------------------------------------

--create container database

\--------------------------------------------

createAsContainerDatabase=true

\--------------------------------------------

-- number of pluggable databases

\--------------------------------------------

numberOfPDBs=1

\--------------------------------------------

-- list of pluggable databases

\--------------------------------------------

pdbName=PORA19C1


\-------------------------------------------- 
-- Flag to create local undo tablespace for all PDB's.
-------------------------------------------- useLocalUndoForPDBs=true

\--------------------------------------------

-- pluggable administrator password

\--------------------------------------------

pdbAdminPassword=Oracle19c#

\--------------------------------------------

-- template name used to create database

\--------------------------------------------

templateName=General\_Purpose.dbc

\--------------------------------------------

-- password for user sys

\--------------------------------------------

sysPassword=Oracle19c#

\--------------------------------------------

-- password for user system

\--------------------------------------------

systemPassword=Oracle19c#

\--------------------------------------------

-- configure dbexpress with port 5500

\--------------------------------------------

emConfiguration=DBEXPRESS

emExpressPort=5510

\--------------------------------------------

-- password for dbsnmp user

\--------------------------------------------

dbsnmpPassword=Oracle19c#

\--------------------------------------------

-- default directory for oracle database datafiles

\--------------------------------------------

datafileDestination=/ora01/app/oracle/oradata

\--------------------------------------------

-- default directory for flashback data

\--------------------------------------------

recoveryAreaDestination=/ora01/app/oracle/flash\_recovery\_area

\--------------------------------------------

-- storage used for database installation

-- FS - OS filesystem

\--------------------------------------------

storageType=FS


\--------------------------------------------

-- database character set

\--------------------------------------------

characterSet=AL32UTF8

\--------------------------------------------

-- national database character set

\--------------------------------------------

nationalCharacterSet=AL16UTF16

\--------------------------------------------

-- listener name to register database to

\--------------------------------------------

listeners=LISTENER

\--------------------------------------------

-- force to install sample schemas on the database

\--------------------------------------------

sampleSchema=true

\--------------------------------------------

--specify database type

--has influence on some instance parameters

\--------------------------------------------

databaseType=OLTP

\--------------------------------------------

-- defines size of memory used by the database

\--------------------------------------------

totalMemory=4096

run database installation

dbca -silent -createDatabase \

-responseFile /ora01/app/oracle/product/19.3.0.0/db\_1/assistants/dbca/dbca.rsp

Example output

[oracle@oel7 dbca]$ dbca -silent -createDatabase \
\> -responseFile /ora01/app/oracle/product/19.3.0.0/db\_1/assistants/dbca/dbca.rsp
Prepare for db operation
8% complete
Copying database files
31% complete
Creating and starting Oracle instance
32% complete
36% complete
40% complete
43% complete
46% complete
Completing Database Creation
51% complete
54% complete
Creating Pluggable Databases
58% complete
77% complete
Executing Post Configuration Actions
100% complete
Database creation complete. For details check the logfiles at:
` `/ora01/app/oracle/cfgtoollogs/dbca/ORA19C.
Database Information:
Global Database Name:ORA19C.dbaora.com
System Identifier(SID):ORA19C
Look at the log file "/ora01/app/oracle/cfgtoollogs/dbca/ORA19C/ORA19C.log" for further details.

Verify connection

[oracle@oel7 dbca]$ sqlplus / as sysdba

SQL\*Plus: Release 19.0.0.0.0 - Production on Sat Jun 8 02:35:22 2019
Version 19.3.0.0.0

Copyright (c) 1982, 2019, Oracle.  All rights reserved.


Connected to:
Oracle Database 19c Enterprise Edition Release 19.0.0.0.0 - Production
Version 19.3.0.0.0

SQL> show parameter db\_name

NAME		TYPE        VALUE
\--------------- ----------- ------------------------------
db\_name         string      ORA19C

SQL> alter session set container=PORA19C1;

Session altered.

SQL> show con\_id

CON\_ID
\------------------------------
3
SQL> show con\_name

CON\_NAME
\------------------------------
PORA19C1
SQL>

Check port status of db express in root database

SQL> ALTER SESSION SET CONTAINER=cdb$root;

Session altered.

SQL> select DBMS\_XDB\_CONFIG.GETHTTPSPORT from dual;

GETHTTPSPORT
\------------
`	`5510

SQL>

