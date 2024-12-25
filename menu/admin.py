from django.contrib import admin
from .models import *
from tables.models import Reservation, Table
# Register your models here.

admin.site.register(Category)
admin.site.register(Deal)
admin.site.register(Item)

#tables
admin.site.register(Table)
admin.site.register(Reservation)
