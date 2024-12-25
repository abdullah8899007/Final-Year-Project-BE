from django.db import models
# from django.contrib.auth.models import User
from custom_user.models import User
from customers.models import CustomersModel

class Table(models.Model):
    AVAILABLE = "Available"
    OCCUPIED = "Occupied"
    STATUS_CHOICES = [
        (AVAILABLE, 'Available'),
        (OCCUPIED, 'Occupied'),
    ]

    table_number = models.IntegerField(unique=True)
    seating_size = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return f"Table {self.table_number} ({self.status})"

class Reservation(models.Model):
    CONFIRMED = "Confirmed"
    ENDED = "Ended"

    STATUS_CHOICES = [
        (CONFIRMED, 'Confirmed'),
        (ENDED, 'Ended'),
    ]

    user = models.ForeignKey(CustomersModel, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    booking_time = models.DateTimeField()

    def __str__(self):
        return f"Reservation for {self.user} at {self.table} ({self.status})"
