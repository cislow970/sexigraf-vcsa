#!/bin/bash
#
# $Id health_sslcert_sts.sh v2.0.0 01/03/2023 <danilo.cilento@gmail.com> $
#
# Description: Check expiration date of the SSL Certificate binding to Security Token Service on vCenter
#
#


usage() {
   echo "Usage: $0 { -s <vcenter fqdn> | -a <vcenter fqdn list> }"
   echo "Examples:"
   echo "1) $0 -s \"vcenter1.local.intranet\""
   echo "2) $0 -a \"vcenter1.local.intranet;vcenter2.local.intranet;vcenter3.local.intranet\""
}

storedata() {
   influx=$result
   echo $influx
}

check_sts_cert() {
   result=$(/usr/bin/ssh -q -o StrictHostKeyChecking=accept-new -o ConnectTimeout=1 -o ConnectionAttempts=2 monitor@${vc} /usr/local/bin/checksts_sg.py ${vc})

   if [[ ! -z $result ]]; then
      storedata
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
        # Check STS certificate on vcenter list
        a)
          vcsa=(${OPTARG//;/ })
          if [[ ! -z $vcsa ]]; then
             for vc in "${vcsa[@]}"; do
                check_sts_cert ${vc}
             done
          else
             echo "[ERROR] -a was triggered, value is empty" >&2
             usage
             exit 1
          fi
          ;;
        # Check STS certificate on a specific vcenter
        s)
          if [[ ! -z $OPTARG ]]; then
	     vc=$OPTARG
             check_sts_cert ${vc}
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
