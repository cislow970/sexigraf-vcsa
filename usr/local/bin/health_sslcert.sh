#!/bin/bash
#
# $Id health_sslcert.sh v1.0.0 26/05/2021 <danilo.cilento@gmail.com> $
#
# Description: Check expiration date of the SSL Certificate on vCenter
#
#


DEBUG=false
warning_days=30         # Number of days to warn about soon-to-expire certs
port=443		# TCP port for SSL check

usage() {
   echo "Usage: $0 { -s <vcenter fqdn> | -a <vcenter fqdn list> }"
   echo "Examples:"
   echo "1) $0 -s \"vcenter1.local.intranet\""
   echo "2) $0 -a \"vcenter1.local.intranet;vcenter2.local.intranet;vcenter3.local.intranet\""
}

storedata() {
   influx="sslcert_health,vcenter=${1} expiry=${2},subject=\"${3}\",issuer=\"${4}\""
   echo $influx
}

health() {
   SERVICE="${1}:${2}"
   $DEBUG && echo "[DEBUG] Checking cert: [$SERVICE]"

   certificate=$(echo | openssl s_client -connect ${SERVICE} 2>/dev/null |\
   sed -ne '/-BEGIN CERTIFICATE-/,/-END CERTIFICATE-/p')

   if [ "$?" -ne 0 ]; then
     $DEBUG && echo "[DEBUG] Error connecting to ${SERVICE} for verify SSL Certificate"
     logger -p local6.warn "Error connecting to ${SERVICE} for verify SSL Certificate"
   else
     output=$(echo | openssl s_client -connect ${SERVICE} 2>/dev/null |\
     sed -ne '/-BEGIN CERTIFICATE-/,/-END CERTIFICATE-/p' |\
     openssl x509 -noout -subject -issuer -dates 2>/dev/null)

     subject=$(echo $output | sed 's/.*subject=\(.*\).*issuer.*not.*/\1/g' | xargs)
     issuer=$(echo $output | sed 's/.*issuer=\(.*\).*not.*not.*/\1/g' | xargs)
     start_date=$(echo $output | sed 's/.*notBefore=\(.*\).*not.*/\1/g')
     end_date=$(echo $output | sed 's/.*notAfter=\(.*\)$/\1/g')

     $DEBUG && echo "[DEBUG] Subject =" $subject
     $DEBUG && echo "[DEBUG] Issuer =" $issuer
     $DEBUG && echo "[DEBUG] Warning Days =" $warning_days
     $DEBUG && echo "[DEBUG] Start Date =" $start_date
     $DEBUG && echo "[DEBUG] End Date =" $end_date

     start_epoch=$(date +%s -d "$start_date")
     end_epoch=$(date +%s -d "$end_date")

     $DEBUG && echo "[DEBUG] Epoch Start =" $start_epoch
     $DEBUG && echo "[DEBUG] Epoch End =" $end_epoch

     epoch_now=$(date +%s)

     $DEBUG && echo "[DEBUG] Epoch Now =" $epoch_now

     # Check if start date of the SSL Certificate is later to current date
     if [ "$start_epoch" -gt "$epoch_now" ]; then
       $DEBUG && echo "[DEBUG] Start date of the SSL Certificate for ${SERVICE} is later to current date. SSL Certificate is not yet valid."
       logger -p local6.warn "Start date of the SSL Certificate for ${SERVICE} is later to current date. SSL Certificate is not yet valid."
     fi

     seconds_to_expire=$(($end_epoch - $epoch_now))
     days_to_expire=$(($seconds_to_expire / 86400))

     $DEBUG && echo "[DEBUG] Days to expiry: ${days_to_expire}"

     if [ "$days_to_expire" -lt "$warning_days" ] && [ "$days_to_expire" -gt "0" ]; then
       $DEBUG && echo "[DEBUG] SSL Certificate for ${SERVICE} is soon to expire"
       logger -p local6.warn "SSL Certificate for ${SERVICE} is soon to expire"
     fi

     if [ "$days_to_expire" -le "0" ]; then
       $DEBUG && echo "[DEBUG] SSL Certificate for ${SERVICE} is expired"
       logger -p local6.warn "SSL Certificate for ${SERVICE} is expired"
     fi

     storedata ${1} ${days_to_expire} "${subject}" "${issuer}"
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
        # Check date to expiry of the SSL Certificate on vcenter list
        a)
          vcsa=(${OPTARG//;/ })
          if [[ ! -z $vcsa ]]; then
             for elem in "${vcsa[@]}"; do
                health ${elem} ${port}
             done
          else
             echo "[ERROR] -a was triggered, value is empty" >&2
             usage
             exit 1
          fi
          ;;
        # Check date to expiry of the SSL Certificate on a specific vcenter
        s)
          if [[ ! -z $OPTARG ]]; then
             health ${OPTARG} ${port}
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

