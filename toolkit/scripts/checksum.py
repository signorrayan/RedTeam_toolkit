import os
import subprocess

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def check():
    p = subprocess.run(
        ["sha1sum", f"{BASE_DIR}/static/toolkit/c.bin"],
        capture_output=True,
        encoding="utf-8",
    )

    output = p.stdout.split()[0]
    if output == "4867b36bd83214c903d6ba6e79e216cedeef6ec1":
        return True
    else:
        return False
