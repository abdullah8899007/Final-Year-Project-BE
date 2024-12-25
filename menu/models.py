from django.db import models
from django.forms import ValidationError


class DateTimeAbstractModel(models.Model):
    starting_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        abstract = True


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.TextField()
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'categories'


class Item(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.TextField()
    price = models.IntegerField()
    status = models.BooleanField(default=True)
    stock = models.PositiveIntegerField(default=10)
    sold = models.IntegerField(default=0)

    def __str__(self):
        return self.name



class Deal(DateTimeAbstractModel):
    name = models.CharField(max_length=100, unique=True)
    image = models.TextField()
    items = models.JSONField()
    discounted_price = models.IntegerField(default=0)
    status = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
    def clean(self):
        if self.end_date < self.starting_date:
            raise ValidationError("End date cannot be earlier than start date.")

    def save(self, *args, **kwargs):
        self.clean()  # Run the clean method to check for validation
        super().save(*args, **kwargs)