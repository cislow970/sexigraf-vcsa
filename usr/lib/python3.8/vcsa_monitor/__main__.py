"""
:Description:

This robot uses the methods exposed by the Rest API to monitor the VCSA.

:Usage:

python -m vcsa_monitor [-h|--help] [-v|--vcsa <FQDN VCSA>] [-u|--username <LOGIN USER>] [-p|--password <LOGIN PASSWORD>] [-m|--method <REST METHOD>] [-f|--function <METRIC FUNCTION>] [-c|--checklist] [-s|--save <BACKEND TYPE>] [-d|--debug] [-l|--log] [-r|--release]

    optional arguments::

        -h, --help                                          show this help message and exit
        -v <FQDN VCSA>, --vcsa <FQDN VCSA>                  name of a specific vCenter (fqdn)
        -u <LOGIN USER>, --username <LOGIN USER>            username for login on rest api
        -p <LOGIN PASSWORD>, --password <LOGIN PASSWORD>    password for login on rest api (encoded base64)
        -m <REST METHOD>, --method <REST METHOD>            call a specific method of rest api
        -f <METRIC FUNCTION>, --function <METRIC FUNCTION>  set a specific metric function
        -c, --checklist                                     gets metrics in check list
        -s <BACKEND TYPE>, --save <BACKEND TYPE>            store data to InfluxDB or Graphite time series database
        -d, --debug                                         enable debug
        -l, --log                                           enable log
        -r, --release                                       show robot release and exit

    - allowed values for method:

        version, uptime, health_load, health_memory, health_storage, health_swap,
        health_system, health_softwarepackages, health_databasestorage, health_applmgmt, cpu_util,
        mem_usage, systemload, disk_latencyrate, disk_readrate, disk_writerate,
        rx_activity_eth0, rx_activity_eth1, rx_packetRate_eth0, rx_packetRate_eth1,
        rx_drop_eth0, rx_drop_eth1, rx_error_eth0, rx_error_eth1, tx_activity_eth0,
        tx_activity_eth1, tx_packetRate_eth0, tx_packetRate_eth1, tx_drop_eth0, tx_drop_eth1,
        tx_error_eth0, tx_error_eth1, fs_root, fs_swap, fs_boot, fs_core, fs_log, fs_db,
        fs_dblog, fs_seat, fs_archive, fs_updatemgr, fs_imagebuilder, fs_autodeploy,
        fs_netdump, fs_lifecycle, fs_vtsdb, fs_vtsdblog, content_library, backup_status, srvc_all,
        srvc_content-library, srvc_pschealth, srvc_vcha, srvc_vmware-vpostgres, srvc_vmware-postgres-archiver,
        srvc_vpxd, srvc_vsan-health, srvc_vsphere-client, srvc_vsphere-ui, available_updates,
        vcha_active_node, vcha_health_cluster

    - allowed values for function:

        MIN, AVG, MAX

    - allowed values for save:

        influxdb, graphite

      [Warning: only numeric metrics are supported saving on Graphite]

:Examples:

- Get version::

    python -m vcsa_monitor --vcsa vcenter.local.intranet --username "monitor@vsphere.local"
    --password "xxxxxxxxxx" --method "version"

- Get uptime::

    python -m vcsa_monitor --vcsa vcenter.local.intranet --username "monitor@vsphere.local"
    --password "xxxxxxxxxx" --method "uptime"

- Get health load::

    python -m vcsa_monitor --vcsa vcenter.local.intranet --username "monitor@vsphere.local"
    --password "xxxxxxxxxx" --method "health_load"

- Get health memory::

    python -m vcsa_monitor --vcsa vcenter.local.intranet --username "monitor@vsphere.local"
    --password "xxxxxxxxxx" --method "health_memory"

- Get health storage::

    python -m vcsa_monitor --vcsa vcenter.local.intranet --username "monitor@vsphere.local"
    --password "xxxxxxxxxx" --method "health_storage"

- Get health swap::

    python -m vcsa_monitor --vcsa vcenter.local.intranet --username "monitor@vsphere.local"
    --password "xxxxxxxxxx" --method "health_swap"

- Get health system::

    python -m vcsa_monitor --vcsa vcenter.local.intranet --username "monitor@vsphere.local"
    --password "xxxxxxxxxx" --method "health_system"

- Get CPU usage::

    python -m vcsa_monitor --vcsa vcenter.local.intranet --username "monitor@vsphere.local"
    --password "xxxxxxxxxx" --method "cpu_util" --function "AVG"

- Get memory usage::

    python -m vcsa_monitor --vcsa vcenter.local.intranet --username "monitor@vsphere.local"
    --password "xxxxxxxxxx" --method "mem_usage" --function "AVG"

- Get system load per min::

    python -m vcsa_monitor --vcsa vcenter.local.intranet --username "monitor@vsphere.local"
    --password "xxxxxxxxxx" --method "systemload" --function "AVG"

- Get disk latency rate (dm-[0:10])::

    python -m vcsa_monitor --vcsa vcenter.local.intranet --username "monitor@vsphere.local"
    --password "xxxxxxxxxx" --method "disk_latencyrate" --function "MAX"

- Get disk read rate (dm-[0:10])::

    python -m vcsa_monitor --vcsa vcenter.local.intranet --username "monitor@vsphere.local"
    --password "xxxxxxxxxx" --method "disk_readrate" --function "MAX"

- Get disk write rate (dm-[0:10])::

    python -m vcsa_monitor --vcsa vcenter.local.intranet --username "monitor@vsphere.local"
    --password "xxxxxxxxxx" --method "disk_writerate" --function "MAX"

- Get ethernet interface eth0 bits received rate::

    python -m vcsa_monitor --vcsa vcenter.local.intranet --username "monitor@vsphere.local"
    --password "xxxxxxxxxx" --method "rx_activity_eth0" --function "MAX"

- Get ethernet interface eth0 bits transmitted rate::

    python -m vcsa_monitor --vcsa vcenter.local.intranet --username "monitor@vsphere.local"
    --password "xxxxxxxxxx" --method "tx_activity_eth0" --function "MAX"

- Get ethernet interface eth0 packets received rate::

    python -m vcsa_monitor --vcsa vcenter.local.intranet --username "monitor@vsphere.local"
    --password "xxxxxxxxxx" --method "rx_packetRate_eth0" --function "MAX"

- Get ethernet interface eth0 packets transmitted rate::

    python -m vcsa_monitor --vcsa vcenter.local.intranet --username "monitor@vsphere.local"
    --password "xxxxxxxxxx" --method "tx_packetRate_eth0" --function "MAX"

- Get ethernet interface eth0 drops received rate::

    python -m vcsa_monitor --vcsa vcenter.local.intranet --username "monitor@vsphere.local"
    --password "xxxxxxxxxx" --method "rx_drop_eth0" --function "MAX"

- Get ethernet interface eth0 drops transmitted rate::

    python -m vcsa_monitor --vcsa vcenter.local.intranet --username "monitor@vsphere.local"
    --password "xxxxxxxxxx" --method "tx_drop_eth0" --function "MAX"

- Get ethernet interface eth0 errors received rate::

    python -m vcsa_monitor --vcsa vcenter.local.intranet --username "monitor@vsphere.local"
    --password "xxxxxxxxxx" --method "rx_error_eth0" --function "MAX"

- Get ethernet interface eth0 errors transmitted rate::

    python -m vcsa_monitor --vcsa vcenter.local.intranet --username "monitor@vsphere.local"
    --password "xxxxxxxxxx" --method "tx_error_eth0" --function "MAX"

- Get ethernet interface eth1 bits received rate::

    python -m vcsa_monitor --vcsa vcenter.local.intranet --username "monitor@vsphere.local"
    --password "xxxxxxxxxx" --method "rx_activity_eth1" --function "MAX"

- Get ethernet interface eth1 bits transmitted rate::

    python -m vcsa_monitor --vcsa vcenter.local.intranet --username "monitor@vsphere.local"
    --password "xxxxxxxxxx" --method "tx_activity_eth1" --function "MAX"

- Get ethernet interface eth1 packets received rate::

    python -m vcsa_monitor --vcsa vcenter.local.intranet --username "monitor@vsphere.local"
    --password "xxxxxxxxxx" --method "rx_packetRate_eth1" --function "MAX"

- Get ethernet interface eth1 packets transmitted rate::

    python -m vcsa_monitor --vcsa vcenter.local.intranet --username "monitor@vsphere.local"
    --password "xxxxxxxxxx" --method "tx_packetRate_eth1" --function "MAX"

- Get ethernet interface eth1 drops received rate::

    python -m vcsa_monitor --vcsa vcenter.local.intranet --username "monitor@vsphere.local"
    --password "xxxxxxxxxx" --method "rx_drop_eth1" --function "MAX"

- Get ethernet interface eth1 drops transmitted rate::

    python -m vcsa_monitor --vcsa vcenter.local.intranet --username "monitor@vsphere.local"
    --password "xxxxxxxxxx" --method "tx_drop_eth1" --function "MAX"

- Get ethernet interface eth1 errors received rate::

    python -m vcsa_monitor --vcsa vcenter.local.intranet --username "monitor@vsphere.local"
    --password "xxxxxxxxxx" --method "rx_error_eth1" --function "MAX"

- Get ethernet interface eth1 errors transmitted rate::

    python -m vcsa_monitor --vcsa vcenter.local.intranet --username "monitor@vsphere.local"
    --password "xxxxxxxxxx" --method "tx_error_eth1" --function "MAX"

- Get filesystem root usage::

    python -m vcsa_monitor --vcsa vcenter.local.intranet --username "monitor@vsphere.local"
    --password "xxxxxxxxxx" --method "fs_root" --function "MAX"

- Get filesystem boot usage::

    python -m vcsa_monitor --vcsa vcenter.local.intranet --username "monitor@vsphere.local"
    --password "xxxxxxxxxx" --method "fs_boot" --function "MAX"

- Get filesystem swap usage::

    python -m vcsa_monitor --vcsa vcenter.local.intranet --username "monitor@vsphere.local"
    --password "xxxxxxxxxx" --method "fs_swap" --function "MAX"

- Get filesystem log usage::

    python -m vcsa_monitor --vcsa vcenter.local.intranet --username "monitor@vsphere.local"
    --password "xxxxxxxxxx" --method "fs_log" --function "MAX"

- Get filesystem db usage::

    python -m vcsa_monitor --vcsa vcenter.local.intranet --username "monitor@vsphere.local"
    --password "xxxxxxxxxx" --method "fs_db" --function "MAX"

- Get filesystem dblog usage::

    python -m vcsa_monitor --vcsa vcenter.local.intranet --username "monitor@vsphere.local"
    --password "xxxxxxxxxx" --method "fs_dblog" --function "MAX"

- Get filesystem seat usage::

    python -m vcsa_monitor --vcsa vcenter.local.intranet --username "monitor@vsphere.local"
    --password "xxxxxxxxxx" --method "fs_seat" --function "MAX"

- Get filesystem core usage::

    python -m vcsa_monitor --vcsa vcenter.local.intranet --username "monitor@vsphere.local"
    --password "xxxxxxxxxx" --method "fs_core" --function "MAX"

- Get filesystem archive usage::

    python -m vcsa_monitor --vcsa vcenter.local.intranet --username "monitor@vsphere.local"
    --password "xxxxxxxxxx" --method "fs_archive" --function "MAX"

- Get filesystem updatemgr usage::

    python -m vcsa_monitor --vcsa vcenter.local.intranet --username "monitor@vsphere.local"
    --password "xxxxxxxxxx" --method "fs_updatemgr" --function "MAX"

- Get filesystem imagebuilder usage::

    python -m vcsa_monitor --vcsa vcenter.local.intranet --username "monitor@vsphere.local"
    --password "xxxxxxxxxx" --method "fs_imagebuilder" --function "MAX"

- Get filesystem autodeploy usage::

    python -m vcsa_monitor --vcsa vcenter.local.intranet --username "monitor@vsphere.local"
    --password "xxxxxxxxxx" --method "fs_autodeploy" --function "MAX"

- Get filesystem netdump usage::

    python -m vcsa_monitor --vcsa vcenter.local.intranet --username "monitor@vsphere.local"
    --password "xxxxxxxxxx" --method "fs_netdump" --function "MAX"

- Get content library synchronization status::

    python -m vcsa_monitor --vcsa vcenter.local.intranet --username "monitor@vsphere.local"
    --password "xxxxxxxxxx" --method "content_library"

- Get latest backup status::

    python -m vcsa_monitor --vcsa vcenter.local.intranet --username "monitor@vsphere.local"
    --password "xxxxxxxxxx" --method "backup_status"

- Get health status of all services::

    python -m vcsa_monitor --vcsa vcenter.local.intranet --username "monitor@vsphere.local"
    --password "xxxxxxxxxx" --method "srvc_all"

- Get health status of content library service::

    python -m vcsa_monitor --vcsa vcenter.local.intranet --username "monitor@vsphere.local"
    --password "xxxxxxxxxx" --method "srvc_content-library"

- Get health status of psc service::

    python -m vcsa_monitor --vcsa vcenter.local.intranet --username "monitor@vsphere.local"
    --password "xxxxxxxxxx" --method "srvc_pschealth"

- Get health status of vcsa service::

    python -m vcsa_monitor --vcsa vcenter.local.intranet --username "monitor@vsphere.local"
    --password "xxxxxxxxxx" --method "srvc_vcha"

- Get health status of vpostgres service::

    python -m vcsa_monitor --vcsa vcenter.local.intranet --username "monitor@vsphere.local"
    --password "xxxxxxxxxx" --method "srvc_vmware-vpostgres"

- Get health status of vpostgres-archiver service::

    python -m vcsa_monitor --vcsa vcenter.local.intranet --username "monitor@vsphere.local"
    --password "xxxxxxxxxx" --method "srvc_vmware-postgres-archiver"

- Get health status of vpxd service::

    python -m vcsa_monitor --vcsa vcenter.local.intranet --username "monitor@vsphere.local"
    --password "xxxxxxxxxx" --method "srvc_vpxd"

- Get health status of vsan service::

    python -m vcsa_monitor --vcsa vcenter.local.intranet --username "monitor@vsphere.local"
    --password "xxxxxxxxxx" --method "srvc_vsan-health"

- Get health status of vsphere-client service::

    python -m vcsa_monitor --vcsa vcenter.local.intranet --username "monitor@vsphere.local"
    --password "xxxxxxxxxx" --method "srvc_vsphere-ui"

- Get updates available::

    python -m vcsa_monitor --vcsa vcenter.local.intranet --username "monitor@vsphere.local"
    --password "xxxxxxxxxx" --method "available_updates"

- Get vcha node active::

    python -m vcsa_monitor --vcsa vcenter.local.intranet --username "monitor@vsphere.local"
    --password "xxxxxxxxxx" --method "vcha_active_node"

- Get vcha health cluster::

    python -m vcsa_monitor --vcsa vcenter.local.intranet --username "monitor@vsphere.local"
    --password "xxxxxxxxxx" --method "vcha_health_cluster"
"""

