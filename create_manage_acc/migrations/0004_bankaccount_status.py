# Generated by Django 4.2.1 on 2024-06-07 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('create_manage_acc', '0003_bankaccount_deposit_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='bankaccount',
            name='status',
            field=models.CharField(default='Pending', max_length=100),
        ),
    ]
