from django.db import models

class Deposit(models.Model):
    application_no = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    account_name = models.CharField(max_length=100)
    reference_number = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
