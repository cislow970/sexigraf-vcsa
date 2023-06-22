import sys
import time
import logging
import requests
import urllib3
import json

# InsecureRequestWarning suppress (HTTPS)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_health(vcsa, token, category, log, debug):
    """
    Get health status of system, load, memory, storage and swap

    :param vcsa: name of a specific vCenter (fqdn)
    :type vcsa: str
    :param token: session id
    :type token: str
    :param category: name of the subsystem whose integrity is to be verified
    :type category: str
    :param log: enable log to file
    :type log: bool
    :param debug: enable debug
    :type debug: bool
    :returns: health status of sub-system (1 = green, 2 = orange, 3 = red, 4 = gray)
    :rtype: time, str
    """
    now = int(time.time())
    response = None
    status_code = None

    if debug:
        print("[DEBUG] ::VCSA:: REST Method: Get health %s" % category)

    if log:
        logging.info("::VCSA:: REST Method: Get health %s" % category)

    url = 'https://' + vcsa + '/rest/appliance/health/' + category
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

        if debug:
            print("[DEBUG] Status: HTTP %s" % response.status_code)
            print("[DEBUG] The response contains {0} properties".format(len(body_resp)))
            print("[DEBUG] value: %s" % result)

        if log:
            logging.debug("The response contains {0} properties".format(len(body_resp)))
            logging.debug("value: %s" % result)

        # 1 = green, 2 = orange, 3 = red, 4 = gray
        if result == "green":
            status_code = 1
        elif result == "orange":
            status_code = 2
        elif result == "red":
            status_code = 3
        elif result == "gray":      # cannot retrieve status (N/A)
            status_code = 4
    else:
        # If response code is not ok (200), print the resulting http error code with description
        if debug:
            print("[DEBUG] HTTP response code is not 200!")

        if log:
            logging.error("HTTP response code is not 200!")
            logging.info("-- Finish --------------------------------------------------------")

        sys.exit(1)

    return now, status_code
