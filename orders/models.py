from django.db import models
from django.core.exceptions import ValidationError
from menu.models import Item, Category, Deal
from random import randint
from django.db.models import F
from customers.models import CustomersModel


# Create your models here.
class Orders(models.Model):

    READY = 'Ready'
    ENQUEUE = 'Enqueue'
    COMPLETED = 'Completed'
    CANCEL = 'Cancel'

    My_Choices_status = [
        (READY, 'Ready'),
        (ENQUEUE, 'Enqueue'),
        (COMPLETED, 'Completed'),
        (CANCEL, 'Cancel'),
    ]


    LUNCH = "Lunch"
    DINNER = "Dinner"

    order_type_choices = [
        (LUNCH, 'Lunch'),
        (DINNER, 'Dinner'),
    ]

    customer = models.ForeignKey(CustomersModel, on_delete=models.CASCADE)
    items = models.JSONField(default=dict, null=True)
    deals = models.JSONField(default=dict, null=True)
    status = models.CharField(
        max_length=20, choices=My_Choices_status, default="Enqueue", null=False)
    orderType = models.CharField(max_length=25, choices=order_type_choices, null=False)
    total = models.PositiveIntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)


    def save(self, *args, **kwargs):
        if not self.items and not self.deals:
            raise ValidationError("Either 'items' or 'deals' must be provided.")
        
        if self.items:
            for item_data in self.items:
                try:
                    item = Item.objects.get(id=item_data['itemid'])
                    quantity = item_data['quantity']
                    if quantity > item.stock:
                        raise ValidationError(f"Quantity of item {item.name} exceeds available stock")
                    item.stock = F('stock') - quantity
                    item.sold = F('sold') + quantity
                    item.save(update_fields=['stock', 'sold'])
                except Item.DoesNotExist:
                    pass

        if self.deals:
            for deal_data in self.deals:
                try:
                    deal = Deal.objects.get(id=deal_data['dealid'])
                    deal_quantity = deal_data['stock']

                    items_data = deal.items
                    
                    for item_data in items_data:
                        item_name = item_data  
                        try:
                            item = Item.objects.get(name=item_name)
                            item_quantity = items_data[item_name]
                            if item_quantity * deal_quantity > item.stock:
                                raise ValidationError(f"Quantity of deal {deal.name} exceeds available stock for item {item.name}")
                            item.stock = F('stock') - item_quantity * deal_quantity
                            item.sold = F('sold') + item_quantity * deal_quantity
                            item.save(update_fields=['stock', 'sold'])
                        except Item.DoesNotExist:
                            pass
                except Deal.DoesNotExist:
                    pass

        # for item_name, quantity in self.items.items():
        #     try:
        #         item = Item.objects.get(name=item_name)
        #         if quantity > item.stock:
        #             raise ValidationError(f"Quantity of {item_name} exceeds available stock")
        #         item.stock = F('stock') - quantity
        #         item.sold = F('sold') + quantity
        #         item.save(update_fields=['stock', 'sold'])
        #     except Item.DoesNotExist:
        #         pass

        # for deal_name, quantity in self.deals.items():
        #     try:
        #         deal = Deal.objects.get(name=deal_name)
        #         for item_name, item_quantity in deal.items.items():
        #             try:
        #                 item = Item.objects.get(name=item_name)
        #                 if item_quantity * quantity > item.stock:
        #                     raise ValidationError(f"Quantity of {deal_name} exceeds available stock for item {item_name}")
        #                 item.stock = F('stock') - item_quantity * quantity
        #                 item.sold = F('sold') + item_quantity * quantity
        #                 item.save(update_fields=['stock', 'sold'])
        #             except Item.DoesNotExist:
        #                 pass
        #     except Deal.DoesNotExist:
        #         pass

        super().save(*args, **kwargs)

    def __str__(self):
        return self.customer.name

    class Meta:
        verbose_name_plural = "Orders"



class Invoice(models.Model):
    invoice_id = models.PositiveBigIntegerField(editable=False, unique=True)
    order = models.OneToOneField(
        Orders, on_delete=models.CASCADE, related_name='invoice')
    issued_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.invoice_id:
            self.invoice_id = randint(100000, 999999)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Invoice {self.invoice_id} for order {self.order_id}"