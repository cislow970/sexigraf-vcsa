#!/bin/bash
#
# $Id vcsa_monitor_kill.sh v1.0.0 14/09/2020 <danilo.cilento@gmail.com> $
#
# Description: Kill vcsa_monitor processes running from long time
#
#


PID=$(ps -eo comm,pid,etimes | awk '/^python/ { if ($3 > 3600) { print $2 }}')
for id in $PID
do 
	timestamp=$(date +"%d-%m-%Y %H:%M:%S")
	echo "${timestamp} process with pid ${id}"
	check=$(ps $id | grep -i "vcsa_monitor" | grep -v grep)
	if [ -z "${check}" ]
	then
		echo "process is not vcsa_monitor"
	else
		echo "kill vcsa_monitor process running from long time"
		kill -9 $id
	fi
	echo --------------------
done
