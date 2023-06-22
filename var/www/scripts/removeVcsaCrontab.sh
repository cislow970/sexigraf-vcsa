#!/bin/bash
# added by Danilo Cilento <danilo.cilento@gmail.com>
crontabFile="/etc/cron.d/vcsa_$(sed s/\\./_/g <<<$1)"

sed -i '/"'"${1}"'"/d' /usr/lib/python3.8/vcsa_monitor/config.py

rm -f $crontabFile
rm -f /etc/telegraf/telegraf.d/input.${1}-ping.conf
rm -f /etc/telegraf/telegraf.d/input.${1}-devmapper.conf
rm -f /etc/telegraf/telegraf.d/input.${1}-sslcert.conf
rm -f /etc/telegraf/telegraf.d/input.${1}-sslcert_sts.conf
rm -f /etc/telegraf/telegraf.d/input.${1}-snmpv2c-cpu.conf
rm -f /etc/telegraf/telegraf.d/input.${1}-snmpv2c-network.conf
rm -f /etc/telegraf/telegraf.d/input.${1}-snmpv2c-snmpagent.conf
rm -f /etc/telegraf/telegraf.d/input.${1}-snmpv2c-storage.conf
rm -f /etc/telegraf/telegraf.d/input.${1}-snmpv2c-system.conf
rm -f /etc/telegraf/telegraf.d/input.${1}-snmpv3-cpu.conf
rm -f /etc/telegraf/telegraf.d/input.${1}-snmpv3-network.conf
rm -f /etc/telegraf/telegraf.d/input.${1}-snmpv3-snmpagent.conf
rm -f /etc/telegraf/telegraf.d/input.${1}-snmpv3-storage.conf
rm -f /etc/telegraf/telegraf.d/input.${1}-snmpv3-system.conf

service cron reload
systemctl restart telegraf.service
