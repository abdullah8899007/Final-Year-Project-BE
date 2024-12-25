from django.db import models
from custom_user.models import User


# Create your models here.

class UserInfoModel(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    phone=models.CharField(max_length=13, default="+920000000000")

    def __str__(self):
        return self.user.email
    