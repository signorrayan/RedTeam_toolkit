import multiprocessing
import os

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http.response import Http404, HttpResponse, StreamingHttpResponse
from django.shortcuts import redirect, render

from .forms import CvedesForm, IpscanForm, SshbruteForm, SubDomainForm, URLForm
from .scripts import (
    cvescanner,
    dirscanner,
    nmap,
    rustscan,
    sshbrute,
)
from .scripts.windows import rdpbrute, proxyshell
from .scripts.webapp import gather_url, verbtampering, subdomain_finder, cve_2021_41773

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def home(request):
    return render(request, "toolkit/home.html")


def loginuser(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return render(request, "toolkit/dashboard.html")
        else:
            return render(request, "toolkit/login.html", {"form": AuthenticationForm()})

    else:
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user is None:
            return render(
                request,
                "toolkit/login.html",
                {"form": AuthenticationForm(), "error": "Invalid Username/Password"},
            )
        else:
            login(request, user)
            return redirect("dashboard")


@login_required(login_url="/forbidden/")
def dashboard(request):
    if request.method == "GET":
        return render(request, "toolkit/dashboard.html")


@login_required(login_url="/forbidden/")
def fullscan(request):
    if request.method == "GET":
        return render(request, "toolkit/fullscan.html", {"form": IpscanForm()})

    else:
        try:
            global ip, user_name, function_name
            form = IpscanForm(request.POST)
            if form.is_valid():
                ip = form.cleaned_data.get("ip")
                function_name = "fullscan"
                # validate_ipv46_address(ip) or RegexValidator("(?:http\w?://)?(?:www.)?[^\.]+.\w{2,8}")
                user_name = request.user
                p_fullscan = multiprocessing.Process(
                    target=nmap.nmap_script,
                    args=(
                        ip,
                        user_name,
                        function_name,
                    ),
                )
                p_fullscan.start()
                p_fullscan.join()
            # nmap.nmap_script(ip, user_name, function_name)

        except ValueError:
            return render(
                request,
                "toolkit/dashboard.html",
                {"error": "Bad data passed in. Try again."},
            )

    return render(request, "toolkit/download.html")


@login_required(login_url="/forbidden/")
def livehost(request):
    if request.method == "GET":
        return render(request, "toolkit/livehost.html", {"form": IpscanForm()})

    else:
        try:
            global ip, user_name, function_name
            form = IpscanForm(request.POST)
            if form.is_valid():
                ip = form.cleaned_data.get("ip")
            function_name = livehost.__name__
            user_name = request.user
            p_livehost = multiprocessing.Process(
                target=rustscan.rustscan_script,
                args=(
                    ip,
                    user_name,
                    function_name,
                ),
            )
            p_livehost.start()
            p_livehost.join()
            # rustscan.rustscan_script(ip, user_name, function_name)
            ip = str(ip).split("/")[0]

        except ValueError:
            return render(
                request,
                "toolkit/dashboard.html",
                {"form": IpscanForm()},
                {"error": "Bad data passed in. Try again."},
            )

    return render(request, "toolkit/download.html")


@login_required(login_url="/forbidden/")
def dirscan(request):
    if request.method == "GET":
        return render(request, "toolkit/dirscan.html", {"form": IpscanForm()})

    elif request.method == "POST":
        try:
            global ip, user_name, function_name
            form = IpscanForm(request.POST)
            if form.is_valid():
                ip = form.cleaned_data.get("ip")
            function_name = dirscan.__name__
            user_name = request.user
            response = StreamingHttpResponse(
                dirscanner.dirscan_script(ip, user_name, function_name)
            )  # Accept generator/yield
            response["Content-Type"] = "text/event-stream"
            return response

        except ValueError:
            return render(
                request,
                "toolkit/dashboard.html",
                {"form": IpscanForm()},
                {"error": "Bad data passed in. Try again."},
            )

    return render(request, "toolkit/download.html")


@login_required(login_url="/forbidden/")
def stream(request):
    response = StreamingHttpResponse()  # Accept generator/yield
    response["Content-Type"] = "text/event-stream"
    return response


@login_required(login_url="/forbidden/")
def cvedes(request):
    if request.method == "GET":
        return render(request, "toolkit/cvedes.html", {"form": CvedesForm()})

    else:
        try:
            global cve_id, user_name
            form = CvedesForm(request.POST)
            if form.is_valid():
                cve_id = form.cleaned_data.get("cve_id")
                user_name = request.user
                result = cvescanner.cve_search(cve_id)
                if result is None:
                    return render(
                        request,
                        "toolkit/cvedes.html",
                        {"error": "The requested CVE is not found."},
                    )
                else:
                    context = {"result": result}
                    return render(request, "toolkit/cvedes.html", context)

        except ValueError:
            return render(
                request,
                "toolkit/cvedes.html",
                {"error": "Bad data passed in. Try again."},
            )


# @login_required(login_url='/login/')
# def user_reports(request):
#   user_reports = models.Report.objects.filter(owner=request.user)
#   return render(request, 'yourhtmlfile.html', {'user_reports':user_reports})


@login_required(login_url="/forbidden/")
def linux(request):
    return render(request, "toolkit/linux/home.html")


# Windows Section


@login_required(login_url="/forbidden/")
def windows(request):
    return render(request, "toolkit/windows/index.html")


@login_required(login_url="/forbidden/")
def rdpbruteforce(request):
    if request.method == "GET":
        return render(
            request, "toolkit/windows/rdpbruteforce.html", {"form": IpscanForm()}
        )

    else:
        form = IpscanForm(request.POST)
        if form.is_valid():
            ip = form.cleaned_data.get("ip")
            result = rdpbrute.rdpbrute_script(ip)
            if result is not None:
                context = {"result": result}
                return render(request, "toolkit/windows/rdpbruteforce.html", context)

            else:
                return render(
                    request,
                    "toolkit/windows/rdpbruteforce.html",
                    {"error": "Not Found!"},
                )

        return render(
            request,
            "toolkit/windows/rdpbruteforce.html",
            {"error": "Bad data passed in. Try again."},
        )


@login_required(login_url="/forbidden/")
def win_proxyshell(request):
    if request.method == "GET":
        return render(
            request, "toolkit/windows/proxyshell.html", {"form": IpscanForm()}
        )

    else:
        form = IpscanForm(request.POST)
        if form.is_valid():
            ip = form.cleaned_data.get("ip")
            result = proxyshell.scanner(ip)
            if result is not None:
                context = {"result": result}
                return render(request, "toolkit/windows/proxyshell.html", context)

            else:
                return render(
                    request,
                    "toolkit/windows/proxyshell.html",
                    {
                        "error": "Something went wrong... Maybe there is not route to the target!"
                    },
                )

        return render(
            request,
            "toolkit/windows/proxyshell.html",
            {"error": "Bad data passed in. Try again."},
        )


@login_required(login_url="/forbidden/")
def nightmare(request):
    return render(request, "toolkit/fullscan.html")


# End Windows Section


@login_required(login_url="/forbidden/")
def sshbruteforce(request):
    if request.method == "GET":
        return render(request, "toolkit/sshbruteforce.html", {"form": SshbruteForm()})

    else:
        form = SshbruteForm(request.POST)
        if form.is_valid():
            target_username = form.cleaned_data.get("username")
            target_ip = form.cleaned_data.get("ip")
            result = sshbrute.ssh_bruteforce(target_username, target_ip)
            if result is not None:
                context = {"result": result}
                return render(request, "toolkit/sshbruteforce.html", context)

            else:
                return render(
                    request, "toolkit/sshbruteforce.html", {"error": "Not Found!"}
                )

        return render(
            request,
            "toolkit/sshbruteforce.html",
            {"error": "Bad data passed in. Try again."},
        )


# Web Application Section


@login_required(login_url="/forbidden/")
def webapp(request):
    if request.method == "GET":
        return render(request, "toolkit/webapp/index.html")


@login_required(login_url="/forbidden/")
def verbtamper(request):
    if request.method == "GET":
        return render(request, "toolkit/webapp/verbtampering.html", {"form": URLForm()})

    else:
        try:
            global target_url, user_name
            form = URLForm(request.POST)
            if form.is_valid():
                target_url = form.cleaned_data.get("target_url")
                user_name = request.user
                result = verbtampering.start(target_url, user_name)
                if result is None:
                    return render(
                        request,
                        "toolkit/webapp/verbtampering.html",
                        {"error": "Bad URL Passed in, Try again..."},
                    )
                else:
                    context = {"result": result.items(), "target_url": target_url}
                    return render(request, "toolkit/webapp/verbtampering.html", context)

        except ValueError:
            return render(
                request,
                "toolkit/webapp/verbtampering.html",
                {"error": "Bad data passed in. Try again."},
            )


@login_required(login_url="/forbidden/")
def webcrawler(request):
    if request.method == "GET":
        return render(request, "toolkit/webapp/webcrawler.html", {"form": URLForm()})

    else:
        try:
            global target_url
            form = URLForm(request.POST)
            if form.is_valid():
                target_url = form.cleaned_data.get("target_url")
                result = gather_url.get(target_url)
                if result is None:
                    return render(
                        request,
                        "toolkit/webapp/webcrawler.html",
                        {"error": "Bad URL Passed in, Try again..."},
                    )

                else:
                    context = {"result": result, "target_url": target_url}
                    return render(request, "toolkit/webapp/webcrawler.html", context)

        except ValueError:
            return render(
                request,
                "toolkit/webapp/webcrawler.html",
                {"error": "Bad data passed in. Try again."},
            )


@login_required(login_url="/forbidden/")
def subdomain(request):
    if request.method == "GET":
        return render(
            request, "toolkit/webapp/subdomain.html", {"form": SubDomainForm()}
        )

    else:
        try:
            global target_url
            form = SubDomainForm(request.POST)
            if form.is_valid():
                target_url = form.cleaned_data.get("target_url")
                fast_scan = form.cleaned_data.get("fast_scan")
                if fast_scan:
                    result = subdomain_finder.sublister(target_url)
                    if result is None:
                        return render(
                            request,
                            "toolkit/webapp/subdomain.html",
                            {"error": "Bad URL Passed in, Try again..."},
                        )

                    else:
                        context = {"result": result, "target_url": target_url}
                        return render(request, "toolkit/webapp/subdomain.html", context)

                else:
                    target_url = (
                        str(target_url).replace("https://", "").replace("http://", "")
                    )
                    response = StreamingHttpResponse(
                        subdomain_finder.knockpy(target_url)
                    )  # Accept generator/yield
                    response["Content-Type"] = "text/event-stream"
                    return response

        except ValueError:
            return render(
                request,
                "toolkit/webapp/subdomain.html",
                {"error": "Bad data passed in. Try again."},
            )


@login_required(login_url="/forbidden/")
def apache_cve_41773(request):
    if request.method == "GET":
        return render(
            request, "toolkit/webapp/cve_2021_41773.html", {"form": IpscanForm()}
        )

    else:
        form = IpscanForm(request.POST)
        if form.is_valid():
            ip = form.cleaned_data.get("ip")
            result = cve_2021_41773.start(ip)
            if result is not None:
                context = {"result": result}
                return render(request, "toolkit/webapp/cve_2021_41773.html", context)

            else:
                return render(
                    request,
                    "toolkit/webapp/cve_2021_41773.html",
                    {"error": "Something went wrong..."},
                )

        return render(
            request,
            "toolkit/webapp/cve_2021_41773.html",
            {"error": "Bad data passed in. Try again."},
        )


# End WebApplication Section


@login_required(login_url="/forbidden/")
def download_file(request):
    filename = f"{function_name}-{ip}.pdf"
    # Define the full file path
    user_name = request.user
    filepath = f"{BASE_DIR}/toolkit/media/toolkit/reports/{user_name}/{filename}"
    # Open the file for reading content
    if os.path.exists(filepath):
        # Set the return value of the HttpResponse
        response = HttpResponse(open(filepath, "rb"))
        # Set the HTTP header for sending to browser
        response["Content-Disposition"] = "attachment; filename=%s" % filename
        return response
    # Return the response value
    else:
        raise Http404


@login_required(login_url="/forbidden/")
def logoutuser(request):
    if request.method == "POST":
        logout(request)
        return redirect("home")

    else:
        return render(request, "toolkit/home.html")


def forbidden(request):
    if request.method == "GET":
        return render(request, "toolkit/403.html")
