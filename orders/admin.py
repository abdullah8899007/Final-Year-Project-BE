from django.contrib import admin
from .models import  Orders, Invoice

# Register your models here.

admin.site.register(Orders)
admin.site.register(Invoice)
# admin.site.register(Item)
# admin.site.register(OrderItem)
# admin.site.register(OrderDeal)

