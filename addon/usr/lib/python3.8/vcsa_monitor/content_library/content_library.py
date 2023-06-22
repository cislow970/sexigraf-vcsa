import sys
import time
import logging
import requests
import urllib3
import json

# InsecureRequestWarning suppress (HTTPS)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_clib_sync(vcsa, token, log, debug):
    """
    Get content libraries synchronization status

    :param vcsa: name of a specific vCenter (fqdn)
    :type vcsa: str
    :param token: session id
    :type token: str
    :param log: enable log to file
    :type log: bool
    :param debug: enable debug
    :type debug: bool
    :returns: list content libraries not sync
    :rtype: time, bool, list, bool
    """
    now = int(time.time())
    response = None
    not_sync_lib_name = []

    if debug:
        print("[DEBUG] ::VCSA:: REST Method: Get content libraries sync status")

    if log:
        logging.info("::VCSA:: REST Method: Get content libraries sync status")

    url = 'https://' + vcsa + '/rest/com/vmware/content/subscribed-library'
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
        liblist = body_resp["value"]

        if debug:
            print("[DEBUG] Status: HTTP %s" % response.status_code)
            print("[DEBUG] The response contains {0} properties".format(len(body_resp)))
            print("[DEBUG] Library ID:")
            print("[DEBUG] JSON %s" % json.dumps(liblist))

        if log:
            logging.debug("The response contains {0} properties".format(len(body_resp)))
            logging.debug("Library ID:")
            logging.debug("JSON %s" % json.dumps(liblist))

        if liblist:
            clib_subscribed = True
            not_sync_lib = []
            for lib in liblist:
                not_sync_item = 0
                libid = { "library_id": lib }
                url = 'https://' + vcsa + '/rest/com/vmware/content/library/item?~action=list'
                headers = {
                    'content-type': 'application/json'
                }
                cookies = {
                    'vmware-api-session-id': token
                }

                if debug:
                    print("[DEBUG] URI: %s" % url)

                try:
                    response = requests.post(url, verify=False, headers=headers, cookies=cookies, timeout=urllib3.Timeout(connect=5.0, read=20.0), json=libid)
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

                if response.ok:
                    # Loading the response data into a dict variable
                    body_resp = json.loads(response.content)
                    itemlist = body_resp["value"]

                    if debug:
                        print("[DEBUG] Status: HTTP %s" % response.status_code)
                        print("[DEBUG] The response contains {0} properties".format(len(body_resp)))
                        print("[DEBUG] Items ID of library %s" % lib)
                        print("[DEBUG] JSON %s" % json.dumps(itemlist))

                    if log:
                        logging.debug("The response contains {0} properties".format(len(body_resp)))
                        logging.debug("Items ID of library %s" % lib)
                        logging.debug("JSON %s" % json.dumps(itemlist))

                    for item in itemlist:
                        itemid = { "library_item_id": item }
                        url = 'https://' + vcsa + '/rest/com/vmware/content/library/item?~action=get'
                        headers = {
                            'content-type': 'application/json'
                        }
                        cookies = {
                            'vmware-api-session-id': token
                        }

                        if debug:
                            print("[DEBUG] URI: %s" % url)

                        try:
                            response = requests.post(url, verify=False, headers=headers, cookies=cookies, timeout=urllib3.Timeout(connect=5.0, read=20.0), json=itemid)
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

                        if response.ok:
                            # Loading the response data into a dict variable
                            body_resp = json.loads(response.content)
                            itemdetails = body_resp["value"]

                            if debug:
                                print("[DEBUG] Status: HTTP %s" % response.status_code)
                                print("[DEBUG] The response contains {0} properties".format(len(body_resp)))
                                print("[DEBUG] Details of item %s in library %s" % (item, lib))
                                print("[DEBUG] JSON %s" % json.dumps(itemdetails))

                            if log:
                                logging.debug("The response contains {0} properties".format(len(body_resp)))
                                logging.debug("Details of item %s in library %s" % (item, lib))
                                logging.debug("JSON %s" % json.dumps(itemdetails))

                            if itemdetails["cached"]:
                                if debug:
                                    print("[DEBUG] Item %s is synchronized" % item)
                                if log:
                                    logging.debug("Item %s is synchronized" % item)
                            else:
                                not_sync_item += 1
                                if debug:
                                    print("[WARNING] Item %s is unsynchronized" % item)
                                if log:
                                    logging.warning("Item %s is unsynchronized" % item)
                        else:
                            # If response code is not ok (200), print the resulting http error code with description
                            if debug:
                                print("[DEBUG] HTTP response code is not 200!")

                            if log:
                                logging.error("HTTP response code is not 200!")
                                logging.info("-- Finish --------------------------------------------------------")

                            sys.exit(1)

                    if not_sync_item == 0:
                        if debug:
                            print("[DEBUG] All items in library %s are synchronized" % lib)
                        if log:
                            logging.debug("All items in library %s are synchronized" % lib)
                    else:
                        not_sync_lib.append(lib)
                        if debug:
                            print("[WARNING] The library %s contains unsynchronized items" % lib)
                        if log:
                            logging.warning("The library %s contains unsynchronized items" % lib)
                else:
                    # If response code is not ok (200), print the resulting http error code with description
                    if debug:
                        print("[DEBUG] HTTP response code is not 200!")

                    if log:
                        logging.error("HTTP response code is not 200!")
                        logging.info("-- Finish --------------------------------------------------------")

                    sys.exit(1)
        else:
            clib_subscribed = False
            sync_status = 2             # 0 = sync warning, 1 = sync ok, 2 = sync not configured
            if debug:
                print("[DEBUG] There are no content libraries subscribed")
            if log:
                logging.debug("There are no content libraries subscribed")

            return now, clib_subscribed, not_sync_lib_name, sync_status
    else:
        # If response code is not ok (200), print the resulting http error code with description
        if debug:
            print("[DEBUG] HTTP response code is not 200!")

        if log:
            logging.error("HTTP response code is not 200!")
            logging.info("-- Finish --------------------------------------------------------")

        sys.exit(1)

    if len(not_sync_lib) > 0:
        sync_status = 0         # 0 = sync warning, 1 = sync ok, 2 = sync not configured

        if debug:
            print("[DEBUG] Total libraries unsynchronized = %s" % len(not_sync_lib))
        if log:
            logging.debug("Total libraries unsynchronized = %s" % len(not_sync_lib))

        for lib in not_sync_lib:
            libid = {"library_id": lib}
            url = 'https://' + vcsa + '/rest/com/vmware/content/library?~action=get'
            headers = {
                'content-type': 'application/json'
            }
            cookies = {
                'vmware-api-session-id': token
            }

            if debug:
                print("[DEBUG] URI: %s" % url)

            try:
                response = requests.post(url, verify=False, headers=headers, cookies=cookies, timeout=urllib3.Timeout(connect=5.0, read=20.0), json=libid)
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

            if response.ok:
                # Loading the response data into a dict variable
                body_resp = json.loads(response.content)
                libdetails = body_resp["value"]

                if debug:
                    print("[DEBUG] Status: HTTP %s" % response.status_code)
                    print("[DEBUG] The response contains {0} properties".format(len(body_resp)))
                    print("[DEBUG] Details of library %s" % lib)
                    print("[DEBUG] JSON %s" % json.dumps(libdetails))

                if log:
                    logging.debug("The response contains {0} properties".format(len(body_resp)))
                    logging.debug("Details of library %s" % lib)
                    logging.debug("JSON %s" % json.dumps(libdetails))

                not_sync_lib_name.append(libdetails["name"])
            else:
                # If response code is not ok (200), print the resulting http error code with description
                if debug:
                    print("[DEBUG] HTTP response code is not 200!")

                if log:
                    logging.error("HTTP response code is not 200!")
                    logging.info("-- Finish --------------------------------------------------------")

                sys.exit(1)

        for elem in not_sync_lib_name:
            if debug:
                print("[DEBUG] Library unsynchronized: %s" % elem)
            if log:
                logging.debug("Library unsynchronized: %s" % elem)
    else:
        sync_status = 1             # 0 = sync warning, 1 = sync ok, 2 = sync not configured

    return now, clib_subscribed, not_sync_lib_name, sync_status
