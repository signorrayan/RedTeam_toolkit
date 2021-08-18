import subprocess
from .ctpdf import convert_to_pdf
import re

def dirscan_script(ip, user_name,full_name, function_name):
    #p = subprocess.run(["python3", "/home/pytm/dirsearch/dirsearch.py", "--quiet", "-u", f"{ip}"],
    #                   capture_output=True, encoding="utf-8")

    p = subprocess.run(["dirhunt", f"{str(ip)}"], capture_output=True, encoding='utf-8') #

    ansi_escape = re.compile(r'\\x1b(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    result = ansi_escape.sub('', str(p))
    output = re.findall(r"http\w?://[^\)]+\)|\s*\S+\s+to\:\s+[^\\]*", result) #


    if check():
        convert_to_pdf(output[2:-1], user_name, ip, function_name)


#user_name = "sarayloo"
#ip = "roadstershop.com"
#function_name = "dirscan"
#full_name = "Mohammadreza Sarayloo"
#dirscan_script(ip,user_name, full_name, function_name)