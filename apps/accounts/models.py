from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager

class User(AbstractBaseUser):

    full_name = models.CharField(max_length=120)
    email = models.EmailField(max_length=120, unique=True)
    userid = models.IntegerField(unique=True ,blank=True, null=True)

    country = models.CharField(max_length=30, blank=True)
    city = models.CharField(max_length=30, blank=True)
    detailed_address = models.CharField(max_length=120, blank=True)

    add_food = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name","country", "city", "detailed_address"]
    

    def __str__(self):
        return self.full_name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin