from django import forms
from django.forms import ModelForm

from .models import Report


class IpscanForm(ModelForm):
    class Meta:
        model = Report
        fields = ["ip"]


class CvedesForm(forms.Form):
    cve_id = forms.CharField(max_length=15)


class SshbruteForm(forms.Form):
    username = forms.CharField(max_length=20)
    ip = forms.GenericIPAddressField()
    port = forms.IntegerField(max_value=65535)


class IpCommandForm(forms.Form):
    target = forms.GenericIPAddressField()
    command = forms.CharField(max_length=150)


class URLForm(forms.Form):
    target_url = forms.CharField()


class SubDomainForm(forms.Form):
    target_url = forms.CharField()
    fast_scan = forms.BooleanField(required=False)
