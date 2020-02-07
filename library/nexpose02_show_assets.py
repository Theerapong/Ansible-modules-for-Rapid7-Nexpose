#!/usr/bin/python

from ansible.module_utils.basic import *

# ! ....
import json
import requests
import urllib3
import ast
urllib3.disable_warnings()
#! home
IP_ADDRESS = "https://172.20.10.5:3780"
USERNAME = "jamnexpose"
PASSWORD = "@Public1234567890"
#! home
# IPADDRESS_OF_TARGET="192.168.0.128"
#NAME_OF_TARGET="Test Fedora 192.168.1.6"


def show_table(data):

    is_error = False
    has_changed = False
    number_of_row = data['number_of_roll']
    res = []
    i = 0

    # ! show all assets , and select asset
    # ! GET https://192.168.1.9:3780/api/3/assets
    url = IP_ADDRESS + "/api/3/assets"
    resp = requests.request("GET", url, auth=(
        USERNAME, PASSWORD), verify=False, headers={'Content-type': 'application/json'})
    parsed = json.loads(resp.content)
    obj = None
    obj = json.loads(resp.content)
    count_hosts = len(obj['resources'])
    str_overall = "Number of asset (host, ip) : " + str(count_hosts)

    for i in range(count_hosts):

        hostnameStr = ""
        try:
            hostnameStr = obj['resources'][i]['hostName']
        except:
            hostnameStr = "-"

        result = {
            "Hostname ": hostnameStr,
            "IP       ": obj['resources'][i]['ip'],
            "Asset ID ": str(obj['resources'][i]['id'])
        }
        res.append(result)

    # show_message_if_scan_status_is_in_progress
    url = IP_ADDRESS + "/api/3/scans"
    resp = requests.request("GET", url, auth=(
        USERNAME, PASSWORD), verify=False, headers={'Content-type': 'application/json'})
    obj = json.loads(resp.content)
    count_vul = len(obj['resources'])
    for i in range(count_vul):
        try:
            if obj['resources'][i]['status'] == "running":
                result = {
                    " --- Alert --- ": " --- Some assets are being scanned , please wait --- "
                }
                res.append(result)

        except:
            result = {
                "--- Error ---": "--- some assets are being scanned ---"
            }
            res.append(result)
    ######################################

    resp = {
        str_overall: res
    }
    meta = {" Nexpose ": resp}

    return is_error, has_changed, meta


def main():
    fields = {
        "number_of_roll": {
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
