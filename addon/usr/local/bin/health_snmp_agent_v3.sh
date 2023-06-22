#!/bin/bash
#
# $Id health_snmp_agent_v3.sh v1.1.0 15/12/2021 <danilo.cilento@gmail.com> $
#
# Description: Check status of the SNMP agent v3 on VCSA
#
#

DEBUG=false
regex1='^(\w+)((\.\w+){1,3})?'
regex2='^SNMPv2-MIB::sysName\.0\s=\sSTRING:\s(\w+)((\.\w+){1,3})?'

usage() {
   echo "Usage: $0 -u <snmp3 user> -p <authentication password> -t <privacy password> { -s <vcenter fqdn> | -a <vcenter fqdn list> }"
   echo "Examples:"
   echo "1) $0 -u \"monitor\" -p \"secretauth\" -t \"secretpriv\" -s \"vcenter1.local.intranet\""
   echo "2) $0 -u \"monitor\" -p \"secretauth\" -t \"secretpriv\" -a \"vcenter1.local.intranet;vcenter2.local.intranet;vcenter3.local.intranet\""
}

storedata() {
   influx="snmp_health,vcenter=${1} agent=${2}"
   echo $influx
}

health() {
   result=$(/usr/bin/snmpget -v3 -l authPriv -u ${2} -a SHA -A ${3} -x AES -X ${4} ${1} sysName.0 2> /dev/null)
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

if [[ ( "$1" == "-h" ) || ( "$#" -eq 8 ) ]]; then
   while getopts ":ha:s:u:p:t:" opt; do
      case $opt in
        # Help
        h)
          usage
          exit 1
          ;;
        # Get SNMP agent health status on vcenter list
        u)
          if [[ ! -z $OPTARG ]]; then
             username=$OPTARG
          else
             echo "[ERROR] -u was triggered, value is empty" >&2
             usage
             exit 1
          fi
          ;;
        p)
          if [[ ! -z $OPTARG ]]; then
             authpwd=$OPTARG
          else
             echo "[ERROR] -p was triggered, value is empty" >&2
             usage
             exit 1
          fi
          ;;
        t)
          if [[ ! -z $OPTARG ]]; then
             privpwd=$OPTARG
          else
             echo "[ERROR] -t was triggered, value is empty" >&2
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
		   health ${elem} ${username} ${authpwd} ${privpwd}
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
                health ${OPTARG} ${username} ${authpwd} ${privpwd}
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
   if [[ "$#" -ne 8 ]]; then
      echo "[ERROR] Illegal number of parameters"
      usage
      exit 1
   fi
fi
