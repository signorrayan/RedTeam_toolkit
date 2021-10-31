import urllib3
import requests
import re


def scanner(ip):
    ip = ip.strip()
    url = f"https://{ip}/autodiscover/autodiscover.json?@mss.com/owa/?&Email=autodiscover/autodiscover.json%3F@mss.com"
    try:
        requests.packages.urllib3.disable_warnings(
            urllib3.exceptions.InsecureRequestWarning
        )
        req = requests.get(
            url, timeout=10, verify=False, allow_redirects=False
        )  # nosec
        if (req.status_code == 302) and (re.search("errorfe.aspx", req.text)):
            result = {"message": f"Host {ip} is vulnerable "}
        else:
            result = {"message": f"Host {ip} is not vulnerable"}
        return result

    except Exception:
        return None
