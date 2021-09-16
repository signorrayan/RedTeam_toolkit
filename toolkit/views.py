import multiprocessing
import os

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http.response import (
    Http404,
    HttpResponse,
    StreamingHttpResponse,
)
from django.shortcuts import, redirect, render

from .forms import CvedesForm, IpscanForm, SshbruteForm
from .scripts import cvescanner, dirscanner, nmap, rdpbrute, rustscan, sshbrute

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


@login_required(login_url="/login/")
def dashboard(request):
    if request.method == "GET":
        return render(request, "toolkit/dashboard.html")


@login_required(login_url="/login/")
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


@login_required(login_url="/login/")
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


@login_required(login_url="/login/")
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


def stream(request):
    response = StreamingHttpResponse()  # Accept generator/yield
    response["Content-Type"] = "text/event-stream"
    return response


@login_required(login_url="/login/")
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


@login_required(login_url="/login/")
def linux(request):
    return render(request, "toolkit/linux/home.html")


@login_required(login_url="/login/")
def windows(request):
    return render(request, "toolkit/linux/home.html")


@login_required(login_url="/login/")
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


@login_required(login_url="/login/")
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


@login_required(login_url="/login/")
def nightmare(request):
    return render(request, "toolkit/fullscan.html")


@login_required(login_url="/login/")
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


@login_required(login_url="/login/")
def logoutuser(request):
    if request.method == "POST":
        logout(request)
        return redirect("home")
