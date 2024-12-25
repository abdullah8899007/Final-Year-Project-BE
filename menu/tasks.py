from celery import shared_task
from Restaurant.celery import app

from .models import Deal
from django.utils import timezone
from datetime import timedelta


@shared_task
def update_expired_deals():
    current_date = timezone.now().date()
    print(current_date)
    expired_deals = Deal.objects.filter(end_date__lte=current_date, status=True)

    expired_deals |= Deal.objects.filter(end_date=current_date, status=True)

    for deal in expired_deals:
        deal.status = False
        deal.save()