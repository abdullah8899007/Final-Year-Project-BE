# Generated by Django 4.2.10 on 2024-03-06 17:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0005_delete_mainbalance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymenthistory',
            name='customer_name',
        ),
    ]