import sys
import time
import logging
import datetime
from . import core
from . import config
from .authentication import authentication
from .backup import backup
from .content_library import content_library
from .cpu_mem import cpu_mem
from .database import database
from .disk import disk
from .health import health
from .network import network
from .storage import storage
from .system import uptime
from .system import version
from .updates import updates
from .vcha import vcha
from .vmon import vmon


# noinspection PyTypeChecker
def save_restapi_health(vcsa, status, save, log, debug):
    """
    Store rest api status

    :param vcsa: name of a specific vCenter (fqdn)
    :type vcsa: str
    :param status: status of the rest api
    :type status: int
    :param save: store data to database InfluxDB or Graphite
    :type save: str
    :param log: enable log to file
    :type log: bool
    :param debug: enable debug
    :type debug: bool
    """
    tsepoch = int(time.time())
    tsdt = datetime.datetime.utcfromtimestamp(tsepoch).strftime("%Y-%m-%dT%H:%M:%S.000Z")

    if save == "influxdb":
        # Store data to database InfluxDB
        data = {
            "status": status
        }
        database.store2influx(vcsa, "restapi_health", tsdt, data, log, debug)
    elif save == "graphite":
        # Store data to database Graphite
        database.store2graphite(vcsa, "restapi_health", tsepoch, "status", status, log, debug)


