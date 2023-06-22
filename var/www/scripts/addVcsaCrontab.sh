#!/bin/bash
# added by Danilo Cilento <danilo.cilento@gmail.com>
crontabFile="/etc/cron.d/vcsa_$(sed s/\\./_/g <<<$1)"

sed -i 's/"map_vcha_dummy": "Do not delete",/"map_vcha_dummy": "Do not delete",\n    "'"${1}"'": {"Primary": "'"${6}"'", "Secondary": "'"${7}"'", "Witness": "'"${8}"'"},/g' /usr/lib/python3.8/vcsa_monitor/config.py
sed -i 's/"check_list_dummy": "Do not delete",/"check_list_dummy": "Do not delete",\n    "'"${1}"'": [{"uptime": "--"}, {"health_load": "--"}, {"health_memory": "--"}, {"health_storage": "--"}, {"health_swap": "--"}, {"health_system": "--"}, {"health_softwarepackages": "--"}, {"health_databasestorage": "--"}, {"health_applmgmt": "--"}, {"cpu_util": "AVG"}, {"mem_usage": "AVG"}, {"systemload": "AVG"}, {"disk_readrate": "MAX"}, {"disk_writerate": "MAX"}, {"rx_activity_eth0": "MAX"}, {"tx_activity_eth0": "MAX"}, {"rx_packetRate_eth0": "MAX"}, {"tx_packetRate_eth0": "MAX"}, {"rx_drop_eth0": "MAX"}, {"tx_drop_eth0": "MAX"}, {"rx_error_eth0": "MAX"}, {"tx_error_eth0": "MAX"}, {"fs_root": "MAX"}, {"fs_boot": "MAX"}, {"fs_swap": "MAX"}, {"fs_core": "MAX"}, {"fs_log": "MAX"}, {"fs_db": "MAX"}, {"fs_dblog": "MAX"}, {"fs_seat": "MAX"}, {"fs_archive": "MAX"}, {"fs_updatemgr": "MAX"}, {"fs_imagebuilder": "MAX"}, {"fs_autodeploy": "MAX"}, {"fs_netdump": "MAX"}, {"fs_lifecycle": "MAX"}, {"fs_vtsdb": "MAX"}, {"fs_vtsdblog": "MAX"}, {"srvc_content-library": "--"}, {"srvc_pschealth": "--"}, {"srvc_vcha": "--"}, {"srvc_vmware-vpostgres": "--"}, {"srvc_vmware-postgres-archiver": "--"}, {"srvc_vpxd": "--"}, {"srvc_vsan-health": "--"}, {"srvc_vsphere-ui": "--"}, {"vcha_active_node": "--"}, {"vcha_health_cluster": "--"}],/g' /usr/lib/python3.8/vcsa_monitor/config.py

echo "*/1 * * * * root python3 -m vcsa_monitor --vcsa $1 --checklist --save 'influxdb' >/dev/null 2>&1" >> $crontabFile
echo "0 */1 * * * root python3 -m vcsa_monitor --vcsa $1 --method 'version' --save 'influxdb' >/dev/null 2>&1" >> $crontabFile
echo "0 */1 * * * root python3 -m vcsa_monitor --vcsa $1 --method 'content_library' --save 'influxdb' >/dev/null 2>&1" >> $crontabFile
echo "0 9,15 * * * root python3 -m vcsa_monitor --vcsa $1 --method 'available_updates' --save 'influxdb' >/dev/null 2>&1" >> $crontabFile
echo "0 9,15 * * * root python3 -m vcsa_monitor --vcsa $1 --method 'backup_status' --save 'influxdb' >/dev/null 2>&1" >> $crontabFile

