import sys
import logging
import json
import graphyte
from influxdb import InfluxDBClient
from .. import config


def store2influx(vcsa, measurement, timestamp, fields, log, debug):
    """
    Store data to time series database InfluxDB

    :param vcsa: name of a specific vCenter (fqdn) for tagging
    :type vcsa: str
    :param measurement: type of metric
    :type measurement: str
    :param timestamp: UTC time
    :type timestamp: datetime
    :param fields: value of metric
    :type fields: dict
    :param log: enable log to file
    :type log: bool
    :param debug: enable debug
    :type debug: bool
    """
    # Connection to InfluxDB instance
    host = config.influxdb_host
    port = config.influxdb_port
    user = config.influxdb_user
    password = config.influxdb_pwd
    dbname = config.influxdb_repo
    json_body = [
        {
            "measurement": measurement,
            "tags": {
                "hostname": vcsa,
                "poller": "pollerpy"
            },
            "time": timestamp,
            "fields": fields
        }
    ]

    client = InfluxDBClient(host, port, user, password, dbname, ssl=False, verify_ssl=False)
    json_dump = json.dumps(json_body)

    if debug:
        print("[DEBUG] ::InfluxDB:: Store data to database")
        print("[DEBUG] Write points: {0}".format(json_dump))

    if log:
        logging.info("::InfluxDB:: Store data to database")
        logging.debug("Write points: {0}".format(json_dump))

    try:
        result = client.write_points(json_body)
        if result:
            if debug:
                print("[DEBUG] Write data to InfluxDB: OK")

            if log:
                logging.debug("Write data to InfluxDB: OK")
    except:
        if debug:
            print("[ERROR] Cannot write data to InfluxDB!")

        if log:
            logging.error("Cannot write data to InfluxDB!")
            logging.info("-- Finish --------------------------------------------------------")

        sys.exit(1)


def store2graphite(vcsa, group, timestamp, measurement, value, log, debug):
    """
    Store data to time series database Graphite

    :param vcsa: name of a specific vCenter (fqdn) for tagging
    :type vcsa: str
    :param group: group of metrics
    :type group: str
    :param timestamp: UTC time
    :type timestamp: datetime
    :param measurement: type of metric
    :type measurement: str
    :param value: value of metric
    :type value: str|numeric
    :param log: enable log to file
    :type log: bool
    :param debug: enable debug
    :type debug: bool
    """
    # Connection to Graphite instance
    vcsa = vcsa.replace('.','_')
    repo = config.graphite_basepath + "." + vcsa
    datapath = repo + "." + group
    graphyte.init(config.graphite_host, config.graphite_port, prefix=datapath)

    if debug:
        print("[DEBUG] ::Graphite:: Store data to database")
        print("[DEBUG] repo: %s" % repo)
        print("[DEBUG] group: %s" % group)
        print("[DEBUG] measurement: %s" % measurement)
        print("[DEBUG] value: %s" % value)

    if log:
        logging.info("::Graphite:: Store data to database")
        logging.debug("repo: %s" % repo)
        logging.debug("group: %s" % group)
        logging.debug("measurement: %s" % measurement)
        logging.debug("value: %s" % value)

    try:
        graphyte.send(measurement, value, timestamp)

        if debug:
            print("[DEBUG] Write data to Graphite: OK")

        if log:
            logging.debug("Write data to Graphite: OK")
    except:
        if debug:
            print("[ERROR] Cannot write data to Graphite!")

        if log:
            logging.error("Cannot write data to Graphite!")
            logging.info("-- Finish --------------------------------------------------------")

        sys.exit(1)