def rest_version(vcsa, token, save, log, debug):
    """
    Use rest method version and store result

    :param vcsa: name of a specific vCenter (fqdn)
    :type vcsa: str
    :param token: session id
    :type token: str
    :param save: store data to database InfluxDB or Graphite
    :type save: str
    :param log: enable log to file
    :type log: bool
    :param debug: enable debug
    :type debug: bool
    """
    result = version.get_version(vcsa, token, log, debug)
    tsepoch = result[0]
    product = result[1]
    release_date = result[2]
    release = result[3]
    build = result[4]
    type = result[5]

    if save == "influxdb":
        # Store data to database InfluxDB
        tsdt = datetime.datetime.utcfromtimestamp(tsepoch).strftime("%Y-%m-%dT%H:%M:%S.000Z")
        data = {
            "product": product,
            "release_date": release_date,
            "version": release,
            "build": build,
            "type": type
        }
        database.store2influx(vcsa, "version", tsdt, data, log, debug)
    elif save == "graphite":
        # Store data to database Graphite
        #database.store2graphite(vcsa, "version", tsepoch, "product", str(product), log, debug)
        #database.store2graphite(vcsa, "version", tsepoch, "release_date", str(release_date), log, debug)
        #database.store2graphite(vcsa, "version", tsepoch, "version", str(release), log, debug)
        #database.store2graphite(vcsa, "version", tsepoch, "build", str(build), log, debug)
        #database.store2graphite(vcsa, "version", tsepoch, "type", str(type), log, debug)
        if debug:
            print("[DEBUG] Graphite time series database does not support this type of metric!")
        if log:
            logging.error("Graphite time series database does not support this type of metric!")


def rest_uptime(vcsa, token, save, log, debug):
    """
    Use rest method uptime and store result

    :param vcsa: name of a specific vCenter (fqdn)
    :type vcsa: str
    :param token: session id
    :type token: str
    :param save: store data to database InfluxDB or Graphite
    :type save: str
    :param log: enable log to file
    :type log: bool
    :param debug: enable debug
    :type debug: bool
    """
    result = uptime.get_uptime(vcsa, token, log, debug)
    tsepoch = result[0]
    value = result[1]

    if save == "influxdb":
        # Store data to database InfluxDB
        tsdt = datetime.datetime.utcfromtimestamp(tsepoch).strftime("%Y-%m-%dT%H:%M:%S.000Z")
        data = {
            "days": value
        }
        database.store2influx(vcsa, "uptime", tsdt, data, log, debug)
    elif save == "graphite":
        # Store data to database Graphite
        database.store2graphite(vcsa, "uptime", tsepoch, "days", value, log, debug)


def rest_health(vcsa, token, method, save, log, debug):
    """
    Use rest method health and store result

    :param vcsa: name of a specific vCenter (fqdn)
    :type vcsa: str
    :param token: session id
    :type token: str
    :param method: set a specific method (value = load, mem, storage, swap, system, software-packages, database-storage)
    :type method: str
    :param save: store data to database InfluxDB or Graphite
    :type save: str
    :param log: enable log to file
    :type log: bool
    :param debug: enable debug
    :type debug: bool
    """
    result = None

    if method == "health_load":
        result = health.get_health(vcsa, token, "load", log, debug)
    elif method == "health_memory":
        result = health.get_health(vcsa, token, "mem", log, debug)
    elif method == "health_storage":
        result = health.get_health(vcsa, token, "storage", log, debug)
    elif method == "health_swap":
        result = health.get_health(vcsa, token, "swap", log, debug)
    elif method == "health_system":
        result = health.get_health(vcsa, token, "system", log, debug)
    elif method == "health_softwarepackages":
        result = health.get_health(vcsa, token, "software-packages", log, debug)
    elif method == "health_databasestorage":
        result = health.get_health(vcsa, token, "database-storage", log, debug)
    elif method == "health_applmgmt":
        result = health.get_health(vcsa, token, "applmgmt", log, debug)

    tsepoch = result[0]
    value = result[1]

    if save == "influxdb":
        # Store data to database InfluxDB
        tsdt = datetime.datetime.utcfromtimestamp(tsepoch).strftime("%Y-%m-%dT%H:%M:%S.000Z")
        data = {
            "status": value
        }
        database.store2influx(vcsa, method, tsdt, data, log, debug)
    elif save == "graphite":
        # Store data to database Graphite
        database.store2graphite(vcsa, method, tsepoch, "status", value, log, debug)