if [ $2 != "none" ]; then
    cp -pv /etc/telegraf/templates/input.vcsa-ping.conf /etc/telegraf/telegraf.d/input.${1}-ping.conf
    cp -pv /etc/telegraf/templates/input.vcsa-devmapper.conf /etc/telegraf/telegraf.d/input.${1}-devmapper.conf
    cp -pv /etc/telegraf/templates/input.vcsa-sslcert.conf /etc/telegraf/telegraf.d/input.${1}-sslcert.conf
    cp -pv /etc/telegraf/templates/input.vcsa-sslcert_sts.conf /etc/telegraf/telegraf.d/input.${1}-sslcert_sts.conf
    cp -pv /etc/telegraf/templates/input.vcsa-snmpv2c-snmpagent.conf /etc/telegraf/telegraf.d/input.${1}-snmpv2c-snmpagent.conf
    cp -pv /etc/telegraf/templates/input.vcsa-snmpv2c-cpu.conf /etc/telegraf/telegraf.d/input.${1}-snmpv2c-cpu.conf
    cp -pv /etc/telegraf/templates/input.vcsa-snmpv2c-network.conf /etc/telegraf/telegraf.d/input.${1}-snmpv2c-network.conf
    cp -pv /etc/telegraf/templates/input.vcsa-snmpv2c-storage.conf /etc/telegraf/telegraf.d/input.${1}-snmpv2c-storage.conf
    cp -pv /etc/telegraf/templates/input.vcsa-snmpv2c-system.conf /etc/telegraf/telegraf.d/input.${1}-snmpv2c-system.conf

    sed -i 's/<VCSA_FQDN>/'${1}'/g' /etc/telegraf/telegraf.d/input.${1}-ping.conf
    sed -i 's/<VCSA_FQDN>/'${1}'/g' /etc/telegraf/telegraf.d/input.${1}-devmapper.conf
    sed -i 's/<VCSA_FQDN>/'${1}'/g' /etc/telegraf/telegraf.d/input.${1}-sslcert.conf
    sed -i 's/<VCSA_FQDN>/'${1}'/g' /etc/telegraf/telegraf.d/input.${1}-sslcert_sts.conf
    sed -i 's/<VCSA_FQDN>/'${1}'/g' /etc/telegraf/telegraf.d/input.${1}-snmpv2c-snmpagent.conf
    sed -i 's/<COMMUNITY_NAME>/'${2}'/g' /etc/telegraf/telegraf.d/input.${1}-snmpv2c-snmpagent.conf
    sed -i 's/<VCSA_FQDN>/'${1}'/g' /etc/telegraf/telegraf.d/input.${1}-snmpv2c-cpu.conf
    sed -i 's/<COMMUNITY_NAME>/'${2}'/g' /etc/telegraf/telegraf.d/input.${1}-snmpv2c-cpu.conf
    sed -i 's/<VCSA_FQDN>/'${1}'/g' /etc/telegraf/telegraf.d/input.${1}-snmpv2c-network.conf
    sed -i 's/<COMMUNITY_NAME>/'${2}'/g' /etc/telegraf/telegraf.d/input.${1}-snmpv2c-network.conf
    sed -i 's/<VCSA_FQDN>/'${1}'/g' /etc/telegraf/telegraf.d/input.${1}-snmpv2c-storage.conf
    sed -i 's/<COMMUNITY_NAME>/'${2}'/g' /etc/telegraf/telegraf.d/input.${1}-snmpv2c-storage.conf
    sed -i 's/<VCSA_FQDN>/'${1}'/g' /etc/telegraf/telegraf.d/input.${1}-snmpv2c-system.conf
    sed -i 's/<COMMUNITY_NAME>/'${2}'/g' /etc/telegraf/telegraf.d/input.${1}-snmpv2c-system.conf
fi

