# Generated by Django 4.1.7 on 2024-06-09 04:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loans_borrower', '0011_alter_payment_amount_due'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Payment',
        ),
    ]