def rest_cpu_mem_usage(vcsa, token, method, function, save, log, debug):
    """
    Use rest method cpu/memory utilization and store result

    :param vcsa: name of a specific vCenter (fqdn)
    :type vcsa: str
    :param token: session id
    :type token: str
    :param method: set a specific method (value = cpu, memory)
    :type method: str
    :param function: set a specific metric function (value = MIN, AVG, MAX)
    :type function: str
    :param save: store data to database InfluxDB or Graphite
    :type save: str
    :param log: enable log to file
    :type log: bool
    :param debug: enable debug
    :type debug: bool
    """
    result = None

    if method == "cpu_util":
        result = cpu_mem.get_cpu_mem_usage(vcsa, token, "cpu", function, log, debug)
    elif method == "mem_usage":
        result = cpu_mem.get_cpu_mem_usage(vcsa, token, "memory", function, log, debug)

    tsepoch = result[0]
    value = result[1]

    if save == "influxdb":
        # Store data to database InfluxDB
        tsdt = datetime.datetime.utcfromtimestamp(tsepoch).strftime("%Y-%m-%dT%H:%M:%S.000Z")
        data = {
            "percent": value
        }
        database.store2influx(vcsa, method, tsdt, data, log, debug)
    elif save == "graphite":
        # Store data to database Graphite
        database.store2graphite(vcsa, method, tsepoch, "percent", value, log, debug)


def rest_systemload(vcsa, token, function, save, log, debug):
    """
    Use rest method systemload and store result

    :param vcsa: name of a specific vCenter (fqdn)
    :type vcsa: str
    :param token: session id
    :type token: str
    :param function: set a specific metric function (value = MIN, AVG, MAX)
    :type function: str
    :param save: store data to database InfluxDB or Graphite
    :type save: str
    :param log: enable log to file
    :type log: bool
    :param debug: enable debug
    :type debug: bool
    """
    result = cpu_mem.get_systemload(vcsa, token, function, log, debug)
    tsepoch = result[0]
    value = result[1]

    if save == "influxdb":
        # Store data to database InfluxDB
        tsdt = datetime.datetime.utcfromtimestamp(tsepoch).strftime("%Y-%m-%dT%H:%M:%S.000Z")
        data = {
            "load": value
        }
        database.store2influx(vcsa, "load_per_min", tsdt, data, log, debug)
    elif save == "graphite":
        # Store data to database Graphite
        database.store2graphite(vcsa, "system_load", tsepoch, "load_per_min", value, log, debug)


def rest_disk_performance(vcsa, token, method, function, save, log, debug):
    """
    Use rest method disk performance and store result

    :param vcsa: name of a specific vCenter (fqdn)
    :type vcsa: str
    :param token: session id
    :type token: str
    :param method: set a specific method (value = disk_latencyrate, disk_readrate, disk_writerate)
    :type method: str
    :param function: set a specific metric function (value = MIN, AVG, MAX)
    :type function: str
    :param save: store data to database InfluxDB or Graphite
    :type save: str
    :param log: enable log to file
    :type log: bool
    :param debug: enable debug
    :type debug: bool
    """
    result = disk.get_disk_performance(vcsa, token, method, function, log, debug)
    tsepoch = result[0]
    rate = result[1]

    if save == "influxdb":
        # Store data to database InfluxDB
        tsdt = datetime.datetime.utcfromtimestamp(tsepoch).strftime("%Y-%m-%dT%H:%M:%S.000Z")
        for key, value in rate.items():
            data = {
                "rate": value
            }
            database.store2influx(vcsa, key, tsdt, data, log, debug)
    elif save == "graphite":
        # Store data to database Graphite
        for key, value in rate.items():
            database.store2graphite(vcsa, method, tsepoch, key, value, log, debug)


def rest_network_performance(vcsa, token, method, function, save, log, debug):
    """
    Use rest method network performance and store result

    :param vcsa: name of a specific vCenter (fqdn)
    :type vcsa: str
    :param token: session id
    :type token: str
    :param method: set a specific method (value = rx_activity_eth0, rx_activity_eth1, rx_packetRate_eth0,
                                                  rx_packetRate_eth1, rx_drop_eth0, rx_drop_eth1, rx_error_eth0,
                                                  rx_error_eth1, tx_activity_eth0, tx_activity_eth1, tx_packetRate_eth0,
                                                  tx_packetRate_eth1, tx_drop_eth0, tx_drop_eth1, tx_error_eth0,
                                                  tx_error_eth1)
    :type method: str
    :param function: set a specific metric function (value = MIN, AVG, MAX)
    :type function: str
    :param save: store data to database InfluxDB or Graphite
    :type save: str
    :param log: enable log to file
    :type log: bool
    :param debug: enable debug
    :type debug: bool
    """
    result = network.get_network_performance(vcsa, token, method, function, log, debug)
    tsepoch = result[0]
    value = result[1]
    unit = result[2]

    if save == "influxdb":
        # Store data to database InfluxDB
        tsdt = datetime.datetime.utcfromtimestamp(tsepoch).strftime("%Y-%m-%dT%H:%M:%S.000Z")
        data = {
            unit: value
        }
        database.store2influx(vcsa, method, tsdt, data, log, debug)
    elif save == "graphite":
        # Store data to database Graphite
        database.store2graphite(vcsa, method, tsepoch, unit, value, log, debug)


def rest_filesystem_usage(vcsa, token, method, function, save, log, debug):
    """
    Use rest method filesystem usage and store data

    :param vcsa: name of a specific vCenter (fqdn)
    :type vcsa: str
    :param token: session id
    :type token: str
    :param method: set a specific method (value = fs_root, fs_swap, fs_boot, fs_core, fs_log, fs_db, fs_dblog,
                                                fs_seat, fs_archive, fs_updatemgr, fs_imagebuilder, fs_autodeploy,
                                                fs_netdump, fs_lifecycle, fs_vtsdb, fs_vtsdblog)
    :type method: str
    :param function: set a specific metric function (value = MIN, AVG, MAX)
    :type function: str
    :param save: store data to database InfluxDB or Graphite
    :type save: str
    :param log: enable log to file
    :type log: bool
    :param debug: enable debug
    :type debug: bool
    """
    result = storage.get_filesystem_usage(vcsa, token, method, function, log, debug)
    tsepoch = result[0]
    value = result[1]

    if save == "influxdb":
        # Store data to database InfluxDB
        tsdt = datetime.datetime.utcfromtimestamp(tsepoch).strftime("%Y-%m-%dT%H:%M:%S.000Z")
        data = {
            "percent": value
        }
        database.store2influx(vcsa, method, tsdt, data, log, debug)
    elif save == "graphite":
        # Store data to database Graphite
        database.store2graphite(vcsa, method, tsepoch, "percent", value, log, debug)


