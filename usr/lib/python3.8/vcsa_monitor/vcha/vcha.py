import sys
import time
import logging
import requests
import urllib3
import json

# InsecureRequestWarning suppress (HTTPS)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_vcha_active_node(vcsa, token, log, debug):
    """
    Get VCHA active node

    :param vcsa: name of a specific vCenter (fqdn)
    :type vcsa: str
    :param token: session id
    :type token: str
    :param log: enable log to file
    :type log: bool
    :param debug: enable debug
    :type debug: bool
    :returns: name and ip of the active node
    :rtype: time, str
    """
    now = int(time.time())
    response = None

    if debug:
        print("[DEBUG] ::VCSA:: REST Method: Get VCHA active node")

    if log:
        logging.info("::VCSA:: REST Method: Get VCHA active node")

    url = 'https://' + vcsa + '/api/vcenter/vcha/cluster/active?action=get'
    headers = {
        'content-type': 'application/json'
    }
    cookies = {
        'vmware-api-session-id': token
    }

    if debug:
        print("[DEBUG] URI: %s" % url)

    try:
        response = requests.post(url, verify=False, headers=headers, cookies=cookies, timeout=urllib3.Timeout(connect=5.0, read=20.0))
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
        if errh.response.status_code != 404:
            if debug:
                print("[DEBUG] HTTP error: %s" % errh)
            if log:
                logging.error("HTTP error: %s" % errh)

    # For successful API call, response code will be 200 (OK)
    if response.ok:
        # Loading the response data into a dict variable
        body_resp = json.loads(response.content)
        #result = body_resp["value"]
        result = body_resp      #fix change rest api response

        try:
            ha_ip = result["ha"]["ipv4"]["address"]
            ha_name = result["placement"]["vm_name"]
            vcha_config = "present"

            if debug:
                print("[DEBUG] Status: HTTP %s" % response.status_code)
                print("[DEBUG] The response contains {0} properties".format(len(body_resp)))
                print("[DEBUG] value:")
                print("[DEBUG] JSON %s" % json.dumps(result))
                print("[DEBUG] HA IP: %s" % ha_ip)
                print("[DEBUG] HA Name: %s" % ha_name)

            if log:
                logging.debug("The response contains {0} properties".format(len(body_resp)))
                logging.debug("value:")
                logging.debug("JSON %s" % json.dumps(result))
                logging.debug("HA IP: %s" % ha_ip)
                logging.debug("HA Name: %s" % ha_name)
        except:
            vcha_config = "absent"
            ha_ip = "--"
            ha_name = "--"

            if debug:
                print("[DEBUG] Status: HTTP %s" % response.status_code)
                print("[DEBUG] The response contains {0} properties".format(len(body_resp)))
                print("[DEBUG] value:")
                print("[DEBUG] JSON %s" % json.dumps(result))
                print("[DEBUG] HA data not found")
                print("[DEBUG] VCHA is not configured!")

            if log:
                logging.debug("The response contains {0} properties".format(len(body_resp)))
                logging.debug("value:")
                logging.debug("JSON %s" % json.dumps(result))
                logging.debug("HA data not found")
                logging.debug("VCHA is not configured!")
    elif response.status_code == 404:
        vcha_config = "absent"
        ha_ip = "--"
        ha_name = "--"

        if debug:
            print("[DEBUG] Status: HTTP %s" % response.status_code)
            print("[DEBUG] HA data not found")
            print("[DEBUG] VCHA is not configured!")

        if log:
            logging.debug("HA data not found")
            logging.debug("VCHA is not configured!")
    else:
        # If response code is not ok (200 or 404), print the resulting http error code with description
        if debug:
            print("[DEBUG] HTTP response code is not 200 or 404!")

        if log:
            logging.error("HTTP response code is not 200 or 404!")
            logging.info("-- Finish --------------------------------------------------------")

        sys.exit(1)

    return now, vcha_config, ha_ip, ha_name


