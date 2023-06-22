import sys
import logging
import requests
import urllib3
import json
from requests.auth import HTTPBasicAuth

# InsecureRequestWarning suppress (HTTPS)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_session(vcsa, username, password, log, debug):
    """
    Get token session

    :param vcsa: name of a specific vCenter (fqdn)
    :type vcsa: str
    :param username: user to login on vCenter
    :type username: str
    :param password: password of the user
    :type password: str
    :param log: enable log to file
    :type log: bool
    :param debug: enable debug
    :type debug: bool
    :returns: Session token
    :rtype: str
    """
    response = None

    if debug:
        print("[DEBUG] ::VCSA:: REST Method: Get session token")

    if log:
        logging.info("::VCSA:: REST Method: Get session token")

    url = 'https://' + vcsa + '/api/session'
    headers = {
        'content-type': 'application/json'
    }

    if debug:
        print("[DEBUG] URI: %s" % url)

    try:
        response = requests.post(url, auth=HTTPBasicAuth(username, password), verify=False, headers=headers, timeout=urllib3.Timeout(connect=5.0, read=20.0))
        response.raise_for_status()
    except requests.exceptions.ConnectionError as errc:
        if debug:
            print("[DEBUG] Error connecting: %s" % errc)
        if log:
            logging.error("Error connecting: %s" % errc)

        return "failed"
    except requests.exceptions.Timeout as errt:
        if debug:
            print("[DEBUG] Timeout error: %s" % errt)
        if log:
            logging.error("Timeout error: %s" % errt)

        return "failed"
    except requests.exceptions.HTTPError as errh:
        if debug:
            print("[DEBUG] HTTP error: %s" % errh)

        if log:
            logging.error("HTTP error: %s" % errh)

    # For successful API call, response code will be 200 (OK)
    if response.ok:
        # Loading the response data into a dict variable
        result = json.loads(response.content)

        if debug:
            print("[DEBUG] Status: HTTP %s" % response.status_code)
            print("[DEBUG] value: %s" % result)

        if log:
            logging.debug("value: %s" % result)
    else:
        # If response code is not ok (200), print the resulting http error code with description
        result = "failed"

        if debug:
            print("[DEBUG] HTTP response code is not 200!")

        if log:
            logging.error("HTTP response code is not 200!")

    return result


def del_session(vcsa, token, log, debug):
    """
    Delete token session

    :param vcsa: name of a specific vCenter (fqdn)
    :type vcsa: str
    :param token: session id
    :type token: str
    :param log: enable log to file
    :type log: bool
    :param debug: enable debug
    :type debug: bool
    """
    response = None

    if debug:
        print("[DEBUG] ::VCSA:: REST Method: Delete session token")

    if log:
        logging.info("::VCSA:: REST Method: Delete session token")

    url = 'https://' + vcsa + '/rest/com/vmware/cis/session'
    headers = {
        'content-type': 'application/json'
    }
    cookies = {
        'vmware-api-session-id': token
    }

    if debug:
        print("[DEBUG] URI: %s" % url)

    try:
        response = requests.delete(url, verify=False, headers=headers, cookies=cookies, timeout=urllib3.Timeout(connect=5.0, read=20.0))
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
        if debug:
            print("[DEBUG] Status: HTTP %s" % response.status_code)
            print("[DEBUG] Session deleted (%s)" % token)

        if log:
            logging.debug("Session deleted (%s)" % token)
    else:
        # If response code is not ok (200), print the resulting http error code with description
        if debug:
            print("[DEBUG] HTTP response code is not 200!")

        if log:
            logging.error("HTTP response code is not 200!")
            logging.info("-- Finish --------------------------------------------------------")

        sys.exit(1)