def rest_content_library(vcsa, token, save, log, debug):
    """
    Use rest method content library and store result

    :param vcsa: name of a specific vCenter (fqdn)
    :type vcsa: str
    :param token: session id
    :type token: str
    :param save: store data to database InfluxDB or Graphite
    :type save: str
    :param log: enable log to file
    :type log: bool
    :param debug: enable debug
    :type debug: bool
    """
    result = content_library.get_clib_sync(vcsa, token, log, debug)
    tsepoch = result[0]
    subscribed = result[1]
    not_sync = result[2]
    status = result[3]

    if subscribed:
        if len(not_sync) > 0:
            if debug:
                print("[DEBUG] There are libraries unsynchronized")
            if log:
                logging.debug("There are libraries unsynchronized")

            message = "There are libraries unsynchronized"
            libraries = ""
            for elem in result[2]:
                libraries += elem + ", "
            libraries = libraries[:-2]

            if save == "influxdb":
                # Store data to database InfluxDB
                tsdt = datetime.datetime.utcfromtimestamp(tsepoch).strftime("%Y-%m-%dT%H:%M:%S.000Z")
                data = {
                    "message": message,
                    "libraries": libraries,
                    "status": status
                }
                database.store2influx(vcsa, "clib_sync", tsdt, data, log, debug)
            elif save == "graphite":
                # Store data to database Graphite
                #database.store2graphite(vcsa, "clib_sync", tsepoch, "message", message, log, debug)
                #database.store2graphite(vcsa, "clib_sync", tsepoch, "libraries", libraries, log, debug)
                #database.store2graphite(vcsa, "clib_sync", tsepoch, "status", status, log, debug)
                if debug:
                    print("[DEBUG] Graphite time series database does not support this type of metric!")
                if log:
                    logging.error("Graphite time series database does not support this type of metric!")
        else:
            if debug:
                print("[DEBUG] All libraries are synchronized")
            if log:
                logging.debug("All libraries are synchronized")

            message = "All libraries are synchronized"
            libraries = "--"

            if save == "influxdb":
                # Store data to database InfluxDB
                tsdt = datetime.datetime.utcfromtimestamp(tsepoch).strftime("%Y-%m-%dT%H:%M:%S.000Z")
                data = {
                    "message": message,
                    "libraries": libraries,
                    "status": status
                }
                database.store2influx(vcsa, "clib_sync", tsdt, data, log, debug)
            elif save == "graphite":
                # Store data to database Graphite
                #database.store2graphite(vcsa, "clib_sync", tsepoch, "message", message, log, debug)
                #database.store2graphite(vcsa, "clib_sync", tsepoch, "libraries", libraries, log, debug)
                #database.store2graphite(vcsa, "clib_sync", tsepoch, "status", status, log, debug)
                if debug:
                    print("[DEBUG] Graphite time series database does not support this type of metric!")
                if log:
                    logging.error("Graphite time series database does not support this type of metric!")
    else:
        # There are no content library subscribed
        message = "There are no content libraries subscribed"
        libraries = "--"

        if save == "influxdb":
            # Store data to database InfluxDB
            tsdt = datetime.datetime.utcfromtimestamp(tsepoch).strftime("%Y-%m-%dT%H:%M:%S.000Z")
            data = {
                "message": message,
                "libraries": libraries,
                "status": status
            }
            database.store2influx(vcsa, "clib_sync", tsdt, data, log, debug)
        elif save == "graphite":
            # Store data to database Graphite
            #database.store2graphite(vcsa, "clib_sync", tsepoch, "message", message, log, debug)
            #database.store2graphite(vcsa, "clib_sync", tsepoch, "libraries", libraries, log, debug)
            #database.store2graphite(vcsa, "clib_sync", tsepoch, "status", status, log, debug)
            if debug:
                print("[DEBUG] Graphite time series database does not support this type of metric!")
            if log:
                logging.error("Graphite time series database does not support this type of metric!")


def rest_backup_status(vcsa, token, save, log, debug):
    """
    Use rest method backup status and store result

    :param vcsa: name of a specific vCenter (fqdn)
    :type vcsa: str
    :param token: session id
    :type token: str
    :param save: store data to database InfluxDB or Graphite
    :type save: str
    :param log: enable log to file
    :type log: bool
    :param debug: enable debug
    :type debug: bool
    """
    result = backup.get_backup_status(vcsa, token, log, debug)
    tsepoch = result[0]
    tot_job = result[1]
    job_status = result[2]
    job_type = result[3]
    job_start_time = result[4]
    job_end_time = result[5]
    job_size = result[6]

    job_aging = None

    if tot_job > 0:
        if debug:
            print("[DEBUG] There is a backup job")
        if log:
            logging.debug("There is a backup job")

        if job_status == "SUCCEEDED":
            datetimeFormat = '%Y-%m-%dT%H:%M:%S.%fZ'
            diff_time = datetime.datetime.fromtimestamp(tsepoch) - datetime.datetime.strptime(job_start_time, datetimeFormat)
            if diff_time.days < 1:
                job_aging = 0       # 0 = recent

                if debug:
                    print("[DEBUG] Backup aging: RECENT")
                if log:
                    logging.debug("Backup aging: RECENT")
            elif diff_time.days >= 1 and diff_time.days <= 3:
                job_aging = 1       # 1 = stale

                if debug:
                    print("[DEBUG] Backup aging: STALE")
                if log:
                    logging.debug("Backup aging: STALE")
            elif diff_time.days > 3:
                job_aging = 2       # 2 = old

                if debug:
                    print("[DEBUG] Backup aging: OLD")
                if log:
                    logging.debug("Backup aging: OLD")
        else:
            job_aging = 3           # 3 = error

            if debug:
                print("[DEBUG] Backup aging: ERROR")
            if log:
                logging.debug("Backup aging: ERROR")

        if save == "influxdb":
            # Store data to database InfluxDB
            tsdt = datetime.datetime.utcfromtimestamp(tsepoch).strftime("%Y-%m-%dT%H:%M:%S.000Z")
            data = {
                "job_status": job_status,
                "job_type": job_type,
                "job_start_time": (job_start_time[:-5]).replace("T", " "),
                "job_end_time": (job_end_time[:-5]).replace("T", " "),
                "job_size": job_size,
                "job_aging": job_aging
            }
            database.store2influx(vcsa, "backup_status", tsdt, data, log, debug)
        elif save == "graphite":
            # Store data to database Graphite
            #database.store2graphite(vcsa, "backup_status", tsepoch, "job_status", job_status, log, debug)
            #database.store2graphite(vcsa, "backup_status", tsepoch, "job_type", job_type, log, debug)
            #database.store2graphite(vcsa, "backup_status", tsepoch, "job_start_time", job_start_time[:-5], log, debug)
            #database.store2graphite(vcsa, "backup_status", tsepoch, "job_end_time", job_end_time[:-5], log, debug)
            #database.store2graphite(vcsa, "backup_status", tsepoch, "job_size", job_size, log, debug)
            #database.store2graphite(vcsa, "backup_status", tsepoch, "job_aging", job_aging, log, debug)
            if debug:
                print("[DEBUG] Graphite time series database does not support this type of metric!")
            if log:
                logging.error("Graphite time series database does not support this type of metric!")
    else:
        if debug:
            print("[DEBUG] There is no backup job")
        if log:
            logging.debug("There is no backup job")

        job_status = "ABSENT"
        job_type = "N/A"
        job_start_time = "N/A"
        job_end_time = "N/A"
        job_size = 0
        job_aging = -1

        if save == "influxdb":
            # Store data to database InfluxDB
            tsdt = datetime.datetime.utcfromtimestamp(tsepoch).strftime("%Y-%m-%dT%H:%M:%S.000Z")
            data = {
                "job_status": job_status,
                "job_type": job_type,
                "job_start_time": job_start_time,
                "job_end_time": job_end_time,
                "job_size": job_size,
                "job_aging": job_aging
            }
            database.store2influx(vcsa, "backup_status", tsdt, data, log, debug)
        elif save == "graphite":
            # Store data to database Graphite
            #database.store2graphite(vcsa, "backup_status", tsepoch, "job_status", job_status, log, debug)
            #database.store2graphite(vcsa, "backup_status", tsepoch, "job_type", job_type, log, debug)
            #database.store2graphite(vcsa, "backup_status", tsepoch, "job_start_time", job_start_time, log, debug)
            #database.store2graphite(vcsa, "backup_status", tsepoch, "job_end_time", job_end_time, log, debug)
            #database.store2graphite(vcsa, "backup_status", tsepoch, "job_size", job_size, log, debug)
            #database.store2graphite(vcsa, "backup_status", tsepoch, "job_aging", job_aging, log, debug)
            if debug:
                print("[DEBUG] Graphite time series database does not support this type of metric!")
            if log:
                logging.error("Graphite time series database does not support this type of metric!")


