from django.db import models
from restaurant.models import Food
from django.contrib.auth import get_user_model
from accounts.utils.token_generator import random_number


class Order(models.Model):
    
    class status(models.TextChoices):
        ordered = "Ordered"
        preparing = "Preparing"
        sending = "Sending"
        arrived = "Arrived"

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='orders')
    order_id = models.CharField(max_length=15, default=random_number)

    is_paid = models.BooleanField(default=False)

    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=status.choices, default=status.ordered, max_length=10)

    @property
    def total_price(self):        
        total = sum(item.price() for item in self.items.all())
        return total

    def __str__(self):
        return str(self.order_id)


class OrderItem(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Food, on_delete=models.CASCADE)

    quantity = models.IntegerField(default=1)
    
    prepared = models.BooleanField(default=False)

    def price(self):
        return self.item.price * self.quantity

    def __str__(self):
        return self.order.order_id