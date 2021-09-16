from django.contrib.auth.models import User

# from django.core.validators import RegexValidator, validate_ipv46_address
from django.db import models

# validate_hostname = RegexValidator(regex=r'[a-zA-Z0-9-_]*\.[a-zA-Z]{2,6}')


class Report(models.Model):
    ip = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    report_file = models.FileField(upload_to="reports/%Y/%m/%d")
    report_date = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