def rest_health_service(vcsa, token, method, save, log, debug):
    """
    Use rest method health service and store result

    :param vcsa: name of a specific vCenter (fqdn)
    :type vcsa: str
    :param token: session id
    :type token: str
    :param method: set a specific method (value = srvc_all, srvc_content-library, srvc_pschealth,
                                            srvc_vcha, srvc_vmware-vpostgres, srvc_vmware-postgres-archiver,
                                            srvc_vpxd, srvc_vsan-health, srvc_vsphere-client, srvc_vsphere-ui)
    :type method: str
    :param save: store data to database InfluxDB or Graphite
    :type save: str
    :param log: enable log to file
    :type log: bool
    :param debug: enable debug
    :type debug: bool
    """
    result = None

    if method == "srvc_all":
        result = vmon.get_health_service(vcsa, token, "ALL", log, debug)
    elif method == "srvc_content-library":
        result = vmon.get_health_service(vcsa, token, "content-library", log, debug)
    elif method == "srvc_pschealth":
        result = vmon.get_health_service(vcsa, token, "pschealth", log, debug)
    elif method == "srvc_vcha":
        result = vmon.get_health_service(vcsa, token, "vcha", log, debug)
    elif method == "srvc_vmware-vpostgres":
        result = vmon.get_health_service(vcsa, token, "vmware-vpostgres", log, debug)
    elif method == "srvc_vmware-postgres-archiver":
        result = vmon.get_health_service(vcsa, token, "vmware-postgres-archiver", log, debug)
    elif method == "srvc_vpxd":
        result = vmon.get_health_service(vcsa, token, "vpxd", log, debug)
    elif method == "srvc_vsan-health":
        result = vmon.get_health_service(vcsa, token, "vsan-health", log, debug)
    elif method == "srvc_vsphere-client":
        result = vmon.get_health_service(vcsa, token, "vsphere-client", log, debug)
    elif method == "srvc_vsphere-ui":
        result = vmon.get_health_service(vcsa, token, "vsphere-ui", log, debug)

    tsepoch = result[0]
    services = result[1]

    if save == "influxdb":
        # Store data to database InfluxDB
        tsdt = datetime.datetime.utcfromtimestamp(tsepoch).strftime("%Y-%m-%dT%H:%M:%S.000Z")
        for key, value in services.items():
            data = {
                "status": value
            }
            srvc_name = "srvc_" + key
            database.store2influx(vcsa, srvc_name, tsdt, data, log, debug)
    elif save == "graphite":
        # Store data to database Graphite
        for key, value in services.items():
            srvc_name = "srvc_" + key
            database.store2graphite(vcsa, srvc_name, tsepoch, "status", value, log, debug)


def rest_available_updates(vcsa, token, save, log, debug):
    """
    Use rest method available updates and store result

    :param vcsa: name of a specific vCenter (fqdn)
    :type vcsa: str
    :param token: session id
    :type token: str
    :param save: store data to database InfluxDB or Graphite
    :type save: str
    :param log: enable log to file
    :type log: bool
    :param debug: enable debug
    :type debug: bool
    """
    result = updates.get_available_updates(vcsa, token, log, debug)
    tsepoch = result[0]
    value = result[1]

    if save == "influxdb":
        # Store data to database InfluxDB
        tsdt = datetime.datetime.utcfromtimestamp(tsepoch).strftime("%Y-%m-%dT%H:%M:%S.000Z")
        data = {
            "updates": value
        }
        database.store2influx(vcsa, "available_updates", tsdt, data, log, debug)
    elif save == "graphite":
        # Store data to database Graphite
        database.store2graphite(vcsa, "available_updates", tsepoch, "updates", value, log, debug)


def rest_vcha_active_node(vcsa, token, save, log, debug):
    """
    Use rest method vcha active node and store result

    :param vcsa: name of a specific vCenter (fqdn)
    :type vcsa: str
    :param token: session id
    :type token: str
    :param save: store data to database InfluxDB or Graphite
    :type save: str
    :param log: enable log to file
    :type log: bool
    :param debug: enable debug
    :type debug: bool
    """
    result = vmon.get_health_service(vcsa, token, "vcha", log, debug)
    tsepoch = result[0]
    health_srvc = result[1]
    value = None

    if health_srvc["vcha"] == 3:  # Service STOPPED
        if debug:
            print("[DEBUG] Service VCHA is stopped!")
        if log:
            logging.debug("Service VCHA is stopped!")

        value = 3       # 1 = PRIMARY ONLINE, 2 = SECONDARY ONLINE, 3 = HA OFF

        if save == "influxdb":
            # Store data to database InfluxDB
            tsdt = datetime.datetime.utcfromtimestamp(tsepoch).strftime("%Y-%m-%dT%H:%M:%S.000Z")
            data = {
                "node": value
            }
            database.store2influx(vcsa, "vcha_active_node", tsdt, data, log, debug)
        elif save == "graphite":
            # Store data to database Graphite
            database.store2graphite(vcsa, "vcha_active_node", tsepoch, "node", value, log, debug)
    else:
        # Get VCHA active node (return value: IP of VCHA active node)
        result = vcha.get_vcha_active_node(vcsa, token, log, debug)
        tsepoch = result[0]
        vcha_config = result[1]
        ha_ip = result[2]

        if vcha_config == "present":
            found = False
            for key in config.map_vcha:
                if key == vcsa:
                    found = True
                    if debug:
                        print("[DEBUG] Heartbeat stored mapping for VCSA %s" % vcsa)
                        print("[DEBUG] Heartbeat IP of VCHA node 1 (Primary): %s" % config.map_vcha[key]["Primary"])
                        print("[DEBUG] Heartbeat IP of VCHA node 2 (Secondary): %s" % config.map_vcha[key]["Secondary"])
                        print("[DEBUG] Heartbeat IP of VCHA node 3 (Witness): %s" % config.map_vcha[key]["Witness"])

                    if log:
                        logging.debug("Heartbeat stored mapping for VCSA %s" % vcsa)
                        logging.debug("Heartbeat IP of VCHA node 1 (Primary): %s" % config.map_vcha[key]["Primary"])
                        logging.debug("Heartbeat IP of VCHA node 2 (Secondary): %s" % config.map_vcha[key]["Secondary"])
                        logging.debug("Heartbeat IP of VCHA node 3 (Witness): %s" % config.map_vcha[key]["Witness"])

                    if ha_ip == config.map_vcha[key]["Primary"]:
                        value = 1       # 1 = PRIMARY ONLINE, 2 = SECONDARY ONLINE, 3 = HA OFF

                        if debug:
                            print("[DEBUG] VCHA Node 1 (Primary) is now online!")
                        if log:
                            logging.debug("VCHA Node 1 (Primary) is now online!")

                    if ha_ip == config.map_vcha[key]["Secondary"]:
                        value = 2       # 1 = PRIMARY ONLINE, 2 = SECONDARY ONLINE, 3 = HA OFF

                        if debug:
                            print("[DEBUG] VCHA Node 2 (Secondary) is now online!")
                        if log:
                            logging.debug("VCHA Node 2 (Secondary) is now online!")

            if not found:
                if debug:
                    print("[ERROR] VCSA not found in heartbeat mapping!")

                if log:
                    logging.error("VCSA not found in heartbeat mapping!")

                sys.exit(1)
        elif vcha_config == "absent":
            value = 3               # 1 = PRIMARY ONLINE, 2 = SECONDARY ONLINE, 3 = HA OFF

        if save == "influxdb":
            # Store data to database InfluxDB
            tsdt = datetime.datetime.utcfromtimestamp(tsepoch).strftime("%Y-%m-%dT%H:%M:%S.000Z")
            data = {
                "node": value
            }
            database.store2influx(vcsa, "vcha_active_node", tsdt, data, log, debug)
        elif save == "graphite":
            # Store data to database Graphite
            database.store2graphite(vcsa, "vcha_active_node", tsepoch, "node", value, log, debug)


