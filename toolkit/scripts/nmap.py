import subprocess
from .ctpdf import convert_to_pdf
from .checksum import check
import multiprocessing
#import re


def nmap_script(ip, user_name, function_name):
    #"-sS", "-T5", "-sV", "-Pn", "-O", "-A", "-sC",
    p = subprocess.run(["nmap", "-sT", "-sV", "-T5", "-Pn", "--script", "vulners", f"{ip}"],
                       capture_output=True, encoding="utf-8")
    output = p.stdout.split('\n')
    output = output[4:-3]

    if check():
        convert_to_pdf(output, user_name, ip, function_name)
    else:
        exit(1)