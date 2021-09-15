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
