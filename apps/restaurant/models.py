from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from star_ratings.models import Rating
from django.urls import reverse
from accounts.models import User
# Create your models here.

class Restaurant(models.Model):
    name = models.CharField(max_length= 50)
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    
    picture = models.ImageField(upload_to= "restaurant/profile")
    description = models.TextField()

    country = models.CharField(max_length=30, blank=True)
    city = models.CharField(max_length=30, blank=True)
    detailed_address = models.CharField(max_length=120, blank=True)

    owner = models.OneToOneField(User,on_delete=models.CASCADE ,related_name="restaurant", blank=True)
    email = models.EmailField(max_length=70, unique=True)

    ratings = GenericRelation(Rating)

    def get_absolute_url(self):
        return reverse("restaurant:profile-restaurant", kwargs={"pk" : self.pk, "slug" : self.slug})

    def __str__(self):
        return  self.name



class Food(models.Model):
    name = models.CharField(max_length= 10)
    slug = models.SlugField(unique=True, blank=True)

    picture = models.ImageField(upload_to="foods/")

    description = models.TextField(max_length=30)
    category = models.ManyToManyField("Category", related_name="food_category")
    provider = models.ForeignKey(Restaurant, on_delete=models.CASCADE, blank=True, related_name="foods")

    inventory = models.PositiveIntegerField(default=0)

    price = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)

    ratings = GenericRelation(Rating)

    def __str__(self):
        return self.name


class Category(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title