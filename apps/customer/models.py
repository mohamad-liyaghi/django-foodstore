from django.db import models
from restaurant.models import  Food
from django.contrib.auth import get_user_model
# Create your models here.

class Order(models.Model):
    class status(models.TextChoices):
        ordered = "ordered"
        preparing = "preparing"
        sending = "sending"
        arrived = "Arrived"

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='orders')
    items = models.ManyToManyField(Food, blank=True)
    orderid = models.CharField(max_length=15, blank=True)
    total_price = models.IntegerField(blank=True)

    is_paid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    status = models.CharField(choices=status.choices, default=status.ordered, max_length= 10)

    def __str__(self):
        return self.orderid

