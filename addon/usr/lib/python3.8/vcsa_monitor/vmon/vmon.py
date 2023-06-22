import sys
import time
import logging
import requests
import urllib3
import json

# InsecureRequestWarning suppress (HTTPS)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_health_service(vcsa, token, service, log, debug):
    """
    Get service health status

    :param vcsa: name of a specific vCenter (fqdn)
    :type vcsa: str
    :param token: session id
    :type token: str
    :param service: name of a specific service
    :type service: str
    :param log: enable log to file
    :type log: bool
    :param debug: enable debug
    :type debug: bool
    :returns: dictionary with name and health status of the service (0 = HEALTHY, 1 = HEALTHY_WITH_WARNINGS, 2 = DEGRADED, 3 = STOPPED)
    :rtype: time, dict
    """
    now = int(time.time())
    response = None
    health_srvc = {}            # 0 = HEALTHY, 1 = HEALTHY_WITH_WARNINGS, 2 = DEGRADED, 3 = STOPPED
    all_srvc = [
        "content-library",
        "pschealth",
        "vcha",
        "vmware-vpostgres",
        "vmware-postgres-archiver",
        "vpxd",
        "vsan-health",
        "vsphere-client",
        "vsphere-ui"
    ]

    def service_verify(srvclist, srvcname):
        state = None
        health = None

        for elem in srvclist:
            if elem["key"] == srvcname:
                key = elem["key"]
                name_key = elem["value"]["name_key"]
                startup_type = elem["value"]["startup_type"]
                state = elem["value"]["state"]
                try:
                    health = elem["value"]["health"]
                except:
                    health = "--"

                if debug:
                    print("[DEBUG] - Service found:")
                    print("[DEBUG] key: %s" % key)
                    print("[DEBUG] name_key: %s" % name_key)
                    print("[DEBUG] startup_type: %s" % startup_type)
                    print("[DEBUG] state: %s" % state)
                    print("[DEBUG] health: %s" % health)

                if log:
                    logging.debug("- Service found:")
                    logging.debug("key: %s" % key)
                    logging.debug("name_key: %s" % name_key)
                    logging.debug("startup_type: %s" % startup_type)
                    logging.debug("state: %s" % state)
                    logging.debug("health: %s" % health)

            if state == "STARTED" and health == "HEALTHY":
                return 0
            elif state == "STARTED" and health == "HEALTHY_WITH_WARNINGS":
                return 1
            elif state == "STARTED" and health == "DEGRADED":
                return 2
            elif state == "STOPPED":
                return 3

    if debug:
        print("[DEBUG] ::VCSA:: REST Method: Get health service")

    if log:
        logging.info("::VCSA:: REST Method: Get health service")

    url = 'https://' + vcsa + '/rest/appliance/vmon/service'
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
            print("[DEBUG] value:")
            print("[DEBUG] JSON %s" % json.dumps(result))

        if log:
            logging.debug("The response contains {0} properties".format(len(body_resp)))
            logging.debug("value:")
            logging.debug("JSON %s" % json.dumps(result))

        if service == "ALL":
            for elem in all_srvc:
                health_srvc[elem] = service_verify(result, elem)
        elif service == "content-library":
            health_srvc[service] = service_verify(result, service)
        elif service == "pschealth":
            health_srvc[service] = service_verify(result, service)
        elif service == "vcha":
            health_srvc[service] = service_verify(result, service)
        elif service == "vmware-vpostgres":
            health_srvc[service] = service_verify(result, service)
        elif service == "vmware-postgres-archiver":
            health_srvc[service] = service_verify(result, service)
        elif service == "vpxd":
            health_srvc[service] = service_verify(result, service)
        elif service == "vsan-health":
            health_srvc[service] = service_verify(result, service)
        elif service == "vsphere-client":
            health_srvc[service] = service_verify(result, service)
        elif service == "vsphere-ui":
            health_srvc[service] = service_verify(result, service)
    else:
        # If response code is not ok (200), print the resulting http error code with description
        if debug:
            print("[DEBUG] HTTP response code is not 200!")

        if log:
            logging.error("HTTP response code is not 200!")
            logging.info("-- Finish --------------------------------------------------------")

        sys.exit(1)

    return now, health_srvc