def get_vcha_health_cluster(vcsa, token, log, debug):
    """
    Get VCHA health cluster

    :param vcsa: name of a specific vCenter (fqdn)
    :type vcsa: str
    :param token: session id
    :type token: str
    :param log: enable log to file
    :type log: bool
    :param debug: enable debug
    :type debug: bool
    :returns: vcha cluster status
    :rtype: datetime, str
    """
    now = int(time.time())
    response = None

    if debug:
        print("[DEBUG] ::VCSA:: REST Method: Get VCHA health cluster")

    if log:
        logging.info("::VCSA:: REST Method: Get VCHA health cluster")

    url = 'https://' + vcsa + '/api/vcenter/vcha/cluster?action=get'
    headers = {
        'content-type': 'application/json'
    }
    cookies = {
        'vmware-api-session-id': token
    }

    if debug:
        print("[DEBUG] URI: %s" % url)

    try:
        response = requests.post(url, verify=False, headers=headers, cookies=cookies, timeout=urllib3.Timeout(connect=5.0, read=20.0))
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
        if errh.response.status_code != 404:
            if debug:
                print("[DEBUG] HTTP error: %s" % errh)
            if log:
                logging.error("HTTP error: %s" % errh)

    # For successful API call, response code will be 200 (OK)
    if response.ok:
        # Loading the response data into a dict variable
        body_resp = json.loads(response.content)
        #result = body_resp["value"]
        result = body_resp	#fix change rest api response

        config_state = result["config_state"]                               # CONFIGURED, NOTCONFIGURED

        try:
            cluster_mode = result["mode"]                                   # ENABLED, MAINTENANCE, DISABLED
            health_state = result["health_state"]                           # HEALTHY, HEALTHY_WITH_WARNINGS, DEGRADED
            manual_failover_allowed = result["manual_failover_allowed"]     # True, False
            auto_failover_allowed = result["auto_failover_allowed"]         # True, False
        except:
            cluster_mode = "--"
            health_state = "--"
            manual_failover_allowed = "--"
            auto_failover_allowed = "--"

        try:
            health_warnings = result["health_warnings"]
        except:
            health_warnings = "--"

        try:
            primary_role = result["node1"]["runtime"]["role"]
            secondary_role = result["node2"]["runtime"]["role"]
            primary_state = result["node1"]["runtime"]["state"]
            secondary_state = result["node2"]["runtime"]["state"]
            witness_state = result["witness"]["runtime"]["state"]
        except:
            primary_role = "--"
            secondary_role = "--"
            primary_state = "--"
            secondary_state = "--"
            witness_state = "--"

        if debug:
            print("[DEBUG] Status: HTTP %s" % response.status_code)
            print("[DEBUG] The response contains {0} properties".format(len(body_resp)))
            print("[DEBUG] value:")
            print("[DEBUG] JSON %s" % json.dumps(result))
            print("[DEBUG] config_state: %s" % config_state)
            print("[DEBUG] cluster_mode: %s" % cluster_mode)
            print("[DEBUG] health_state: %s" % health_state)
            print("[DEBUG] manual_failover_allowed: %s" % manual_failover_allowed)
            print("[DEBUG] auto_failover_allowed: %s" % auto_failover_allowed)
            print("[DEBUG] health_warnings: %s" % health_warnings)
            print("[DEBUG] primary_role: %s" % primary_role)
            print("[DEBUG] secondary_role: %s" % secondary_role)
            print("[DEBUG] primary_state: %s" % primary_state)
            print("[DEBUG] secondary_state: %s" % secondary_state)
            print("[DEBUG] witness_state: %s" % witness_state)

        if log:
            logging.debug("The response contains {0} properties".format(len(body_resp)))
            logging.debug("value:")
            logging.debug("JSON %s" % json.dumps(result))
            logging.debug("config_state: %s" % config_state)
            logging.debug("cluster_mode: %s" % cluster_mode)
            logging.debug("health_state: %s" % health_state)
            logging.debug("manual_failover_allowed: %s" % manual_failover_allowed)
            logging.debug("auto_failover_allowed: %s" % auto_failover_allowed)
            logging.debug("health_warnings: %s" % health_warnings)
            logging.debug("primary_role: %s" % primary_role)
            logging.debug("secondary_role: %s" % secondary_role)
            logging.debug("primary_state: %s" % primary_state)
            logging.debug("secondary_state: %s" % secondary_state)
            logging.debug("witness_state: %s" % witness_state)
    elif response.status_code == 404:
        config_state = "--"
        cluster_mode = "--"
        health_state = "--"
        manual_failover_allowed = "--"
        auto_failover_allowed = "--"
        health_warnings = "--"
        primary_role = "--"
        secondary_role = "--"
        primary_state = "--"
        secondary_state = "--"
        witness_state = "--"

        if debug:
            print("[DEBUG] Status: HTTP %s" % response.status_code)
            print("[DEBUG] VCHA cluster status is not defined!")

        if log:
            logging.debug("[DEBUG] VCHA cluster status is not defined!")
    else:
        # If response code is not ok (200 or 404), print the resulting http error code with description
        if debug:
            print("[DEBUG] HTTP response code is not 200 or 404!")

        if log:
            logging.error("HTTP response code is not 200 or 404!")
            logging.info("-- Finish --------------------------------------------------------")

        sys.exit(1)

    return now, config_state, cluster_mode, health_state, manual_failover_allowed, auto_failover_allowed, health_warnings, primary_role, secondary_role, primary_state, secondary_state, witness_state
