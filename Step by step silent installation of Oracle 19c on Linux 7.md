**Step by step silent installation of Oracle 19c on Linux 7**

***Step by step silent installation of Oracle 19c on Linux 7***

![](Aspose.Words.000562b5-ba4c-4485-b9da-4a79f172a3bb.001.png)


As everyone aware of the oracle database installation. oracle database installation can be done through 2 methods.

1. runInstaller(GUI mode).
1. **Silent Installation.**

   Basically, we use runInstaller to install the database, as we all know runInstaller required a graphical interface which is an additional cost to the organization.

   Sometimes we might not have access to a graphical interface.

   The silent installation allows installing the Oracle components without using a graphical interface.

Here we are going to illustrate step by step how to install the Oracle 19c database using the silent installation.

Below are the steps which we are followed to install the oracle 19c binary on Linux 7.

If we are installing the first time, we need to run step1 to step 5. Since we have access to the console as root user if you don’t have root access on the server then reach to your System Admin to perform steps 1 to 5.

**1.** **Hardware Requirement.**
Oracle 19c installation, we have to required Linux 7 64 bit.
In my environment, we are using Linux 7.9

[root@localhost ~]# cat /etc/redhat-release

Red Hat Enterprise Linux Server release 7.9 (Maipo)


**2. Create Directory**
Here we are creating u01 and u02 directory for installation, where **/u01/app/oracle/product/19.0.0/dbhome\_1** is the oracle home and **/u02/oradata** which used for datafile location (soon will publish manual creation of a database on 19c)

[root@localhost Packages]# mkdir -p /u01/app/oracle/product/19.0.0/dbhome\_1

[root@localhost Packages]# mkdir -p /u02/oradata


**3. Create the new groups and users**

Below we are creating groups which is required at the time of installation

[root@localhost Packages]# groupadd -g 10052 oinstall

[root@localhost Packages]# groupadd -g 10054 dba


**4. Change Ownership and permissions**
we have to change the ownership and permissions of the directories so that oracle user can read, write, and execute files.

[root@localhost Packages]# chown -R oracle:oinstall /u01 /u02

[root@localhost Packages]# chmod -R 775 /u01 /u02


**5. Pre-requisites required for oracle installation**
Before moving forward toward installation, Below pre-requisites required for oracle 19c.

[root@localhost Packages]# yum install -y oracle-database-preinstall-19c

Loaded plugins: langpacks, ulninfo

ol7\_UEKR6                                                       | 2.5 kB  00:00:00     

ol7\_latest                                                      | 2.7 kB  00:00:00     

(1/3): ol7\_latest/x86\_64/group                                  | 660 kB  00:00:07     

(2/3): ol7\_latest/x86\_64/updateinfo                             | 3.1 MB  00:00:07     

(3/3): ol7\_latest/x86\_64/primary\_db                             |  30 MB  00:00:06     

Resolving Dependencies

--> Running transaction check

---> Package oracle-database-preinstall-19c.x86\_64 0:1.0-2.el7 will be installed

--> Processing Dependency: ksh for package: oracle-database-preinstall-19c-1.0-2.el7.x86\_64

--> Running transaction check

---> Package ksh.x86\_64 0:20120801-142.0.1.el7 will be installed

--> Finished Dependency Resolution


Dependencies Resolved

\=======================================================================================

` `Package                          Arch     Version                  Repository    Size

\=======================================================================================

Installing:

` `oracle-database-preinstall-19c   x86\_64   1.0-2.el7                ol7\_latest    19 k

Installing for dependencies:

` `ksh                              x86\_64   20120801-142.0.1.el7     ol7\_latest   882 k

Transaction Summary

\=======================================================================================

Install  1 Package (+1 Dependent package)

Total download size: 901 k

Installed size: 3.2 M

Downloading packages:

No Presto metadata available for ol7\_latest

warning: /var/cache/yum/x86\_64/7Server/ol7\_latest/packages/oracle-database-preinstall-19c-1.0-2.el7.x86\_64.rpm: Header V3 RSA/SHA256 Signature, key ID ec551f03: NOKEY

Public key for oracle-database-preinstall-19c-1.0-2.el7.x86\_64.rpm is not installed

(1/2): oracle-database-preinstall-19c-1.0-2.el7.x86\_64.rpm      |  19 kB  00:00:08     

