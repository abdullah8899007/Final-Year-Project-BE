# Generated by Django 4.2.10 on 2024-03-06 18:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0009_alter_paymenthistory_customer_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='paymenthistory',
            old_name='customer_name',
            new_name='name',
        ),
    ]