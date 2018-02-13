#!/bin/bash 
# 
# copstart.sh
#
# This script will install the firmware and device defaults
#
# SYNOPSIS
# copstart.sh <context> <logfile>
#
# turn it on for debug
#set x

#
# Checking parameters
#
if [ $# -lt 1 ]
then
  CONTEXT="options"
else
  CONTEXT=$1
fi
#
# Set some env variables
#
# Context will be either options (default), install or L2
#
TMPDIR=`pwd`
LOGFILE=${TMPDIR}/install.log
TFTPDIR=/usr/local/cm/tftp
LOADINFODIR=/usr/local/cm/db/loadinfo
INSTALLDB=/usr/local/cm/bin/installdb

LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cm/lib
export LD_LIBRARY_PATH

#
# Copy files and change permissions
#
echo "Installing *.sbn, *.loads and load info files" > ${LOGFILE}
/bin/chmod 770 ${TMPDIR}/*.txt ${TMPDIR}/*.sbn ${TMPDIR}/*.loads 

/bin/chown ctftp ${TMPDIR}/*.sbn ${TMPDIR}/*.loads
/bin/chown database ${TMPDIR}/*.txt

/bin/chgrp ccmbase ${TMPDIR}/*.txt ${TMPDIR}/*.loads ${TMPDIR}/*.sbn

/bin/cp -fp ${TMPDIR}/*.txt ${LOADINFODIR}/
/bin/cp -fp ${TMPDIR}/*.sbn ${TFTPDIR}/
/bin/cp -fp ${TMPDIR}/*.loads ${TFTPDIR}/

#
# Remove any old TERMxx.DEFAULT.loads files
#
echo "Cleaning up TERMxx.DEFAULT.loads files..." >> ${LOGFILE}
term_default_files="`/bin/ls term*.default.loads`"
for term_default_file in $term_default_files
do
    model="`echo $term_default_file | /bin/cut -c5- | /bin/cut -d. -f1`"
    /bin/rm -f ${TFTPDIR}/TERM$model.DEFAULT.loads
done

#
# Update the device defaults
#
echo "Updating device defaults..." >> ${LOGFILE}
echo "from load files in ${TMPDIR}" >> ${LOGFILE}
load_files="`/bin/ls ${TMPDIR}/*.txt`";

# Context equals 'L2', 'options' or 'install'
if [ ${CONTEXT} != "L2" ]
then 
  echo "Updating device defaults for non-L2" >> ${LOGFILE}
  L2_OPT=
else
  echo "Updating device defaults for L2" >> ${LOGFILE}
  L2_OPT=L2
fi
for load_file in $load_files
do
  /bin/su -l informix -s /bin/sh -c "source /usr/local/cm/db/dblenv.bash /usr/local/cm ; source /usr/local/cm/db/informix/local/ids.env ${L2_OPT}; $INSTALLDB -l $load_file" >> ${LOGFILE}
done
exit 0

