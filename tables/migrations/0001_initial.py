# Generated by Django 4.2.10 on 2024-02-26 11:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table_number', models.IntegerField(unique=True)),
                ('seating_size', models.IntegerField()),
                ('status', models.CharField(choices=[('available', 'Available'), ('occupied', 'Occupied')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=100)),
                ('status', models.CharField(choices=[('confirmed', 'Confirmed'), ('ended', 'Ended')], max_length=20)),
                ('booking_time', models.DateTimeField()),
                ('table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tables.table')),
            ],
        ),
    ]