def rest_vcha_health_cluster(vcsa, token, save, log, debug):
    """
    Use rest method vcha health cluster and store result

    :param vcsa: name of a specific vCenter (fqdn)
    :type vcsa: str
    :param token: session id
    :type token: str
    :param save: store data to database InfluxDB or Graphite
    :type save: str
    :param log: enable log to file
    :type log: bool
    :param debug: enable debug
    :type debug: bool
    """
    result = vcha.get_vcha_health_cluster(vcsa, token, log, debug)
    tsepoch = result[0]
    config_state = result[1]
    cluster_mode = result[2]
    health_state = result[3]
    manual_failover_allowed = result[4]
    auto_failover_allowed = result[5]
    health_warnings = result[6]
    primary_role = result[7]
    secondary_role = result[8]
    primary_state = result[9]
    secondary_state = result[10]
    witness_state = result[11]

    if config_state == "NOTCONFIGURED" or config_state == "--":
        cluster_mode = 3                    # 0 = ENABLED, 1 = MAINTENANCE, 2 = DISABLED, 3 = NOT_CONFIGURED
        health_state = 3                    # 0 = HEALTHY, 1 = HEALTHY_WITH_WARNINGS, 2 = DEGRADED, 3 = NOT_CONFIGURED
        manual_failover_allowed = 2         # UNDEFINED FAILOVER: manual_failover_allowed = 2, auto_failover_allowed = 2
        auto_failover_allowed = 2           # UNDEFINED FAILOVER: manual_failover_allowed = 2, auto_failover_allowed = 2
        primary_role = 2                    # UNDEFINED ROLE: primary_role = 2, secondary_role = 2
        secondary_role = 2                  # UNDEFINED ROLE: primary_role = 2, secondary_role = 2
        primary_state = 2                   # UNDEFINED STATE: primary_state = 2, secondary_state = 2, witness_state = 2
        secondary_state = 2                 # UNDEFINED STATE: primary_state = 2, secondary_state = 2, witness_state = 2
        witness_state = 2                   # UNDEFINED STATE: primary_state = 2, secondary_state = 2, witness_state = 2

    elif config_state == "CONFIGURED":
        if cluster_mode == "ENABLED":
            cluster_mode = 0
        elif cluster_mode == "MAINTENANCE":
            cluster_mode = 1
        elif cluster_mode == "DISABLED":
            cluster_mode = 2

        if health_state == "HEALTHY":
            health_state = 0
        elif health_state == "HEALTHY_WITH_WARNINGS":
            health_state = 1
        elif health_state == "DEGRADED":
            health_state = 2

        manual_failover_allowed = int(manual_failover_allowed == True)
        auto_failover_allowed = int(auto_failover_allowed == True)

        if primary_role == "ACTIVE":
            primary_role = 1
        elif primary_role == "PASSIVE":
            primary_role = 0

        if secondary_role == "ACTIVE":
            secondary_role = 1
        elif secondary_role == "PASSIVE":
            secondary_role = 0

        if primary_state == "UP":
            primary_state = 1
        elif primary_state == "DOWN":
            primary_state = 0

        if secondary_state == "UP":
            secondary_state = 1
        elif secondary_state == "DOWN":
            secondary_state = 0

        if witness_state == "UP":
            witness_state = 1
        elif witness_state == "DOWN":
            witness_state = 0

    if save == "influxdb":
        # Store data to database InfluxDB
        tsdt = datetime.datetime.utcfromtimestamp(tsepoch).strftime("%Y-%m-%dT%H:%M:%S.000Z")
        data = {
                "cluster_mode": cluster_mode,
                "health_state": health_state,
                "manual_failover_allowed": manual_failover_allowed,
                "auto_failover_allowed": auto_failover_allowed,
                "primary_role": primary_role,
                "secondary_role": secondary_role,
                "primary_state": primary_state,
                "secondary_state": secondary_state,
                "witness_state": witness_state
        }
        database.store2influx(vcsa, "vcha_health_cluster", tsdt, data, log, debug)
    elif save == "graphite":
        # Store data to database Graphite
        database.store2graphite(vcsa, "vcha_health_cluster", tsepoch, "cluster_mode", cluster_mode, log, debug)
        database.store2graphite(vcsa, "vcha_health_cluster", tsepoch, "health_state", health_state, log, debug)
        database.store2graphite(vcsa, "vcha_health_cluster", tsepoch, "manual_failover_allowed", manual_failover_allowed, log, debug)
        database.store2graphite(vcsa, "vcha_health_cluster", tsepoch, "auto_failover_allowed", auto_failover_allowed, log, debug)
        database.store2graphite(vcsa, "vcha_health_cluster", tsepoch, "primary_role", primary_role, log, debug)
        database.store2graphite(vcsa, "vcha_health_cluster", tsepoch, "secondary_role", secondary_role, log, debug)
        database.store2graphite(vcsa, "vcha_health_cluster", tsepoch, "primary_state", primary_state, log, debug)
        database.store2graphite(vcsa, "vcha_health_cluster", tsepoch, "secondary_state", secondary_state, log, debug)
        database.store2graphite(vcsa, "vcha_health_cluster", tsepoch, "witness_state", witness_state, log, debug)

    if health_warnings != "--":
        if debug:
            print("[WARNING] There are warning messages!")

        if log:
            logging.warning("There are warning messages!")

        count = 0
        for elem in health_warnings:
            try:
                message = elem["error"]["default_message"]
            except:
                message = "--"

            try:
                additional_information = elem["recommendation"]["default_message"]
            except:
                additional_information = "--"

            if debug:
                print("[DEBUG] Message: %s" % message)
                print("[DEBUG] Additional Information: %s" % additional_information)
            if log:
                logging.debug("Message: %s" % message)
                logging.debug("Additional Information: %s" % additional_information)

            tsepoch += count
            if save == "influxdb":
                # Store data to database InfluxDB
                tsdt = datetime.datetime.utcfromtimestamp(tsepoch).strftime("%Y-%m-%dT%H:%M:%S.000Z")
                data = {
                    "message": message,
                    "additional_information": additional_information
                }
                database.store2influx(vcsa, "vcha_cluster_message", tsdt, data, log, debug)
            elif save == "graphite":
                # Store data to database Graphite
                #database.store2graphite(vcsa, "vcha_cluster_message", tsepoch, "message", message, log, debug)
                #database.store2graphite(vcsa, "vcha_cluster_message", tsepoch, "additional_information", additional_information, log, debug)
                if debug:
                    print("[DEBUG] Graphite time series database does not support this type of metric!")
                if log:
                    logging.error("Graphite time series database does not support this type of metric!")

            count += 1
    else:
        if debug:
            print("[DEBUG] There are no warning messages")

        if log:
            logging.debug("There are no warning messages")


