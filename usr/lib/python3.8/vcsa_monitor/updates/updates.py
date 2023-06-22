import sys
import time
import logging
import requests
import urllib3
import json

# InsecureRequestWarning suppress (HTTPS)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_available_updates(vcsa, token, log, debug):
    """
    Get available updates

    :param vcsa: name of a specific vCenter (fqdn)
    :type vcsa: str
    :param token: session id
    :type token: str
    :param log: enable log to file
    :type log: bool
    :param debug: enable debug
    :type debug: bool
    :returns: available updates from VMware online repository
    :rtype: time, int
    """
    now = int(time.time())
    response = None
    updates = None          # 0 = not found, 1 = available

    if debug:
        print("[DEBUG] ::VCSA:: REST Method: Get available updates")

    if log:
        logging.info("::VCSA:: REST Method: Get available updates")

    url = 'https://' + vcsa + '/rest/appliance/update/pending?source_type=LOCAL_AND_ONLINE'
    headers = {
        'content-type': 'application/json'
    }
    cookies = {
        'vmware-api-session-id': token
    }

    if debug:
        print("[DEBUG] URI: %s" % url)

    try:
        response = requests.get(url, verify=False, headers=headers, cookies=cookies, timeout=urllib3.Timeout(connect=5.0, read=180.0))
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
        result = body_resp["value"]

        if debug:
            print("[DEBUG] Status: HTTP %s" % response.status_code)
            print("[DEBUG] The response contains {0} properties".format(len(body_resp)))
            print("[DEBUG] value:")
            print("[DEBUG] JSON %s" % json.dumps(result))

        if log:
            logging.debug("The response contains {0} properties".format(len(body_resp)))
            logging.debug("value:")
            logging.debug("JSON %s" % json.dumps(result))

        if len(result) > 0:
            if debug:
                print("[DEBUG] Updates list:")

            if log:
                logging.debug("Updates list:")

            countupd = 0
            for elem in result:
                countupd += 1
                version = elem["version"]
                update_type = elem["update_type"]
                release_date = elem["release_date"]
                severity = elem["severity"]
                priority = elem["priority"]
                size = str(elem["size"])
                description = elem["description"]["default_message"]

                if debug:
                    print("[DEBUG] #%s update" % str(countupd))
                    print("[DEBUG] version: %s" % version)
                    print("[DEBUG] update type: %s" % update_type)
                    print("[DEBUG] release date: %s" % release_date)
                    print("[DEBUG] severity: %s" % severity)
                    print("[DEBUG] priority: %s" % priority)
                    print("[DEBUG] size (MB): %s" % size)
                    print("[DEBUG] description: %s" % description)

                if log:
                    logging.debug("#%s update" % str(countupd))
                    logging.debug("version: %s" % version)
                    logging.debug("update type: %s" % update_type)
                    logging.debug("release date: %s" % release_date)
                    logging.debug("severity: %s" % severity)
                    logging.debug("priority: %s" % priority)
                    logging.debug("size (MB): %s" % size)
                    logging.debug("description: %s" % description)

            if countupd > 0:
                updates = 1
    elif response.status_code == 404:
        updates = 0

        if debug:
            print("[DEBUG] Status: HTTP %s" % response.status_code)
            print("[DEBUG] Updates not found")

        if log:
            logging.debug("Updates not found")
    elif response.status_code == 500:
        updates = 2

        if debug:
            print("[DEBUG] Status: HTTP %s" % response.status_code)
            print("[DEBUG] Cannot connect to repository")

        if log:
            logging.debug("Cannot connect to repository")
    else:
        # If response code is not ok (200 or 404), print the resulting http error code with description
        if debug:
            print("[DEBUG] HTTP response code is not 200 or 404!")

        if log:
            logging.error("HTTP response code is not 200 or 404!")
            logging.info("-- Finish --------------------------------------------------------")

        sys.exit(1)

    return now, updates
