import sys
import time
import logging
import requests
import urllib3
import json
import datetime

# InsecureRequestWarning suppress (HTTPS)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_filesystem_usage(vcsa, token, filesystem, function, log, debug):
    """
    Get filesytem usage

    :param vcsa: name of a specific vCenter (fqdn)
    :type vcsa: str
    :param token: session id
    :type token: str
    :param filesystem: set a specific filesystem
    :type filesystem: str
    :param function: set a specific metric function
    :type function: str
    :param log: enable log to file
    :type log: bool
    :param debug: enable debug
    :type debug: bool
    :returns: percent (sampling: 30 minutes)
    :rtype: time, float
    """
    unixtime = int(time.time())
    now = datetime.datetime.utcnow()
    now_minus_30 = now + datetime.timedelta(minutes=-30)
    metric = None
    response = None
    utilization = {}

    if filesystem == "fs_root":
        metric = "storage.util.filesystem.root"
    elif filesystem == "fs_swap":
        metric = "storage.util.filesystem.swap"
    elif filesystem == "fs_boot":
        metric = "storage.util.filesystem.boot"
    elif filesystem == "fs_core":
        metric = "storage.util.filesystem.core"
    elif filesystem == "fs_log":
        metric = "storage.util.filesystem.log"
    elif filesystem == "fs_db":
        metric = "storage.util.filesystem.db"
    elif filesystem == "fs_dblog":
        metric = "storage.util.filesystem.dblog"
    elif filesystem == "fs_seat":
        metric = "storage.util.filesystem.seat"
    elif filesystem == "fs_archive":
        metric = "storage.util.filesystem.archive"
    elif filesystem == "fs_updatemgr":
        metric = "storage.util.filesystem.updatemgr"
    elif filesystem == "fs_imagebuilder":
        metric = "storage.util.filesystem.imagebuilder"
    elif filesystem == "fs_autodeploy":
        metric = "storage.util.filesystem.autodeploy"
    elif filesystem == "fs_netdump":
        metric = "storage.util.filesystem.netdump"
    elif filesystem == "fs_lifecycle":
        metric = "storage.util.filesystem.lifecycle"
    elif filesystem == "fs_vtsdb":
        metric = "storage.util.filesystem.vtsdb"
    elif filesystem == "fs_vtsdblog":
        metric = "storage.util.filesystem.vtsdblog"

    if debug:
        print("[DEBUG] ::VCSA:: REST Method: Get filesystem %s usage (%s)" % (filesystem, function))

    if log:
        logging.info("::VCSA:: REST Method: Get filesystem %s usage (%s)" % (filesystem, function))

    url = 'https://' + vcsa + '/rest/appliance/monitoring/query?item.interval=MINUTES30&item.start_time=' + now_minus_30.strftime("%Y-%m-%dT%H:%M:00.000Z") + '&item.end_time=' + now.strftime("%Y-%m-%dT%H:%M:00.000Z") + '&item.function=' + function + '&item.names.1=' + metric
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
            percent = round(float(samples[-2]), 2)
        else:
            percent = samples[-2]
        start_time = now_minus_30.strftime("%Y-%m-%dT%H:%M:00.000Z")
        utilization[start_time] = percent

        if samples[-1] != '':
            percent = round(float(samples[-1]), 2)
        else:
            percent = samples[-1]
        end_time = now.strftime("%Y-%m-%dT%H:%M:00.000Z")
        utilization[end_time] = percent

        if debug:
            print("[DEBUG] utilization: %s" % str(utilization))

        if log:
            logging.debug("utilization: %s" % str(utilization))

        utctime = sorted(utilization.keys())[-1]
        value = utilization[utctime]
        if value == '':
            value = utilization[sorted(utilization.keys())[-2]]
    else:
        # If response code is not ok (200), print the resulting http error code with description
        if debug:
            print("[DEBUG] HTTP response code is not 200!")

        if log:
            logging.error("HTTP response code is not 200!")
            logging.info("-- Finish --------------------------------------------------------")

        sys.exit(1)

    return unixtime, value
