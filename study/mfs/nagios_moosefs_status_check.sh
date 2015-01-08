#!/bin/bash
# ===========================================================================================================
#
# MooseFS status check plugins for nagios
#
# Written by : liu yunfeng
# Release : 1.0
# Create Date : 2010-05-18
# Description : Nagios plugins (script) to check MooseFS status
# Modified by : liu-yunfeng
# Modified : add moosefs disk use status
#
# ===========================================================================================================

# Nagios return codes
STATE_OK=0
STATE_WARNING=1
STATE_CRITICAL=2
STATE_UNKNOWN=3


#Get Master server Process
Master(){
MFS_PID=`ps -ef | grep mfsmaster | grep ${mfspath} | awk '{print $2}'`
if [ "${MFS_PID}" = "" ];then
echo "ERROR : mfs master does not start"
exit $STATE_CRITICAL
else
echo "OK : mfs master server running OK!"
exit $STATE_OK
fi
}

#Get chunker server Process
Chunker(){
MFS_PID=`ps -ef | grep mfschunkserver | grep ${mfspath} | awk '{print $2}'`

if [ "${MFS_PID}" = "" ];then
echo "ERROR : mfs chunkserver does not start"
exit $STATE_CRITICAL
else
echo "OK : mfs master chunkserver running OK!"
exit $STATE_OK
fi
}

#Get disk used status
Disk_used(){
Disk_used=`df -h | grep ${mountpoint} |awk '{print $4}'`
mfs_disk_total=`df -h | grep ${mountpoint} | awk '{print $1}'`
mfs_disk_used=`df -h | grep ${mountpoint} | awk '{print $2}'`
mfs_disk_free=`df -h | grep ${mountpoint} | awk '{print $3}'`

if [ ${Disk_used%\%} -ge ${warningdiskused} -a ${Disk_used%\%} -lt ${criticaldiskused} ];then
echo "Waring :mfs disk used Rate is "${Disk_used}""
exit $STATE_WARNING
elif [ ${Disk_used%\%} -ge ${criticaldiskused} ];then
echo "CRITICAL :mfs disk used Rate is "${Disk_used}""
exit $STATE_CRITICAL
elif [ "${Disk_used%\%}" = "" ];then
echo "CRITICAL :mfs client not mount on"
exit $STATE_CRITICAL
else
echo "OK : MFS client mount on , disk total is ${mfs_disk_total},disk used is ${mfs_disk_used},disk free is ${mfs_disk_free} and disk used rate is "${Disk_used}" , Everything is OK!"
exit $STATE_OK
fi
}

#Get metalogger server Process
Metalogger(){
MFS_PID=`ps -ef | grep mfsmetalogger | grep ${mfspath} | awk '{print $2}'`

if [ "${MFS_PID}" = "" ];then
echo "ERROR : mfs mfsmetalogger does not start"
exit $STATE_CRITICAL
else
echo "OK : mfs master mfsmetalogger running OK!"
exit $STATE_OK
fi
}

# Functions plugin usage
print_usage()
{
echo ""
echo " -M MFS master server status "
echo " -C MFS chunker server status "
echo " -U MFS client disk used Rate "
echo " -L MFS metalogger server status "
echo " -h Show this page "
echo ""
echo " Usage1 : check_mfs.sh -M mfsmasterpath"
echo " ex : check_mfs.sh -M /usr/local/mfs"
echo " Usage2 : check_mfs.sh -C mfschunkpath"
echo " ex : check_mfs.sh -C /usr/local/mfs"
echo " Usage3 : check_mfs.sh -U mountpoint warningrate criticalrate"
echo " ex : check_mfs.sh -U /mnt/mfs 60 80"
echo " Usage4 : check_mfs.sh -L mfsmetaloggerpath"
echo " ex : check_mfs.sh -L /usr/local/mfs"
echo " ex : check_mfs.sh -h"
echo ""
exit 0
}



# Parse parameter
while [ $# -gt 0 ]
do
case "$1" in
-h | --help)
print_usage
exit $STATE_OK
;;
-M | --master)
mfspath=${2:-"/usr/local/mfs"}
Master
exit
;;
-C | --chunker)
mfspath=${2:-"/usr/local/mfs"}
Chunker
;;
-U | --usedwarning)
mountpoint=${2:-"/mnt/mfs"}
warningdiskused=${3:-"75"}
criticaldiskused=${4:-"85"}
Disk_used
;;
-L | --metalogger)
mfspath=${2:-"/usr/local/mfs"}
Metalogger
;;
*) echo "Unknown argement: $1"
exit $STATE_UNKNOWN
;;
esac
shift
done
