from pyexpat import model
from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
# from djmoney.models.fields import MoneyField
from django.conf import settings


import datetime

class AccountReg(models.Model):
    SEX = (
        ('F', 'Female'),
        ('M', 'Male'),
    )

    MARITAL_STATUS = (
        ('S', 'Single'),
        ('M', 'Married'),
        ('D', 'Divorced'),
        ('W', 'Widow'),
    )

    PREFIX = (
        ('MR', 'Mr.'),
        ('MRS', 'Mrs.'),
        ('MS', 'Ms.'),
    )

    YEARS= [x for x in range(1940,2022)]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    sex = models.CharField(max_length=100, choices=SEX)
    marital_status = models.CharField(max_length=100, choices=MARITAL_STATUS)
    birth_date= models.DateField(blank=True, null=True, max_length=8)
    email = models.EmailField()
    prefix = models.CharField(max_length=100, choices=PREFIX)
    phone = models.CharField(max_length=11, blank=True, null=True)
    address = models.CharField(max_length=300)

    def __str__(self):
        return '{} - {}'.format(self.user,self.email)

class BankAccount(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    deposit = models.DecimalField(decimal_places=2, max_digits=50)
    balance = models.DecimalField(default=0, decimal_places=2, max_digits=50, blank=True)
    deposit_id = models.CharField(max_length=100, unique=True, null=True)
    status = models.CharField(max_length=100, default='Pending')
    reference_number = models.CharField(max_length=100, null=True)

    def result(self):
        return '{}'.format(self.user)