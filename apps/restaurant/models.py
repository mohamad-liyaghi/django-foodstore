from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from star_ratings.models import Rating
from django.urls import reverse
from accounts.models import User
from accounts.utils.validators import validate_file_size
from accounts.utils.token_generator import random_number


class Restaurant(models.Model):
    
    class Status(models.TextChoices):
        '''Restaurant Status'''
        PENDING = ("p", "pending")
        ACCEPTED = ("a", "Accepted")
        REJECTED = ("r", "Rejected")
        BLOCKED = ("b", "Blocked")

    name = models.CharField(max_length= 50)    
    
    picture = models.ImageField(upload_to= "restaurant/profile",
                                    validators=[validate_file_size,])
    description = models.TextField()

    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    detailed_address = models.CharField(max_length=120, blank=True)

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="restaurant")

    email = models.EmailField(max_length=70, unique=True)

    status = models.CharField(max_length=1, choices=Status.choices, default=Status.PENDING)
    token = models.CharField(max_length=15, default=random_number)
    date_registered = models.DateTimeField(auto_now_add=True)

    ratings = GenericRelation(Rating)

    @property
    def is_accepted(self):
        return bool(self.status == "a")
    
    @property
    def is_blocked(self):
        return bool(self.status == "b")

    def get_absolute_url(self):
        return reverse("restaurant:restaurant-profile",
                             kwargs={"id" : self.id, "token" : self.token})

    def __str__(self):
        return  self.name
    



class Food(models.Model):
    name = models.CharField(max_length= 120)
    picture = models.ImageField(upload_to="foods/")

    description = models.TextField()
    category = models.ManyToManyField("Category", related_name="food_category")
    provider = models.ForeignKey(Restaurant, on_delete=models.CASCADE, blank=True,
                 related_name="foods")

    inventory = models.PositiveIntegerField(default=0)

    price = models.PositiveIntegerField()

    token = models.CharField(max_length=15, default=random_number)

    ratings = GenericRelation(Rating)

    @property
    def is_available(self):
        return bool(self.inventory > 0)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return  reverse("restaurant:detail-food", args=[self.token])
        

class Category(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title
