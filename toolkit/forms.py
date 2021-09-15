from django.forms import ModelForm
from .models import Report
from django import forms


class IpscanForm(ModelForm):
    class Meta:
        model = Report
        fields = ["ip"]


class CvedesForm(forms.Form):
    cve_id = forms.CharField(max_length=15)


class SshbruteForm(forms.Form):
    username = forms.CharField(max_length=20)
    ip = forms.GenericIPAddressField()
