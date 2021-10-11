# web crawler for gathering URLs
import os
import subprocess

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get(target_url):
    pre_output = subprocess.getoutput(
        f"echo {target_url} | {BASE_DIR}/webapp/hakrawler -t 15 -u"
    )
    if pre_output != "":
        result = pre_output.split("\n")
        return result

    else:
        return None
