#
#   Copyright (c) 2005,2008 Cisco Systems Inc.  All rights
#   reserved.
#
# ######################################################################
#
# copstart.py
#
# This script will install the firmware and device defaults
#
# SYNOPSIS
# python copstart.py <context> <logfile>
#
# created:         2007-10-29
# author:          Mahesh Gopalakrishna Pai R (mapai@cisco.com)
# ######################################################################

import os
import sys
import socket

#
# Checking parameters
#
if len(sys.argv) < 2:
    CONTEXT="options"
else:
    CONTEXT=sys.argv[1]

if len(sys.argv) < 3:
    LOGFILE="install.log"
else:
    LOGFILE=sys.argv[2]

#
# Set some env variables
#
# Context will be either options (default), install or L2
#
TMPDIR="C:\\cisco\\common\\download"
TFTPDIR="C:\\Cisco\\cm\\tftp"
LOADINFODIR="C:\\Cisco\\cm\\db\\loadinfo"
INSTALLDB="C:\\Cisco\\cm\\bin\\installdb"

##### Executes commands    
def syscmd(cmd):
    rc = os.system(cmd)
    os.system("echo Executing [%s]" % cmd)
    if rc != 0:
        os.system("echo Error executing [%s] returned [%s]" % (cmd, rc))
    return rc

#
# Change permissions and copy files
#
syscmd("echo Installing *.sbn, *.loads and load info files")

# Permissions
ACL_PATH=TMPDIR + "\\*.sbn"
print ('Setting ACLs for "%s"' % ACL_PATH)
syscmd('cmcacls "%s" /T /C /E /P ctftp:F ' % (ACL_PATH))
syscmd('cmcacls "%s" /T /C /E /P database:F ' % (ACL_PATH))
syscmd('cmcacls "%s" /T /C /E /P ccmbase-group:F ' % (ACL_PATH))

ACL_PATH=TMPDIR + "\\*.loads"
print ('Setting ACLs for "%s"' % ACL_PATH)
syscmd('cmcacls "%s" /T /C /E /P ctftp:F ' % (ACL_PATH))
syscmd('cmcacls "%s" /T /C /E /P database:F ' % (ACL_PATH))
syscmd('cmcacls "%s" /T /C /E /P ccmbase-group:F ' % (ACL_PATH))

ACL_PATH=TMPDIR + "\\*.txt"
print ('Setting ACLs for "%s"' % ACL_PATH)
syscmd('cmcacls "%s" /T /C /E /P administrator:F ' % (ACL_PATH))
syscmd('cmcacls "%s" /T /C /E /P administrators:F ' % (ACL_PATH))

# Copy Files
syscmd("copy /y " + TMPDIR + "\\*.txt " + LOADINFODIR + "\\")
syscmd("copy /y " + TMPDIR + "\\*.sbn " + TFTPDIR + "\\")
syscmd("copy /y " + TMPDIR + "\\*.loads " + TFTPDIR + "\\")

#
# Remove any old TERMxx.DEFAULT.loads files
#
syscmd("echo Cleaning up TERMxx.DEFAULT.loads files...")
fileList = os.popen("dir /b %s\\term*.default.loads" %(TMPDIR))
while 1:
    fileName = fileList.readline()
    if not fileName:
	break
    model=fileName.upper().split("M")[1].split(".")[0].strip()
    syscmd("del /f " + TFTPDIR + "\\TERM" + model + ".DEFAULT.loads")
    
#
# Update the device defaults
#
syscmd("echo Updating device defaults...")
syscmd("echo from load files in " + TMPDIR)

# Context equals 'L2', 'options' or 'install'
if CONTEXT != "L2": 
  syscmd("echo Updating device defaults for non-L2")
  L2_OPT=""
else:
  syscmd("echo Updating device defaults for L2")
  L2_OPT=L2

fileList = os.popen("dir /b " + TMPDIR + "\\*.txt") 
exitCode=0 
while 1:
    fileName = fileList.readline()
    if not fileName:
	break
    rc=syscmd("C:\\INFORMIX\\" + socket.gethostname().replace('-','_') + "_ccm.cmd && " + INSTALLDB + "  -l " + TMPDIR + "\\" + fileName )
    if rc != 0:
    	exitCode=rc
    
sys.exit(exitCode)

