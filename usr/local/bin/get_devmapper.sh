#!/bin/bash
#
# $Id get_devmapper.sh v1.1.0 19/01/2021 <danilo.cilento@gmail.com> $
#
# Description: Get device mapping of the logical volumes on VCSA
#
#


regex1='^(.+_vg-|.+-lv_)(.+)=(.+)$'
regex2='^(.+)(\,)$'

usage() {
   echo "Usage: $0 { -s <vcenter fqdn> | -a <vcenter fqdn list> }"
   echo "Examples:"
   echo "1) $0 -s \"vcenter1.local.intranet\""
   echo "2) $0 -a \"vcenter1.local.intranet;vcenter2.local.intranet;vcenter3.local.intranet\""
}

storedata() {
   influx="devmapper,vcenter=${vc} ${result}"
   echo $influx
}

show-mapping() {
   result=""
   mapper=(${devmapper//;/ })
   for elem in "${mapper[@]}"; do
      if [[ $elem =~ $regex1 ]]; then
         lv=${BASH_REMATCH[2]}
         dm=${BASH_REMATCH[3]}
         result=$result"${lv}=\"${dm}\","
      fi
   done
   if [[ $result =~ $regex2 ]]; then
      result=${BASH_REMATCH[1]}
   fi
   storedata
}

get-devmapper() {
   devmapper=$(/usr/bin/ssh -q -o StrictHostKeyChecking=accept-new -o ConnectTimeout=1 -o ConnectionAttempts=2 monitor@${vc} ls -l /dev/mapper | awk -F' ' '{ gsub(/\.\.\//, "", $11); print $9"="$11";"; }' | /usr/bin/grep -i dm | /usr/bin/sort -k1)

   if [[ ! -z $devmapper ]]; then 
      show-mapping
   fi
}

if [[ ( "$1" == "-h" ) || ( "$#" -eq 2 ) ]]; then
   while getopts ":ha:s:" opt; do
      case $opt in
        # Help
        h)
          usage
          exit 1
          ;;
        # Get device mapper on vcenter list
        a)
          vcsa=(${OPTARG//;/ })
          if [[ ! -z $vcsa ]]; then
             for vc in "${vcsa[@]}"; do
                get-devmapper ${vc}
             done
          else
             echo "[ERROR] -a was triggered, value is empty" >&2
             usage
             exit 1
          fi
          ;;
        # Get device mapper on a specific vcenter
        s)
          if [[ ! -z $OPTARG ]]; then
	     vc=$OPTARG
             get-devmapper ${vc}
          else
             echo "[ERROR] -s was triggered, value is empty" >&2
             usage
             exit 1
          fi
          ;;
        \?)
          echo "[ERROR] Invalid option: -$OPTARG" >&2
          usage
          exit 1
          ;;
        :)
          echo "[ERROR] Option -$OPTARG requires an argument." >&2
          usage
          exit 1
          ;;
      esac
   done
else
   if [[ "$#" -ne 2 ]]; then
      echo "[ERROR] Illegal number of parameters"
      usage
      exit 1
   fi
fi
