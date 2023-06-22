#!/bin/bash
#
# $Id health_snmp_agent.sh v1.1.0 19/01/2021 <danilo.cilento@gmail.com> $
#
# Description: Check status of the SNMP agent on VCSA
#
#

DEBUG=false
regex1='^(\w+)((\.\w+){1,3})?'
regex2='^SNMPv2-SMI.+"(\w+)((\.\w+){1,3})?"'

usage() {
   echo "Usage: $0 -c <snmpv2 community> { -s <vcenter fqdn> | -a <vcenter fqdn list> }"
   echo "Examples:"
   echo "1) $0 -c \"public\" -s \"vcenter1.local.intranet\""
   echo "2) $0 -c \"public\" -a \"vcenter1.local.intranet;vcenter2.local.intranet;vcenter3.local.intranet\""
}

storedata() {
   influx="snmp_health,vcenter=${1} agent=${2}"
   echo $influx
}

health() {
   result=$(/usr/bin/snmpget -c ${2} -v 2c ${1} SNMPv2-SMI::mib-2.47.1.1.1.1.7.1 2> /dev/null)
   $DEBUG && echo "[DEBUG] SNMPGET ${hostname}:" $result

   if [[ $result =~ $regex2 ]]; then
      found=$(echo ${BASH_REMATCH[1]} | tr '[:upper:]' '[:lower:]')
      $DEBUG && echo "[DEBUG] MATCH ${found}"
      if [[ $hostname == $found ]]; then
         $DEBUG && echo "[DEBUG] RESULT ${hostname}: OK"
         status=1
      fi
   else
      $DEBUG && echo "[DEBUG] RESULT ${hostname}: FAIL"
      status=0
   fi

   storedata ${1} ${status}
}

if [[ ( "$1" == "-h" ) || ( "$#" -eq 4 ) ]]; then
   while getopts ":ha:s:c:" opt; do
      case $opt in
        # Help
        h)
          usage
          exit 1
          ;;
        # Get SNMP agent health status on vcenter list
        c)
          if [[ ! -z $OPTARG ]]; then
             community=$OPTARG
          else
             echo "[ERROR] -c was triggered, value is empty" >&2
             usage
             exit 1
          fi
          ;;
        a)
          vcsa=(${OPTARG//;/ })
          if [[ ! -z $vcsa ]]; then
             for elem in "${vcsa[@]}"; do
                if [[ $elem =~ $regex1 ]]; then
		   hostname=${BASH_REMATCH[1]}
                   $DEBUG && echo "[DEBUG] PROCESS ${hostname}"
		   health ${elem} ${community}
		fi
             done
          else
             echo "[ERROR] -a was triggered, value is empty" >&2
             usage
             exit 1
	  fi
          ;;
        # Get SNMP agent health status on a specific vcenter
        s)
          if [[ ! -z $OPTARG ]]; then
             if [[ $OPTARG =~ $regex1 ]]; then
	        hostname=${BASH_REMATCH[1]}
                $DEBUG && echo "[DEBUG] PROCESS ${hostname}"
                health ${OPTARG} ${community}
	     fi
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
   if [[ "$#" -ne 4 ]]; then
      echo "[ERROR] Illegal number of parameters"
      usage
      exit 1
   fi
fi
