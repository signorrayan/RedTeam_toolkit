import urllib3
import requests
import sys
import re


requests.packages.urllib3.disable_warnings()


def scanner(ip):
    ip = ip.strip()
    url = f"https://{ip}/autodiscover/autodiscover.json?@mss.com/owa/?&Email=autodiscover/autodiscover.json%3F@mss.com"
    try:
        req = requests.get(url, timeout=10, verify=False, allow_redirects=False)
        if (req.status_code == 302) and (re.search("errorfe.aspx", req.text)):
            result = {"message": f"Host {ip} is vulnerable "}
        else:
            result = {"message": f"Host {ip} is not vulnerable"}
        return result

    except Exception:
        return None