def call_method(vcsa, token, method, function, save, log, debug):
    """
    Call method to get a specific metric

    :param vcsa: name of a specific vCenter (fqdn)
    :type vcsa: str
    :param token: session id
    :type token: str
    :param method: set a specific method
    :type method: str
    :param function: set a specific metric function
    :type function: str
    :param save: store data to database
    :type save: bool
    :param log: enable log to file
    :type log: bool
    :param debug: enable debug
    :type debug: bool
    """
    if method == "version":
        rest_version(vcsa, token, save, log, debug)
    elif method == "uptime":
        rest_uptime(vcsa, token, save, log, debug)
    elif method == "health_load" or method == "health_memory" or method == "health_storage"\
            or method == "health_swap" or method == "health_system" or method == "health_softwarepackages"\
            or method == "health_databasestorage" or method == "health_applmgmt":
        rest_health(vcsa, token, method, save, log, debug)
    elif method == "cpu_util" or method == "mem_usage":
        rest_cpu_mem_usage(vcsa, token, method, function, save, log, debug)
    elif method == "systemload":
        rest_systemload(vcsa, token, function, save, log, debug)
    elif method == "disk_latencyrate" or method == "disk_readrate" or method == "disk_writerate":
        rest_disk_performance(vcsa, token, method, function, save, log, debug)
    elif method == "rx_activity_eth0" or method == "rx_activity_eth1" or method == "rx_packetRate_eth0"\
            or method == "rx_packetRate_eth1" or method == "rx_drop_eth0" or method == "rx_drop_eth1"\
            or method == "rx_error_eth0" or method == "rx_error_eth1" or method == "tx_activity_eth0"\
            or method == "tx_activity_eth1" or method == "tx_packetRate_eth0" or method == "tx_packetRate_eth1"\
            or method == "tx_drop_eth0" or method == "tx_drop_eth1" or method == "tx_error_eth0"\
            or method == "tx_error_eth1":
        rest_network_performance(vcsa, token, method, function, save, log, debug)
    elif method == "fs_root" or method == "fs_swap" or method == "fs_boot" or method == "fs_core"\
            or method == "fs_log" or method == "fs_db" or method == "fs_dblog" or method == "fs_seat"\
            or method == "fs_archive" or method == "fs_updatemgr" or method == "fs_imagebuilder"\
            or method == "fs_autodeploy" or method == "fs_netdump" or method == "fs_lifecycle"\
            or method == "fs_vtsdb" or method == "fs_vtsdblog":
        rest_filesystem_usage(vcsa, token, method, function, save, log, debug)
    elif method == "content_library":
        rest_content_library(vcsa, token, save, log, debug)
    elif method == "backup_status":
        rest_backup_status(vcsa, token, save, log, debug)
    elif method == "srvc_all" or method == "srvc_content-library" or method == "srvc_pschealth"\
            or method == "srvc_vcha" or method == "srvc_vmware-vpostgres" or method == "srvc_vmware-postgres-archiver"\
            or method == "srvc_vpxd" or method == "srvc_vsan-health" or method == "srvc_vsphere-client"\
            or method == "srvc_vsphere-ui":
        rest_health_service(vcsa, token, method, save, log, debug)
    elif method == "available_updates":
        rest_available_updates(vcsa, token, save, log, debug)
    elif method == "vcha_active_node":
        rest_vcha_active_node(vcsa, token, save, log, debug)
    elif method == "vcha_health_cluster":
        rest_vcha_health_cluster(vcsa, token, save, log, debug)


# Main
def main():
    arguments = core.options()

    vcsa = arguments[0]
    username = arguments[1]
    password = arguments[2]
    method = arguments[3]
    function = arguments[4]
    checklist = arguments[5]
    save = arguments[6]
    debug = arguments[7]
    log = arguments[8]

    if checklist:
        try:
            if config.check_list[vcsa]:
                if debug:
                    print("[DEBUG] VCSA have the definition of the checklist.")

                if log:
                    logging.info("VCSA have the definition of the checklist.")
        except:
            if debug:
                print("[DEBUG] VCSA does not have the definition of the checklist. " \
                      "Add the definition in the 'config.py' file, to the 'check_list' variable.")
            if log:
                logging.error("VCSA does not have the definition of the checklist.")
                logging.error("Add the definition in the 'config.py' file, to the 'check_list' variable.")
                logging.info("-- Finish --------------------------------------------------------")

            sys.exit(1)

        # Get token session
        session_id = authentication.get_session(vcsa, username, password, log, debug)

        if session_id == "failed":
            if debug:
                print("[DEBUG] REST API Status: FAILED")
            if log:
                logging.error("REST API Status: FAILED")
            if save:
                save_restapi_health(vcsa, 0, save, log, debug)        # status = 0 (FAILED)
            if log:
                logging.info("-- Finish --------------------------------------------------------")

            sys.exit(1)
        else:
            if debug:
                print("[DEBUG] REST API Status: OK")
            if log:
                logging.debug("REST API Status: OK")
            if save:
                save_restapi_health(vcsa, 1, save, log, debug)        # status = 1 (OK)

        for appliance in config.check_list:
            if appliance == vcsa:
                for elem in config.check_list[appliance]:
                    keys_list = list(elem.keys())
                    method = keys_list[0]
                    function = elem[method]
                    call_method(vcsa, session_id, method, function, save, log, debug)

        # Delete token session
        authentication.del_session(vcsa, session_id, log, debug)

        if log:
            logging.info("-- Finish --------------------------------------------------------")
    else:
        # Get token session
        session_id = authentication.get_session(vcsa, username, password, log, debug)

        if session_id == "failed":
            if debug:
                print("[DEBUG] REST API Status: FAILED")
            if log:
                logging.error("REST API Status: FAILED")
            if save:
                save_restapi_health(vcsa, 0, save, log, debug)        # status = 0 (FAILED)
            if log:
                logging.info("-- Finish --------------------------------------------------------")

            sys.exit(1)
        else:
            if debug:
                print("[DEBUG] REST API Status: OK")
            if log:
                logging.debug("REST API Status: OK")
            if save:
                save_restapi_health(vcsa, 1, save, log, debug)        # status = 1 (OK)

        call_method(vcsa, session_id, method, function, save, log, debug)

        # Delete token session
        authentication.del_session(vcsa, session_id, log, debug)

        if log:
            logging.info("-- Finish --------------------------------------------------------")


if __name__ == "__main__":
    main()
