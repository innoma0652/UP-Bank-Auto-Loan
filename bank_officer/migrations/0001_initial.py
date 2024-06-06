# Generated by Django 5.0.6 on 2024-06-05 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Deposit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('application_no', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=100)),
                ('account_name', models.CharField(max_length=100)),
                ('reference_number', models.CharField(max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]
