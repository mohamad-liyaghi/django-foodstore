from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from star_ratings.models import Rating
from accounts.models import User
# Create your models here.

class Restaurant(models.Model):
    name = models.CharField(max_length= 50)
    slug = models.SlugField(max_length=50, unique=True)
    
    picture = models.ImageField(upload_to= "restaurant/profile")
    description = models.TextField()

    country = models.CharField(max_length=30, blank=True)
    city = models.CharField(max_length=30, blank=True)
    detailed_address = models.CharField(max_length=120, blank=True)

    owner = models.OneToOneField(User,on_delete=models.CASCADE ,related_name="restaurant")
    email = models.EmailField(max_length=70, unique=True)

    ratings = GenericRelation(Rating)


