# from rich.console import Console
# from rich import box
# from rich.table import Table
import json
import os
import re
from concurrent.futures import ThreadPoolExecutor

import requests

# from http.cookies import SimpleCookie

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
methods = [
    "CHECKIN",
    "CHECKOUT",
    "CONNECT",
    "GET",
    "HEAD",
    "INDEX",
    "LINK",
    "LOCK",
    "MKCOL",
    "MOVE",
    "NOEXISTE",
    "ORDERPATCH",
    "OPTIONS",
    "POST",
    "PROPFIND",
    "PROPPATCH",
    "REPORT",
    "SEARCH",
    "SHOWMETHOD",
    "SPACEJUMP",
    "TEXTSEARCH",
    "TRACE",
    "TRACK",
    "UNLINK",
    "UNLOCK",
]
# Dangerious Methods: 'COPY', 'DELETE', 'PUT',  'PATCH', 'UNCHECKOUT',


# class Logger(object):
#    def __init__(self, verbosity=0, quiet=False):
#        self.verbosity = verbosity
#        self.quiet = quiet
#
#    def debug(self, message):
#        if self.verbosity == 2:
#            console.print("{}[DEBUG]{} {}".format("[yellow3]", "[/yellow3]", message), highlight=False)
#
#    def verbose(self, message):
#        if self.verbosity >= 1:
#            console.print("{}[VERBOSE]{} {}".format("[blue]", "[/blue]", message), highlight=False)
#
#    def info(self, message):
#        if not self.quiet:
#            console.print("{}[*]{} {}".format("[bold blue]", "[/bold blue]", message), highlight=False)
#
#    def success(self, message):
#        if not self.quiet:
#            console.print("{}[+]{} {}".format("[bold green]", "[/bold green]", message), highlight=False)
#
#    def warning(self, message):
#        if not self.quiet:
#            console.print("{}[-]{} {}".format("[bold orange3]", "[/bold orange3]", message), highlight=False)
#
#    def error(self, message):
#        if not self.quiet:
#            console.print("{}[!]{} {}".format("[bold red]", "[/bold red]", message), highlight=False)


# def get_options():
#    parser = argparse.ArgumentParser(
#        formatter_class=argparse.RawTextHelpFormatter,
#    )
#    parser.add_argument(
#        "url",
#        help="e.g. https://example.com:port/path"
#    )
#    parser.add_argument(
#        "-v",
#        "--verbose",
#        dest="verbosity",
#        action="count",
#        default=0,
#        help="verbosity level (-v for verbose, -vv for debug)",
#    )
#    parser.add_argument(
#        "-q",
#        "--quiet",
#        dest="quiet",
#        action="store_true",
#        default=False,
#        help="Show no information at all",
#    )
#    parser.add_argument(
#        "-k",
#        "--insecure",
#        dest="verify",
#        action="store_false",
#        default=True,
#        required=False,
#        help="Allow insecure server connections when using SSL (default: False)",
#    )
#    parser.add_argument(
#        "-L",
#        "--location",
#        dest="redirect",
#        action="store_true",
#        default=False,
#        required=False,
#        help="Follow redirects (default: False)",
#    )
#    parser.add_argument(
#        "-w",
#        "--wordlist",
#        dest="wordlist",
#        action="store",
#        default=None,
#        required=False,
#        help="HTTP methods wordlist (default is a builtin wordlist)",
#    )
#    parser.add_argument(
#        "-t",
#        "--threads",
#        dest="threads",
#        action="store",
#        type=int,
#        default=5,
#        required=False,
#        help="Number of threads (default: 5)",
#    )
#    parser.add_argument(
#        "-j",
#        "--jsonfile",
#        dest="jsonfile",
#        default=None,
#        required=False,
#        help="Save result to specified JSON file.",
#    )
#    parser.add_argument(
#        '-b', '--cookies',
#        action="store",
#        default=None,
#        dest='cookies',
#        help='Specify cookies to use in requests. (e.g., --cookies "cookie1=blah;cookie2=blah")'
#    )
#
#    options = parser.parse_args()
#    return options


# def methods_from_wordlist(wordlist):
#    logger.verbose(f"Retrieving methods from wordlist {wordlist}")
#    try:
#        with open(options.wordlist, "r") as infile:
#            methods += infile.read().split()
#    except Exception:
#        pass
#        logger.error(f"Had some kind of error loading the wordlist ¯\_(ツ)_/¯: {e}")


def methods_from_http_options(console, target_url, options, proxies, cookies):
    options_methods = []
    # logger.verbose("Pulling available methods from server with an OPTIONS request")
    try:
        r = requests.options(
            url=target_url, proxies=proxies, cookies=cookies, verify=options.verify
        )
    except requests.exceptions.ProxyError:
        # logger.error("Invalid proxy specified ")
        raise SystemExit
    if r.status_code == 200:
        # logger.verbose("URL accepts OPTIONS")
        # logger.debug(r.headers)
        if "Allow" in r.headers:
            # logger.info("URL answers with a list of options: {}".format(r.headers["Allow"]))
            include_options_methods = console.input(
                "[bold orange3][?][/bold orange3] Do you want to add these methods to the test (be careful, some methods can be dangerous)? [Y/n] "
            )
            if not include_options_methods.lower() == "n":
                for method in r.headers["Allow"].replace(" ", "").split(","):
                    if method not in options_methods:
                        # logger.debug(f"Adding new method {method} to methods")
                        options_methods.append(method)
                    else:
                        pass
                        # logger.debug(f"Method {method} already in known methods, passing")
            else:
                pass
                # logger.debug("Methods found with OPTIONS won't be added to the tested methods")
        else:
            pass
            # logger.verbose("URL doesn't answer with a list of options")
    else:
        pass
        # logger.verbose("URL rejects OPTIONS")
    return options_methods