if [ $3 != "none" ]; then
    cp -pv /etc/telegraf/templates/input.vcsa-ping.conf /etc/telegraf/telegraf.d/input.${1}-ping.conf
    cp -pv /etc/telegraf/templates/input.vcsa-devmapper.conf /etc/telegraf/telegraf.d/input.${1}-devmapper.conf
    cp -pv /etc/telegraf/templates/input.vcsa-sslcert.conf /etc/telegraf/telegraf.d/input.${1}-sslcert.conf
    cp -pv /etc/telegraf/templates/input.vcsa-sslcert_sts.conf /etc/telegraf/telegraf.d/input.${1}-sslcert_sts.conf
    cp -pv /etc/telegraf/templates/input.vcsa-snmpv3-snmpagent.conf /etc/telegraf/telegraf.d/input.${1}-snmpv3-snmpagent.conf
    cp -pv /etc/telegraf/templates/input.vcsa-snmpv3-cpu.conf /etc/telegraf/telegraf.d/input.${1}-snmpv3-cpu.conf
    cp -pv /etc/telegraf/templates/input.vcsa-snmpv3-network.conf /etc/telegraf/telegraf.d/input.${1}-snmpv3-network.conf
    cp -pv /etc/telegraf/templates/input.vcsa-snmpv3-storage.conf /etc/telegraf/telegraf.d/input.${1}-snmpv3-storage.conf
    cp -pv /etc/telegraf/templates/input.vcsa-snmpv3-system.conf /etc/telegraf/telegraf.d/input.${1}-snmpv3-system.conf

    sed -i 's/<VCSA_FQDN>/'${1}'/g' /etc/telegraf/telegraf.d/input.${1}-ping.conf
    sed -i 's/<VCSA_FQDN>/'${1}'/g' /etc/telegraf/telegraf.d/input.${1}-devmapper.conf
    sed -i 's/<VCSA_FQDN>/'${1}'/g' /etc/telegraf/telegraf.d/input.${1}-sslcert.conf
    sed -i 's/<VCSA_FQDN>/'${1}'/g' /etc/telegraf/telegraf.d/input.${1}-sslcert_sts.conf
    sed -i 's/<VCSA_FQDN>/'${1}'/g' /etc/telegraf/telegraf.d/input.${1}-snmpv3-snmpagent.conf
    sed -i 's/<USERNAME>/'${3}'/g' /etc/telegraf/telegraf.d/input.${1}-snmpv3-snmpagent.conf
    sed -i 's/<SECRET_AUTH>/'${4}'/g' /etc/telegraf/telegraf.d/input.${1}-snmpv3-snmpagent.conf
    sed -i 's/<SECRET_PRIV>/'${5}'/g' /etc/telegraf/telegraf.d/input.${1}-snmpv3-snmpagent.conf
    sed -i 's/<VCSA_FQDN>/'${1}'/g' /etc/telegraf/telegraf.d/input.${1}-snmpv3-cpu.conf
    sed -i 's/<USERNAME>/'${3}'/g' /etc/telegraf/telegraf.d/input.${1}-snmpv3-cpu.conf
    sed -i 's/<SECRET_AUTH>/'${4}'/g' /etc/telegraf/telegraf.d/input.${1}-snmpv3-cpu.conf
    sed -i 's/<SECRET_PRIV>/'${5}'/g' /etc/telegraf/telegraf.d/input.${1}-snmpv3-cpu.conf
    sed -i 's/<VCSA_FQDN>/'${1}'/g' /etc/telegraf/telegraf.d/input.${1}-snmpv3-network.conf
    sed -i 's/<USERNAME>/'${3}'/g' /etc/telegraf/telegraf.d/input.${1}-snmpv3-network.conf
    sed -i 's/<SECRET_AUTH>/'${4}'/g' /etc/telegraf/telegraf.d/input.${1}-snmpv3-network.conf
    sed -i 's/<SECRET_PRIV>/'${5}'/g' /etc/telegraf/telegraf.d/input.${1}-snmpv3-network.conf
    sed -i 's/<VCSA_FQDN>/'${1}'/g' /etc/telegraf/telegraf.d/input.${1}-snmpv3-storage.conf
    sed -i 's/<USERNAME>/'${3}'/g' /etc/telegraf/telegraf.d/input.${1}-snmpv3-storage.conf
    sed -i 's/<SECRET_AUTH>/'${4}'/g' /etc/telegraf/telegraf.d/input.${1}-snmpv3-storage.conf
    sed -i 's/<SECRET_PRIV>/'${5}'/g' /etc/telegraf/telegraf.d/input.${1}-snmpv3-storage.conf
    sed -i 's/<VCSA_FQDN>/'${1}'/g' /etc/telegraf/telegraf.d/input.${1}-snmpv3-system.conf
    sed -i 's/<USERNAME>/'${3}'/g' /etc/telegraf/telegraf.d/input.${1}-snmpv3-system.conf
    sed -i 's/<SECRET_AUTH>/'${4}'/g' /etc/telegraf/telegraf.d/input.${1}-snmpv3-system.conf
    sed -i 's/<SECRET_PRIV>/'${5}'/g' /etc/telegraf/telegraf.d/input.${1}-snmpv3-system.conf
fi

service cron reload
systemctl restart telegraf.service
