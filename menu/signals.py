from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Item


@receiver(post_save, sender=Item)
def update_category_count(sender, instance, created, **kwargs):
    if created:
        instance.category.count += 1
        instance.category.save()