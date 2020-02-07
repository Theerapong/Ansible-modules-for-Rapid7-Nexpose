#!/bin/env python
from ansible.module_utils.basic import *
import os
import json
import re
import sys


import json
import requests
import urllib3
import ast
#from tabulate import tabulate
urllib3.disable_warnings()
# ! ....
urllib3.disable_warnings()
#! home
IP_ADDRESS = "https://172.20.10.5:3780"
USERNAME = "jamnexpose"
PASSWORD = "@Public1234567890"
# ! home
# IPADDRESS_OF_TARGET="192.168.0.128"
#NAME_OF_TARGET="Test Fedora 192.168.1.6"


def show_table(data):

    is_error = False
    has_changed = False
    assetID = data['assetID']
    res = []
    i = 1
    count_vul = 0
    try:
        # ! show VULNERABILITIES of selected asset
        # ! GET https://192.168.1.31:3780/api/3/assets/{id}/vulnerabilities
        #url = IP_ADDRESS + "/api/3/assets/" + assetNumber + "/vulnerabilities"
        url = IP_ADDRESS + "/api/3/assets/" + str(assetID) + "/vulnerabilities"
        resp = requests.request("GET", url, auth=(
            USERNAME, PASSWORD), verify=False, headers={'Content-type': 'application/json'})
        parsed = json.loads(resp.content)
        obj = json.loads(resp.content)
        count_vul = len(obj['resources'])
        str1 = "number of vulnerabilities : " + str(count_vul)

        title = ""
        cves = ""
        cvssV2 = ""
        cvssV3 = ""
        desc = ""

        for i in range(count_vul):
            id_of_vulnerability = obj['resources'][i]['id']

            # ! show details of each CVSS
            # ! https://192.168.1.31:3780/api/3/vulnerabilities/msft-cve-2017-0146
            url = IP_ADDRESS + "/api/3/vulnerabilities/" + id_of_vulnerability
            resp = requests.request("GET", url, auth=(
                USERNAME, PASSWORD), verify=False, headers={'Content-type': 'application/json'})
            parsed = json.loads(resp.content)
            #print(json.dumps(parsed, indent=4, sort_keys=True))
            obj_of_CVSS = json.loads(resp.content)
            try:
                # title
                title = obj_of_CVSS['title']
            except:
                title = " - "
            try:
                # cves
                cves = obj_of_CVSS['cves'][0]
            except:
                cves = " - "

            try:
                # cvssV2
                cvssV2 = str(obj_of_CVSS['cvss']['v2']['score'])
            except:
                cvssV2 = " - "

            try:
                # cvssV3
                cvssV3 = str(obj_of_CVSS['cvss']['v3']['score'])
            except:
                cvssV3 = " - "

            try:
                # desc
                desc = str(obj_of_CVSS['description']['text'])
            except:
                desc = " - "

            result = {
                "1 ID      ": obj['resources'][i]['id'],
                "2 Title   ": title,
                "3 CVES    ": cves,
                "4 CVSS v2 ": cvssV2,
                "5 CVSS v3 ": cvssV3,
                "6 Desc    ": desc
            }
            res.append(result)

    except:

        result = {
            " --- Error --- ": " --- No asset ID number " + str(assetID) + " --- "
        }
        res.append(result)

    resp = {
        "Number of vulnerabilities : " + str(count_vul): res
    }
    meta = {"Nexpose": resp}

    return is_error, has_changed, meta


def main():
    fields = {
        "assetID": {
            "required": False,
            "default": 1,
            "type": "int"
        },
    }

    module = AnsibleModule(argument_spec=fields)

    is_error, has_changed, result = show_table(module.params)

    if not is_error:
        module.exit_json(changed=has_changed, meta=result)
    else:
        module.fail_json(msg="Error playing dice", meta=result)


if __name__ == '__main__':
    main()
