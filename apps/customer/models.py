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
    items = models.ManyToManyField(Food, blank=True)
    prepared_items = models.ManyToManyField(Food, blank=True, related_name="prepared_items")
    orderid = models.CharField(max_length=15, default=random_number)
    total_price = models.IntegerField(blank=True)

    is_paid = models.BooleanField(default=False)

    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=status.choices, default=status.ordered, max_length= 10)

    def __str__(self):
        return str(self.orderid)