(2/2): ksh-20120801-142.0.1.el7.x86\_64.rpm                      | 882 kB  00:00:08     

\---------------------------------------------------------------------------------------

Total                                                      97 kB/s | 901 kB  00:09     

Retrieving key from file:///etc/pki/rpm-gpg/RPM-GPG-KEY-oracle

Importing GPG key 0xEC551F03:

` `Userid     : "Oracle OSS group (Open Source Software group) <build@oss.oracle.com>"

` `Fingerprint: 4214 4123 fecf c55b 9086 313d 72f9 7b74 ec55 1f03

` `Package    : 7:oraclelinux-release-7.9-1.0.9.el7.x86\_64 (@anaconda/7.9)

` `From       : /etc/pki/rpm-gpg/RPM-GPG-KEY-oracle

Running transaction check

Running transaction test

Transaction test succeeded

Running transaction

Warning: RPMDB altered outside of yum.

`  `Installing : ksh-20120801-142.0.1.el7.x86\_64                                     1/2 

`  `Installing : oracle-database-preinstall-19c-1.0-2.el7.x86\_64                     2/2 

`  `Verifying  : oracle-database-preinstall-19c-1.0-2.el7.x86\_64                     1/2 

`  `Verifying  : ksh-20120801-142.0.1.el7.x86\_64                                     2/2 

Installed:

`  `oracle-database-preinstall-19c.x86\_64 0:1.0-2.el7                                    

Dependency Installed:

`  `ksh.x86\_64 0:20120801-142.0.1.el7                                                    

Complete!


**Now onwards, all steps will be executed as user oracle except step 10**

**6. Unzip software**
**In the silent installation, you have to unzip the oracle binary directly under the ORACLE HOME location.**

unzip oracle binary under oracle home as below.

[oracle@localhost dbhome\_1]$ cd /u01/app/oracle/product/19.0.0/dbhome\_1/

[oracle@localhost dbhome\_1]$ unzip LINUX.X64\_193000\_db\_home.zip


**7. Edit response file.**
This response file is accustomed provide all the specified information for the installation, so no additional user input is required.

In below mention response file we have modified the highlighted parameter response file.

oracle@localhost response]$ cat db\_install.rsp

####################################################################

\## Copyright(c) Oracle Corporation 1998,2019. All rights reserved.##

\##                                                                ##

\## Specify values for the variables listed below to customize     ##

\## your installation.                                             ##

\##                                                                ##

\## Each variable is associated with a comment. The comment        ##

\## can help to populate the variables with the appropriate        ##

\## values.                                                        ##

\##                                                                ##

\## IMPORTANT NOTE: This file contains plain text passwords and    ##

\## should be secured to have read permission only by oracle user  ##

\## or db administrator who owns this installation.                ##

\##                                                                ##

####################################################################


#------------------------------------------------------------------------------

\# Do not change the following system generated value. 

#------------------------------------------------------------------------------

oracle.install.responseFileVersion=/oracle/install/rspfmt\_dbinstall\_response\_schema\_v19.0.0

#-------------------------------------------------------------------------------

\# Specify the installation option.

\# It can be one of the following:

\#   - INSTALL\_DB\_SWONLY

\#   - INSTALL\_DB\_AND\_CONFIG

#-------------------------------------------------------------------------------

oracle.install.option=INSTALL\_DB\_SWONLY

#-------------------------------------------------------------------------------

\# Specify the Unix group to be set for the inventory directory.  

#-------------------------------------------------------------------------------

UNIX\_GROUP\_NAME=oinstall

#-------------------------------------------------------------------------------

\# Specify the location which holds the inventory files.

\# This is an optional parameter if installing on

\# Windows based Operating System.

#-------------------------------------------------------------------------------

INVENTORY\_LOCATION=/u01/app/oraInventory

#-------------------------------------------------------------------------------

\# Specify the complete path of the Oracle Home. 

#-------------------------------------------------------------------------------

ORACLE\_HOME=/u01/app/oracle/product/19.0.0/dbhome\_1

#-------------------------------------------------------------------------------

\# Specify the complete path of the Oracle Base. 

#-------------------------------------------------------------------------------

ORACLE\_BASE=/u01/app/oracle

#-------------------------------------------------------------------------------

