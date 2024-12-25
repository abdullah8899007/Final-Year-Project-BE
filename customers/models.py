from django.db import models

# Create your models here.

class CustomersModel(models.Model):
    # Define your fields here
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.name