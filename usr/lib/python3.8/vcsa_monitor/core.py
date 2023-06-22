import sys
import logging
import base64
import xml.etree.ElementTree as ET
from argparse import ArgumentParser
from . import config


def logger(path):
    """
    Create a logger object to file

    :param path: log file path
    :type path: str
    :returns: logger object
    :rtype: logging
    """
    logging.basicConfig(format='%(asctime)s.%(msecs)03d %(levelname)s\t%(message)s', datefmt='%d/%m/%Y %H:%M:%S', filename=path, level=logging.DEBUG)


def options():
    """
    Define command line arguments and help

    :returns: arguments list
    :rtype: str, bool
    """
    parser = ArgumentParser()

    # Command line options
    parser.add_argument("-v",
                        "--vcsa",
                        dest="vcsa",
                        help="name of a specific vcsa (fqdn)",
                        metavar="<FQDN VCSA>"
                        )
    parser.add_argument("-u",
                        "--username",
                        dest="username",
                        help="username for login on rest api",
                        metavar="<LOGIN USER>"
                        )
    parser.add_argument("-p",
                        "--password",
                        dest="password",
                        help="password for login on rest api (encoded base64)",
                        metavar="<LOGIN PASSWORD>"
                        )
    parser.add_argument("-m",
                        "--method",
                        dest="method",
                        choices=['version',
                                 'uptime',
                                 'health_load',
                                 'health_memory',
                                 'health_storage',
                                 'health_swap',
                                 'health_system',
                                 'health_softwarepackages',
                                 'health_databasestorage',
                                 'health_applmgmt',
                                 'mem_usage',
                                 'cpu_util',
                                 'systemload',
                                 'fs_root',
                                 'fs_swap',
                                 'fs_boot',
                                 'fs_core',
                                 'fs_log',
                                 'fs_db',
                                 'fs_dblog',
                                 'fs_seat',
                                 'fs_archive',
                                 'fs_updatemgr',
                                 'fs_imagebuilder',
                                 'fs_autodeploy',
                                 'fs_netdump',
                                 'fs_lifecycle',
                                 'fs_vtsdb',
                                 'fs_vtsdblog',
                                 'disk_latencyrate',
                                 'disk_readrate',
                                 'disk_writerate',
                                 'rx_activity_eth0',
                                 'rx_activity_eth1',
                                 'rx_packetRate_eth0',
                                 'rx_packetRate_eth1',
                                 'rx_drop_eth0',
                                 'rx_drop_eth1',
                                 'rx_error_eth0',
                                 'rx_error_eth1',
                                 'tx_activity_eth0',
                                 'tx_activity_eth1',
                                 'tx_packetRate_eth0',
                                 'tx_packetRate_eth1',
                                 'tx_drop_eth0',
                                 'tx_drop_eth1',
                                 'tx_error_eth0',
                                 'tx_error_eth1',
                                 'content_library',
                                 'backup_status',
                                 'srvc_all',
                                 'srvc_content-library',
                                 'srvc_pschealth',
                                 'srvc_vcha',
                                 'srvc_vmware-vpostgres',
                                 'srvc_vmware-postgres-archiver',
                                 'srvc_vpxd',
                                 'srvc_vsan-health',
                                 'srvc_vsphere-client',
                                 'srvc_vsphere-ui',
                                 'available_updates',
                                 'vcha_active_node',
                                 'vcha_health_cluster'],
                        help="call a specific method of rest api",
                        metavar="<REST METHOD>"
                        )
    parser.add_argument("-f",
                        "--function",
                        dest="function",
                        choices=['MIN', 'AVG', 'MAX'],
                        help="set a specific metric function",
                        metavar="<METRIC FUNCTION>"
                        )
    parser.add_argument("-c",
                        "--checklist",
                        action="store_true",
                        dest="checklist",
                        help="gets metrics in check list"
                        )
    parser.add_argument("-s",
                        "--save",
			dest="save",
			choices=['influxdb', 'graphite'],
                        help="store data to InfluxDB or Graphite database",
			metavar="<BACKEND TYPE>"
                        )
    parser.add_argument("-d",
                        "--debug",
                        action="store_true",
                        dest="debug",
                        help="enable debug"
                        )
    parser.add_argument("-l",
                        "--log",
                        action="store_true",
                        dest="log",
                        help="enable log"
                        )
    parser.add_argument("-r",
                        "--release",
                        action="store_true",
                        dest="release",
                        help="show robot release and exit"
                        )

    args = parser.parse_args()

    vcsa = args.vcsa
    #username = args.username
    #password = args.password
    login = credentials(vcsa)
    username = login[0]
    password = login[1]
    method = args.method
    function = args.function
    checklist = args.checklist
    save = args.save
    debug = args.debug
    log = args.log
    release = args.release

    if release:
        print("$Id: %s [status: %s] v%s %s (%s %s) $" % (config.__project__, config.__status__, config.__version__,
                                                         config.__date__, config.__author__, config.__email__))
        print("This robot uses the methods exposed by the Rest API to monitor the VCSA.")
        sys.exit()

    if debug:
        print("[DEBUG] Option -v|--vcsa: %s" % str(vcsa))
        print("[DEBUG] Option -u|--username: %s" % str(username))
        #print("[DEBUG] Option -p|--password: %s" % str(password))
        print("[DEBUG] Option -p|--password: ******")
        print("[DEBUG] Option -m|--method: %s" % str(method))
        print("[DEBUG] Option -f|--function: %s (default: AVG)" % str(function))
        print("[DEBUG] Option -c|--checklist: %s" % str(checklist))
        print("[DEBUG] Option -s|--save: %s" % str(save))
        print("[DEBUG] Option -d|--debug: %s" % str(debug))
        print("[DEBUG] Option -l|--log: %s" % str(log))
        print("[DEBUG] Option -r|--release: %s" % str(release))

    if log:
        logger("/var/log/vcsa_monitor.log")
        logging.info("-- Start ---------------------------------------------------------")
        logging.debug("Option -v|--vcsa: %s" % str(vcsa))
        logging.debug("Option -u|--username: %s" % str(username))
        #logging.debug("Option -p|--password: %s" % str(password))
        logging.debug("Option -p|--password: ******")
        logging.debug("Option -m|--method: %s" % str(method))
        logging.debug("Option -f|--function: %s (default: AVG)" % str(function))
        logging.debug("Option -c|--checklist: %s" % str(checklist))
        logging.debug("Option -s|--save: %s" % str(save))
        logging.debug("Option -d|--debug: %s" % str(debug))
        logging.debug("Option -l|--log: %s" % str(log))
        logging.debug("Option -r|--release: %s" % str(release))

    if not checklist:
        if not vcsa or not method:
            print("You must specify the options -v and -m")
            if log:
                logging.error("You must specify the options -v and -m")
                logging.info("-- Finish --------------------------------------------------------")
            sys.exit(1)
    else:
        if not vcsa:
            print("You must specify the option -v")
            if log:
                logging.error("You must specify the option -v")
                logging.info("-- Finish --------------------------------------------------------")
            sys.exit(1)

    if not function:
        function = "AVG"    # Default value for metric function

    return vcsa, username, password, method, function, checklist, save, debug, log


def credentials(vcsa):
    """
    Get VCSA credentials from SexiGraf repository

    :param vcsa: name of a specific vCenter (fqdn)
    :type vcsa: str
    :returns: username and password decoded in base64
    :rtype: str
    """
    tree = ET.parse(config.repo_creds)
    root = tree.getroot()
    user = None
    pwdb64 = None
    for creds in root.findall('passwordEntry'):
        if creds.find('server').text == vcsa:
            user = creds.find('username').text
            pwdb64 = creds.find('password').text

    # Decoding base64
    #decoded = base64.b64decode(pwdb64)
    pwd_decoded = base64.b64decode(pwdb64).decode("utf-16-le")               # fix for password base64 encoded by Powershell

    return user, pwd_decoded