\# Specify the installation edition of the component.                     

\#                                                             

\# The value should contain only one of these choices.  

\#   - EE     : Enterprise Edition 

\#   - SE2     : Standard Edition 2


#-------------------------------------------------------------------------------

oracle.install.db.InstallEdition=EE

###############################################################################

\#                                                                             #

\# PRIVILEGED OPERATING SYSTEM GROUPS                                          #

\# ------------------------------------------                                  #

\# Provide values for the OS groups to which SYSDBA and SYSOPER privileges     #

\# needs to be granted. If the install is being performed as a member of the   #

\# group "dba", then that will be used unless specified otherwise below.       #

\#                                                                             #

\# The value to be specified for OSDBA and OSOPER group is only for UNIX based #

\# Operating System.                                                           #

\#                                                                             #

###############################################################################

#------------------------------------------------------------------------------

\# The OSDBA\_GROUP is the OS group which is to be granted SYSDBA privileges.

#-------------------------------------------------------------------------------

oracle.install.db.OSDBA\_GROUP=oinstall

#------------------------------------------------------------------------------

\# The OSOPER\_GROUP is the OS group which is to be granted SYSOPER privileges.

\# The value to be specified for OSOPER group is optional.

#------------------------------------------------------------------------------

oracle.install.db.OSOPER\_GROUP=oinstall

#------------------------------------------------------------------------------

\# The OSBACKUPDBA\_GROUP is the OS group which is to be granted SYSBACKUP privileges.

#------------------------------------------------------------------------------

oracle.install.db.OSBACKUPDBA\_GROUP=oinstall

#------------------------------------------------------------------------------

\# The OSDGDBA\_GROUP is the OS group which is to be granted SYSDG privileges.

#------------------------------------------------------------------------------

oracle.install.db.OSDGDBA\_GROUP=oinstall

#------------------------------------------------------------------------------

\# The OSKMDBA\_GROUP is the OS group which is to be granted SYSKM privileges.

#------------------------------------------------------------------------------

oracle.install.db.OSKMDBA\_GROUP=oinstall

#------------------------------------------------------------------------------

\# The OSRACDBA\_GROUP is the OS group which is to be granted SYSRAC privileges.

#------------------------------------------------------------------------------

oracle.install.db.OSRACDBA\_GROUP=oinstall

################################################################################

\#                                                                              #

\#                      Root script execution configuration                     #

\#                                                                              #

################################################################################

#-------------------------------------------------------------------------------------------------------

\# Specify the root script execution mode.

\#

\#   - true  : To execute the root script automatically by using the appropriate configuration methods.

\#   - false : To execute the root script manually.

\#

\# If this option is selected, password should be specified on the console.

#-------------------------------------------------------------------------------------------------------

oracle.install.db.rootconfig.executeRootScript=false

#--------------------------------------------------------------------------------------

\# Specify the configuration method to be used for automatic root script execution.

\#

\# Following are the possible choices:

\#   - ROOT

\#   - SUDO

#--------------------------------------------------------------------------------------

oracle.install.db.rootconfig.configMethod=

#--------------------------------------------------------------------------------------

\# Specify the absolute path of the sudo program.

\#

\# Applicable only when SUDO configuration method was chosen.

#--------------------------------------------------------------------------------------

oracle.install.db.rootconfig.sudoPath=

#--------------------------------------------------------------------------------------

\# Specify the name of the user who is in the sudoers list. 

\# Applicable only when SUDO configuration method was chosen.

\# Note:For Single Instance database installations,the sudo user name must be the username of the user installing the database.

#--------------------------------------------------------------------------------------

oracle.install.db.rootconfig.sudoUserName=

###############################################################################

\#                                                                             #

\#                               Grid Options                                  #

\#                                                                             #

###############################################################################

#------------------------------------------------------------------------------

\# Value is required only if the specified install option is INSTALL\_DB\_SWONLY

\# 

\# Specify the cluster node names selected during the installation.

\# 

\# Example : oracle.install.db.CLUSTER\_NODES=node1,node2

#------------------------------------------------------------------------------

oracle.install.db.CLUSTER\_NODES=

###############################################################################

\#                                                                             #

\#                        Database Configuration Options                       #

\#                                                                             #

###############################################################################

#-------------------------------------------------------------------------------

\# Specify the type of database to create.

