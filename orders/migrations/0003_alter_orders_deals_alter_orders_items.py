# Generated by Django 4.2.10 on 2024-03-05 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_alter_orders_order_type_alter_orders_total_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='deals',
            field=models.JSONField(),
        ),
        migrations.AlterField(
            model_name='orders',
            name='items',
            field=models.JSONField(),
        ),
    ]
