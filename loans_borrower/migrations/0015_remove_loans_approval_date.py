# Generated by Django 4.1.7 on 2024-06-09 16:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loans_borrower', '0014_merge_0012_loans_approval_date_0013_payment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loans',
            name='approval_date',
        ),
    ]