\# It can be one of the following:

\#   - GENERAL\_PURPOSE                       

\#   - DATA\_WAREHOUSE 

\# GENERAL\_PURPOSE: A starter database designed for general purpose use or transaction-heavy applications.

\# DATA\_WAREHOUSE : A starter database optimized for data warehousing applications.

#-------------------------------------------------------------------------------

oracle.install.db.config.starterdb.type=

#-------------------------------------------------------------------------------

\# Specify the Starter Database Global Database Name. 

#-------------------------------------------------------------------------------

oracle.install.db.config.starterdb.globalDBName=

#-------------------------------------------------------------------------------

\# Specify the Starter Database SID.

#-------------------------------------------------------------------------------

oracle.install.db.config.starterdb.SID=

#-------------------------------------------------------------------------------

\# Specify whether the database should be configured as a Container database.

\# The value can be either "true" or "false". If left blank it will be assumed

\# to be "false".

#-------------------------------------------------------------------------------

oracle.install.db.ConfigureAsContainerDB=

#-------------------------------------------------------------------------------

\# Specify the  Pluggable Database name for the pluggable database in Container Database.

#-------------------------------------------------------------------------------

oracle.install.db.config.PDBName=

#-------------------------------------------------------------------------------

\# Specify the Starter Database character set.

\#                                               

\#  One of the following

\#  AL32UTF8, WE8ISO8859P15, WE8MSWIN1252, EE8ISO8859P2,

\#  EE8MSWIN1250, NE8ISO8859P10, NEE8ISO8859P4, BLT8MSWIN1257,

\#  BLT8ISO8859P13, CL8ISO8859P5, CL8MSWIN1251, AR8ISO8859P6,

\#  AR8MSWIN1256, EL8ISO8859P7, EL8MSWIN1253, IW8ISO8859P8,

\#  IW8MSWIN1255, JA16EUC, JA16EUCTILDE, JA16SJIS, JA16SJISTILDE,

\#  KO16MSWIN949, ZHS16GBK, TH8TISASCII, ZHT32EUC, ZHT16MSWIN950,

\#  ZHT16HKSCS, WE8ISO8859P9, TR8MSWIN1254, VN8MSWIN1258

#-------------------------------------------------------------------------------

oracle.install.db.config.starterdb.characterSet=

#------------------------------------------------------------------------------

\# This variable should be set to true if Automatic Memory Management 

\# in Database is desired.

\# If Automatic Memory Management is not desired, and memory allocation

\# is to be done manually, then set it to false.

#------------------------------------------------------------------------------

oracle.install.db.config.starterdb.memoryOption=

#-------------------------------------------------------------------------------

\# Specify the total memory allocation for the database. Value(in MB) should be

\# at least 256 MB, and should not exceed the total physical memory available 

\# on the system.

\# Example: oracle.install.db.config.starterdb.memoryLimit=512

#-------------------------------------------------------------------------------

oracle.install.db.config.starterdb.memoryLimit=

#-------------------------------------------------------------------------------

\# This variable controls whether to load Example Schemas onto

\# the starter database or not.

\# The value can be either "true" or "false". If left blank it will be assumed

\# to be "false".

#-------------------------------------------------------------------------------

oracle.install.db.config.starterdb.installExampleSchemas=

###############################################################################

\#                                                                             #

\# Passwords can be supplied for the following four schemas in the	      #

\# starter database:      						      #

\#   SYS                                                                       #

\#   SYSTEM                                                                    #

\#   DBSNMP (used by Enterprise Manager)                                       #

\#                                                                             #

\# Same password can be used for all accounts (not recommended) 		      #

\# or different passwords for each account can be provided (recommended)       #

\#                                                                             #

###############################################################################

#------------------------------------------------------------------------------

\# This variable holds the password that is to be used for all schemas in the

\# starter database.

#-------------------------------------------------------------------------------

oracle.install.db.config.starterdb.password.ALL=

#-------------------------------------------------------------------------------

\# Specify the SYS password for the starter database.

#-------------------------------------------------------------------------------

oracle.install.db.config.starterdb.password.SYS=

#-------------------------------------------------------------------------------

\# Specify the SYSTEM password for the starter database.

#-------------------------------------------------------------------------------

oracle.install.db.config.starterdb.password.SYSTEM=

