from celery import shared_task
from Restaurant.celery import app
from .models import *

from django.utils import timezone
from datetime import timedelta

@shared_task
def update_order_status():
    try:
        orders = Orders.objects.filter(order_status=Orders.READY)
        for order in orders:
            order.status = Orders.COMPLETED
            order.save()
    except Orders.DoesNotExist:
        pass