def test_method(method, target_url, proxies, cookies, result):
    try:
        r = requests.request(
            method=method,
            url=target_url,
            # verify=options.verify,  # this is to set the client to accept insecure servers
            proxies=proxies,
            cookies=cookies,
            # allow_redirects=options.redirect,
            stream=False,  # If True, this is to prevent the download of huge files, focus on the request, not on the data
        )
    except requests.exceptions.ProxyError:
        # logger.error("Invalid proxy specified ")
        raise SystemExit
    # logger.debug(f"Obtained result: {method}, {str(r.status_code)}, {str(len(r.text))}, {r.reason}")
    result[method] = {
        "status_code": r.status_code,
        "length": len(r.text),
        "reason": r.reason[:100],
    }


# def print_result(console, result):
#    logger.verbose("Parsing & printing result")
#    table = Table(show_header=True, header_style="bold blue", border_style="blue", box=box.SIMPLE)
#    table.add_column("Method")
#    table.add_column("Length")
#    table.add_column("Status code")
#    table.add_column("Reason")
#    for result in result.items():
#        if result[1]["status_code"] == 200:  # This means the method is accepted
#            style = "green"
#        elif (300 <= result[1]["status_code"] <= 399):
#            style = "cyan"
#        elif 400 <= result[1]["status_code"] <= 499:  # This means the method is disabled in most cases
#            style = "red"
#        elif (500 <= result[1]["status_code"] <= 599) and result[1][
#            "status_code"] != 502:  # This means the method is not implemented in most cases
#            style = "orange3"
#        elif result[1]["status_code"] == 502:  # This probably means the method is accepted but request was malformed
#            style = "yellow4"
#        else:
#            style = None
#        table.add_row(result[0], str(result[1]["length"]), str(result[1]["status_code"]), result[1]["reason"], style=style)
#    console.print(table)


def json_export(result, tg, user_name):
    directory = f"{BASE_DIR}/../media/toolkit/verbtampering/{user_name}"
    os.makedirs(directory, exist_ok=True)
    with open(f"{directory}/{tg}", "w") as f:
        f.write(json.dumps(result, indent=4) + "\n")


def start(target_url, user_name):
    # logger.info("Starting HTTP verb enumerating and tampering")
    global methods, tg
    result = {}
    proxies = None

    # Parsing cookie option
    # if options.cookies:
    #    cookie = SimpleCookie()
    #    cookie.load(options.cookies)
    #    cookies = {key: value.value for key, value in cookie.items()}
    # else:
    #    cookies = {}
    cookies = {}
    #
    # if options.wordlist is not None:
    #    methods += methods_from_wordlist(options.wordlist)
    # methods += methods_from_http_options(console, options, proxies, cookies)

    # Sort uniq
    methods = [m.upper() for m in methods]
    methods = sorted(set(methods))

    # Filtering for ous methods
    # filtered_methods = []
    # for method in methods:
    #    if method in ["DELETE", "COPY", "PUT", "PATCH", "UNCHECKOUT"]:
    #        test_dangerous_method = console.input(
    #            f"[bold orange3][?][/bold orange3] Do you really want to test method {method} (can be dangerous)? \[y/N] ")
    #        if not test_dangerous_method.lower() == "y":
    #            logger.verbose(f"Method {method} will not be tested")
    #        else:
    #            logger.verbose(f"Method {method} will be tested")
    #            filtered_methods.append(method)
    #    else:
    #        filtered_methods.append(method)
    # methods = filtered_methods[:]
    # del filtered_methods

    # Waits for all the threads to be completed
    with ThreadPoolExecutor(max_workers=min(8, len(methods))) as tp:
        for method in methods:
            tp.submit(test_method, method, target_url, proxies, cookies, result)

    # Sorting the result by method name
    result = {key: result[key] for key in sorted(result)}

    # Parsing and print result
    # print_result(console, result)
    # Export to JSON
    if len(result) == 0:
        return None
    else:
        if re.match("http\w?://\w+\.\w+", target_url):
            tg = target_url.split("/")[2]
            json_export(result, tg, user_name)
        return result


# options = get_options()
# logger = Logger(options.verbosity, options.quiet)
# console = Console()
# if not options.verify:
#    # Disable warings of insecure connection for invalid cerificates
#    requests.packages.urllib3.disable_warnings()
#    # Allow use of deprecated and weak cipher methods
#    requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
#    try:
#        requests.packages.urllib3.contrib.pyopenssl.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
#    except AttributeError:
#        pass