#-------------------------------------------------------------------------------

\# Specify the DBSNMP password for the starter database.

\# Applicable only when oracle.install.db.config.starterdb.managementOption=CLOUD\_CONTROL

#-------------------------------------------------------------------------------

oracle.install.db.config.starterdb.password.DBSNMP=

#-------------------------------------------------------------------------------

\# Specify the PDBADMIN password required for creation of Pluggable Database in the Container Database.

#-------------------------------------------------------------------------------

oracle.install.db.config.starterdb.password.PDBADMIN=

#-------------------------------------------------------------------------------

\# Specify the management option to use for managing the database.

\# Options are:

\# 1. CLOUD\_CONTROL - If you want to manage your database with Enterprise Manager Cloud Control along with Database Express.

\# 2. DEFAULT   -If you want to manage your database using the default Database Express option.

#-------------------------------------------------------------------------------

oracle.install.db.config.starterdb.managementOption=

#-------------------------------------------------------------------------------

\# Specify the OMS host to connect to Cloud Control.

\# Applicable only when oracle.install.db.config.starterdb.managementOption=CLOUD\_CONTROL

#-------------------------------------------------------------------------------

oracle.install.db.config.starterdb.omsHost=

#-------------------------------------------------------------------------------

\# Specify the OMS port to connect to Cloud Control.

\# Applicable only when oracle.install.db.config.starterdb.managementOption=CLOUD\_CONTROL

#-------------------------------------------------------------------------------

oracle.install.db.config.starterdb.omsPort=

#-------------------------------------------------------------------------------

\# Specify the EM Admin user name to use to connect to Cloud Control.

\# Applicable only when oracle.install.db.config.starterdb.managementOption=CLOUD\_CONTROL

#-------------------------------------------------------------------------------

oracle.install.db.config.starterdb.emAdminUser=

#-------------------------------------------------------------------------------

\# Specify the EM Admin password to use to connect to Cloud Control.

\# Applicable only when oracle.install.db.config.starterdb.managementOption=CLOUD\_CONTROL

#-------------------------------------------------------------------------------

oracle.install.db.config.starterdb.emAdminPassword=

###############################################################################

\#                                                                             #

\# SPECIFY RECOVERY OPTIONS                                 	              #

\# ------------------------------------		                              #

\# Recovery options for the database can be mentioned using the entries below  #

\#                                                                             #

###############################################################################

#------------------------------------------------------------------------------

\# This variable is to be set to false if database recovery is not required. Else 

\# this can be set to true.

#-------------------------------------------------------------------------------

oracle.install.db.config.starterdb.enableRecovery=

#-------------------------------------------------------------------------------

\# Specify the type of storage to use for the database.

\# It can be one of the following:

\#   - FILE\_SYSTEM\_STORAGE

\#   - ASM\_STORAGE

#-------------------------------------------------------------------------------

oracle.install.db.config.starterdb.storageType=

#-------------------------------------------------------------------------------

\# Specify the database file location which is a directory for datafiles, control

\# files, redo logs.         

\#

\# Applicable only when oracle.install.db.config.starterdb.storage=FILE\_SYSTEM\_STORAGE 

#-------------------------------------------------------------------------------

oracle.install.db.config.starterdb.fileSystemStorage.dataLocation=

#-------------------------------------------------------------------------------

\# Specify the recovery location.

\#

\# Applicable only when oracle.install.db.config.starterdb.storage=FILE\_SYSTEM\_STORAGE 

#-------------------------------------------------------------------------------

oracle.install.db.config.starterdb.fileSystemStorage.recoveryLocation=

#-------------------------------------------------------------------------------

\# Specify the existing ASM disk groups to be used for storage.

\#

\# Applicable only when oracle.install.db.config.starterdb.storageType=ASM\_STORAGE

#-------------------------------------------------------------------------------

oracle.install.db.config.asm.diskGroup=

#-------------------------------------------------------------------------------

\# Specify the password for ASMSNMP user of the ASM instance.                 

\#

\# Applicable only when oracle.install.db.config.starterdb.storage=ASM\_STORAGE 

#-------------------------------------------------------------------------------

oracle.install.db.config.asm.ASMSNMPPassword=


**8. Execute pre-installation command**

This step will perform a prerequisite that checks for the required component for the installation, if not, then we need to meet the requirement and move forward for installation.

