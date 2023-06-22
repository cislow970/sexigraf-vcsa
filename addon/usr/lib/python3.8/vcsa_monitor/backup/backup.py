import sys
import time
import logging
import requests
import urllib3
import json
import re

# InsecureRequestWarning suppress (HTTPS)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_backup_status(vcsa, token, log, debug):
    """
    Get latest backup status

    :param vcsa: name of a specific vCenter (fqdn)
    :type vcsa: str
    :param token: session id
    :type token: str
    :param log: enable log to file
    :type log: bool
    :param debug: enable debug
    :type debug: bool
    :returns: latest backup properties
    :rtype: time, int, str
    """
    now = int(time.time())
    response = None

    if debug:
        print("[DEBUG] ::VCSA:: REST Method: Get latest backup status")

    if log:
        logging.info("::VCSA:: REST Method: Get latest backup status")

    url = 'https://' + vcsa + '/rest/appliance/recovery/backup/job/details'
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

        tot_backup_job = 0
        latest_job_status = None
        latest_job_type = None
        latest_job_start_time = None
        latest_job_end_time = None
        latest_job_size = None
        if result:
            tot_backup_job = len(result)

            if debug:
                print("[DEBUG] Found backup job: %s" % tot_backup_job)
            if log:
                logging.debug("Found backup job: %s" % tot_backup_job)

            count = 0
            latest_job_idx = 0
            latest_job_timestamp = 0
            pattern = r'(.+)\-(.+)\-(.+)'

            for idx in range(tot_backup_job):
                if debug:
                    print("[DEBUG] Job Index %s" % idx)
                    print("[DEBUG] Job Key %s" % result[idx]["key"])
                if log:
                    logging.debug("Job Index %s" % idx)
                    logging.debug("Job Key %s" % result[idx]["key"])

                match = re.match(pattern, result[idx]["key"])
                if match:
                    if debug:
                        print("[DEBUG] Full match: %s" % match.group())
                        print("[DEBUG] Group(1): %s" % match.group(1))
                        print("[DEBUG] Group(2): %s" % match.group(2))
                        print("[DEBUG] Group(3): %s" % match.group(3))
                    if log:
                        logging.debug("Full match: %s" % match.group())
                        logging.debug("Group(1): %s" % match.group(1))
                        logging.debug("Group(2): %s" % match.group(2))
                        logging.debug("Group(3): %s" % match.group(3))

                    count += 1
                    timestamp_job = match.group(1) + match.group(2) + match.group(3)
                    if int(timestamp_job) > latest_job_timestamp:
                        latest_job_timestamp = int(timestamp_job)
                        latest_job_idx = idx
                else:
                    if debug:
                        print("[DEBUG] No match!")
                    if log:
                        logging.debug("No match!")

            latest_job = result[latest_job_idx]
            latest_job_status = latest_job["value"]["status"]
            latest_job_type = latest_job["value"]["type"]
            latest_job_start_time = latest_job["value"]["start_time"]
            latest_job_end_time = latest_job["value"]["end_time"]
            latest_job_size = round(float(latest_job["value"]["size"])/1073741824, 2)

            if debug:
                print("[DEBUG] Processed backup job: %s" % count)
                print("[DEBUG] Latest backup job index: %s" % latest_job_idx)
                print("[DEBUG] Latest backup job timestamp: %s" % latest_job_timestamp)
                print("[DEBUG] Latest backup job details: %s" % json.dumps(latest_job))
                print("[DEBUG] Status: %s" % latest_job_status)
                print("[DEBUG] Type: %s" % latest_job_type)
                print("[DEBUG] Start Time: %s" % latest_job_start_time)
                print("[DEBUG] End Time: %s" % latest_job_end_time)
                print("[DEBUG] Size (GB): %s" % latest_job_size)

            if log:
                logging.debug("Processed backup job: %s" % count)
                logging.debug("Latest backup job Index: %s" % latest_job_idx)
                logging.debug("Latest backup job Timestamp: %s" % latest_job_timestamp)
                logging.debug("Latest backup job details: %s" % json.dumps(latest_job))
                logging.debug("Status: %s" % latest_job_status)
                logging.debug("Type: %s" % latest_job_type)
                logging.debug("Start Time: %s" % latest_job_start_time)
                logging.debug("End Time: %s" % latest_job_end_time)
                logging.debug("Size (GB): %s" % latest_job_size)

            return now, tot_backup_job, latest_job_status, latest_job_type, latest_job_start_time, latest_job_end_time, latest_job_size
        else:
            return now, tot_backup_job, latest_job_status, latest_job_type, latest_job_start_time, latest_job_end_time, latest_job_size
    else:
        # If response code is not ok (200), print the resulting http error code with description
        if debug:
            print("[DEBUG] HTTP response code is not 200!")

        if log:
            logging.error("HTTP response code is not 200!")
            logging.info("-- Finish --------------------------------------------------------")

        sys.exit(1)
