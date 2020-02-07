#!/bin/env python
from ansible.module_utils.basic import *
import os
import json
import re
import sys

import requests
import urllib3
urllib3.disable_warnings()


#! server
IP_ADDRESS = "https://172.20.10.5:3780"
USERNAME = "jamnexpose"
PASSWORD = "@Public1234567890"


def nexpose_create(ip):
    # ! POST    https://192.168.1.31:3780/api/3/sites

    PARAMS = {

        "name": ip,
        "scan":
        {
            "assets":
            {
                "includedTargets":
                {
                    "addresses":
                    [
                        ip
                    ]
                }
            }
        }
    }

    url = IP_ADDRESS + "/api/3/sites"
    resp = requests.request("POST", url, data=json.dumps(PARAMS), auth=(
        USERNAME, PASSWORD), verify=False, headers={'Content-type': 'application/json'})

    parsed = json.loads(resp.content)
    #print(json.dumps(parsed, indent=4, sort_keys=True))

    # print(resp)
    obj = None
    try:
        obj = json.loads(resp.content)
    except ValueError:
        print("*** error loading JSON ***")

    # print("............................")

    if resp.status_code == 201:  # create
        # this ID will be used to run the process "Start Scan"
        # print(obj["id"])

        # start scan

        # ! POST  https://192.168.1.31:3780/api/3/sites/18/scans

        url = IP_ADDRESS + "/api/3/sites/" + str(obj["id"]) + "/scans"
        resp = requests.request("POST", url, data=json.dumps(PARAMS), auth=(
            USERNAME, PASSWORD), verify=False, headers={'Content-type': 'application/json'})
        parsed = json.loads(resp.content)
        #print(json.dumps(parsed, indent=4, sort_keys=True))
        # print(resp)
        return(" --- Asset has been created and is being scanned --- " + str(resp))

    else:
        #print("...other status codes...")
        return(" --- Asset is duplicate --- !!! " + str(resp))


if __name__ == '__main__':
    fields = {
        "targetIP": {"required": True, "type": "str"}
    }
    module = AnsibleModule(argument_spec=fields)
    targetIP = os.path.expanduser(module.params['targetIP'])
    returnMessage = nexpose_create(targetIP)
    module.exit_json(msg=returnMessage)