Below command to verify the response file and dependent requirement.

[oracle@localhost dbhome\_1]$ ./runInstaller -executePrereqs -silent -responseFile /u01/app/oracle/product/19.0.0/dbhome\_1/install/response/db\_install.rsp

Launching Oracle Database Setup Wizard…

Prerequisite checks executed successfully.


**9. Install oracle 19c binary in silent installation.**
After satisfying the prerequisite, Now we are good to go to install oracle 19c.

[oracle@localhost dbhome\_1]$ ./runInstaller  -silent -responseFile /u01/app/oracle/product/19.0.0/dbhome\_1/install/response/db\_install.rsp

Launching Oracle Database Setup Wizard...

The response file for this session can be found at:

` `/u01/app/oracle/product/19.0.0/dbhome\_1/install/response/db\_2020-11-07\_01-08-43PM.rsp

You can find the log of this install session at:

` `/tmp/InstallActions2020-11-07\_01-08-43PM/installActions2020-11-07\_01-08-43PM.log



As a root user, execute the following script(s):

`	`1. /u01/app/oraInventory/orainstRoot.sh

`	`2. /u01/app/oracle/product/19.0.0/dbhome\_1/root.sh

Execute /u01/app/oraInventory/orainstRoot.sh on the following nodes: 

[localhost]

Execute /u01/app/oracle/product/19.0.0/dbhome\_1/root.sh on the following nodes: 

[localhost]


Successfully Setup Software.

Moved the install session logs to:

` `/u01/app/oraInventory/logs/InstallActions2020-11-07\_01-08-43PM


**10. Run the below script from the root user after installation**.

once the installation is completed successfully, we need to run the below scripts as the root users, In my case I have root, so I am running the below scripts from the root, else we need to contact System Admin/OS team to run the below scripts.

`	`1. /u01/app/oraInventory/orainstRoot.sh

`	`2. /u01/app/oracle/product/19.0.0/dbhome\_1/root.sh


Below is the output of the above scripts.

[root@localhost tmp]# /u01/app/oraInventory/orainstRoot.sh 

Changing permissions of /u01/app/oraInventory.

Adding read,write permissions for group.

Removing read,write,execute permissions for world.

Changing groupname of /u01/app/oraInventory to oinstall.

The execution of the script is complete.


Performing root user operation.

The following environment variables are set as:

`    `ORACLE\_OWNER= oracle

`    `ORACLE\_HOME=  /u01/app/oracle/product/19.0.0/dbhome\_1

`   `Copying dbhome to /usr/local/bin ...

`   `Copying oraenv to /usr/local/bin ...

`   `Copying coraenv to /usr/local/bin ...


Creating /etc/oratab file...

Entries will be added to the /etc/oratab file as needed by

Database Configuration Assistant when a database is created

Finished running generic part of root script.

Now product-specific root actions will be performed.

Oracle Trace File Analyzer (TFA) is available at : /u01/app/oracle/product/19.0.0/dbhome\_1/bin/tfactl 


**12. Verify after installation.**

After successful completion of the Oracle 19c installation, Now we are verifying oracle binary was installed properly or not.

Run below command from oracle users.

[oracle@localhost install]$ . oraenv

ORACLE\_SID = [test] ? 

ORACLE\_HOME = [/home/oracle] ? /u01/app/oracle/product/19.0.0/dbhome\_1/

The Oracle base remains unchanged with value /u01/app/oracle

OR

[oracle@localhost install]$ export ORACLE\_HOME=/u01/app/oracle/product/19.0.0/dbhome\_1/

[oracle@localhost install]$ export PATH=/u01/app/oracle/product/19.0.0/dbhome\_1/bin:$PATH

[oracle@localhost install]$ sqlplus -v

SQL\*Plus: Release 19.0.0.0.0 - Production

Version 19.3.0.0.0

[oracle@localhost install]$ sqlplus 

SQL\*Plus: Release 19.0.0.0.0 - Production on Tue Dec 1 13:33:26 2020

Version 19.3.0.0.0

Copyright (c) 1982, 2019, Oracle.  All rights reserved.

Enter user-name:

[oracle@localhost install]$ which sqlplus

/u01/app/oracle/product/19.0.0/dbhome\_1/bin/sqlplus
