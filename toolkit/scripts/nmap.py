import subprocess

from .checksum import check
from .ctpdf import convert_to_pdf


def nmap_script(ip, user_name, function_name):
    # "-sS", "-T5", "-sV", "-Pn", "-O", "-A", "-sC",
    command = ["nmap", "-sT", "-sV", "-T5", "-Pn", "--script", "vulners", f"{ip}"]

    p = subprocess.run(
        command,
        capture_output=True,
        encoding="utf-8",
    )
    pre_output = p.stdout.split("\n")
    pre_output = pre_output[4:-3]

    output = pre_output.copy()
    for line in pre_output:
        if "MSF" in line or "EXPLOITPACK" in line:
            output.remove(line)

    if check():
        convert_to_pdf(output, user_name, ip, function_name)
    else:
        exit(1)
