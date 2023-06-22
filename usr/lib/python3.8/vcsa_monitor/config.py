# Owned
__project__ = "vcsa_monitor"
__author__ = "Danilo Cilento"
__copyright__ = "Copyright 2020-2023"
__license__ = "GPL v3.0"
__version__ = "2.0.0"
__date__ = "10/10/2022"
__email__ = "<danilo.cilento@gmail.com>"
__status__ = "stable"

# InfluxDB Connection
influxdb_host = "localhost"
influxdb_port = 8086
influxdb_repo = "vcsa_rest"
influxdb_user = "pollerpy"
influxdb_pwd = "p0ll3rpy"

# Grphite Connection
graphite_host = "localhost"
graphite_port = 2003
graphite_basepath = "vcsa.rest"

# SexiGraf repository VI credentials
repo_creds = "/mnt/wfs/inventory/vipscredentials.xml"

# Mapping VCHA
map_vcha = {
    "map_vcha_dummy": "Do not delete",
    "vcenter67.example.intranet": {"Primary": "10.10.20.1", "Secondary": "10.10.20.2", "Witness": "10.10.20.3"},
}

# Check list
check_list = {
    "check_list_dummy": "Do not delete",
    "vcenter67.example.intranet": [{"uptime": "--"},{"health_load": "--"},{"health_memory": "--"},{"health_storage": "--"},{"health_swap": "--"}, {"health_system": "--"}, {"health_softwarepackages": "--"}, {"health_databasestorage": "--"}, {"cpu_util": "AVG"}, {"mem_usage": "AVG"}, {"systemload": "AVG"}, {"disk_readrate": "MAX"}, {"disk_writerate": "MAX"}, {"rx_activity_eth0": "MAX"}, {"tx_activity_eth0": "MAX"}, {"rx_packetRate_eth0": "MAX"}, {"tx_packetRate_eth0": "MAX"}, {"rx_drop_eth0": "MAX"}, {"tx_drop_eth0": "MAX"}, {"rx_error_eth0": "MAX"}, {"tx_error_eth0": "MAX"}, {"fs_root": "MAX"}, {"fs_boot": "MAX"}, {"fs_swap": "MAX"}, {"fs_core": "MAX"}, {"fs_log": "MAX"}, {"fs_db": "MAX"}, {"fs_dblog": "MAX"}, {"fs_seat": "MAX"}, {"fs_archive": "MAX"}, {"fs_updatemgr": "MAX"}, {"fs_imagebuilder": "MAX"}, {"fs_autodeploy": "MAX"}, {"fs_netdump": "MAX"}, {"srvc_all": "--"}, {"vcha_active_node": "--"}, {"vcha_health_cluster": "--"}],
}
