import sys
import time
import logging
import requests
import urllib3
import json
import datetime

# InsecureRequestWarning suppress (HTTPS)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_network_performance(vcsa, token, perftype, function, log, debug):
    """
    Get network usage

    :param vcsa: name of a specific vCenter (fqdn)
    :type vcsa: str
    :param token: session id
    :type token: str
    :param perftype: set a specific performance metric
    :type perftype: str
    :param function: set a specific metric function
    :type function: str
    :param log: enable log to file
    :type log: bool
    :param debug: enable debug
    :type debug: bool
    :returns: percent or bytes or iops (sampling: 5 minutes)
    :rtype: time, float
    """
    unixtime = int(time.time())
    now = datetime.datetime.utcnow()
    now_minus_5 = now + datetime.timedelta(minutes=-5)
    metric = None
    unit = None
    response = None
    performance = {}

    if perftype == "rx_activity_eth0":
        metric = "net.rx.activity.eth0"
        unit = "kb_per_sec"
    elif perftype == "rx_activity_eth1":
        metric = "net.rx.activity.eth1"
        unit = "kb_per_sec"
    elif perftype == "rx_packetRate_eth0":
        metric = "net.rx.packetRate.eth0"
        unit = "packets_per_sec"
    elif perftype == "rx_packetRate_eth1":
        metric = "net.rx.packetRate.eth1"
        unit = "packets_per_sec"
    elif perftype == "rx_drop_eth0":
        metric = "net.rx.drop.eth0"
        unit = "drops_per_sample"
    elif perftype == "rx_drop_eth1":
        metric = "net.rx.drop.eth1"
        unit = "drops_per_sample"
    elif perftype == "rx_error_eth0":
        metric = "net.rx.error.eth0"
        unit = "errors_per_sample"
    elif perftype == "rx_error_eth1":
        metric = "net.rx.error.eth1"
        unit = "errors_per_sample"
    elif perftype == "tx_activity_eth0":
        metric = "net.tx.activity.eth0"
        unit = "kb_per_sec"
    elif perftype == "tx_activity_eth1":
        metric = "net.tx.activity.eth1"
        unit = "kb_per_sec"
    elif perftype == "tx_packetRate_eth0":
        metric = "net.tx.packetRate.eth0"
        unit = "packets_per_sec"
    elif perftype == "tx_packetRate_eth1":
        metric = "net.tx.packetRate.eth1"
        unit = "packets_per_sec"
    elif perftype == "tx_drop_eth0":
        metric = "net.tx.drop.eth0"
        unit = "drops_per_sample"
    elif perftype == "tx_drop_eth1":
        metric = "net.tx.drop.eth1"
        unit = "drops_per_sample"
    elif perftype == "tx_error_eth0":
        metric = "net.tx.error.eth0"
        unit = "errors_per_sample"
    elif perftype == "tx_error_eth1":
        metric = "net.tx.error.eth1"
        unit = "errors_per_sample"

    if debug:
        print("[DEBUG] ::VCSA:: REST Method: Get network %s usage (%s)" % (perftype, function))

    if log:
        logging.info("::VCSA:: REST Method: Get network %s usage (%s)" % (perftype, function))

    url = 'https://' + vcsa + '/rest/appliance/monitoring/query?item.interval=MINUTES5&item.start_time=' + now_minus_5.strftime("%Y-%m-%dT%H:%M:00.000Z") + '&item.end_time=' + now.strftime("%Y-%m-%dT%H:%M:00.000Z") + '&item.function=' + function + '&item.names.1=' + metric
    headers = {
        'content-type': 'application/json'
    }
    cookies = {
        'vmware-api-session-id': token
    }

    if debug:
        print("[DEBUG] URI: %s" % url)

    try:
        response = requests.get(url, verify=False, headers=headers, cookies=cookies, timeout=urllib3.Timeout(connect=5.0, read=20.0))
        response.raise_for_status()
    except requests.exceptions.ConnectionError as errc:
        if debug:
            print("[DEBUG] Error connecting: %s" % errc)
        if log:
            logging.error("Error connecting: %s" % errc)
            logging.info("-- Finish --------------------------------------------------------")
        sys.exit(1)
    except requests.exceptions.Timeout as errt:
        if debug:
            print("[DEBUG] Timeout error: %s" % errt)
        if log:
            logging.error("Timeout error: %s" % errt)
            logging.info("-- Finish --------------------------------------------------------")
        sys.exit(1)
    except requests.exceptions.HTTPError as errh:
        if debug:
            print("[DEBUG] HTTP error: %s" % errh)
        if log:
            logging.error("HTTP error: %s" % errh)

    # For successful API call, response code will be 200 (OK)
    if response.ok:
        # Loading the response data into a dict variable
        body_resp = json.loads(response.content)
        result = body_resp["value"]
        samples = result[0]["data"]

        if debug:
            print("[DEBUG] Status: HTTP %s" % response.status_code)
            print("[DEBUG] The response contains {0} properties".format(len(body_resp)))
            print("[DEBUG] value:")
            print("[DEBUG] JSON %s" % json.dumps(result))
            print("[DEBUG] data:")
            print("[DEBUG] ARRAY %s" % json.dumps(samples))

        if log:
            logging.debug("The response contains {0} properties".format(len(body_resp)))
            logging.debug("value:")
            logging.debug("JSON %s" % json.dumps(result))
            logging.debug("data:")
            logging.debug("ARRAY %s" % json.dumps(samples))

        if samples[-2] != '':
            rate = round(float(samples[-2]), 6)
        else:
            rate = samples[-2]
        start_time = now_minus_5.strftime("%Y-%m-%dT%H:%M:00.000Z")
        performance[start_time] = rate

        if samples[-1] != '':
            rate = round(float(samples[-1]), 6)
        else:
            rate = samples[-1]
        end_time = now.strftime("%Y-%m-%dT%H:%M:00.000Z")
        performance[end_time] = rate

        if debug:
            print("[DEBUG] performance: %s" % str(performance))

        if log:
            logging.debug("performance: %s" % str(performance))

        utctime = sorted(performance.keys())[-1]
        value = performance[utctime]
        if value == '':
            value = performance[sorted(performance.keys())[-2]]
    else:
        # If response code is not ok (200), print the resulting http error code with description
        if debug:
            print("[DEBUG] HTTP response code is not 200!")

        if log:
            logging.error("HTTP response code is not 200!")
            logging.info("-- Finish --------------------------------------------------------")

        sys.exit(1)

    return unixtime, value, unit
