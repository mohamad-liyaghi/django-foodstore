from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from .managers import UserManager

class User(AbstractUser):
    '''Base user class'''

    class Role(models.TextChoices):
        '''User Role'''
        SUPERUSER = ("s", "Superuser")
        ADMIN = ("a", "Admin")
        NORMAL = ("n", "Normal")
        BLOCKED = ("b", "Blocked")

    username = None
    email = models.EmailField(max_length=200, unique=True)
    userid = models.IntegerField(unique=True, blank=True, null=True)
    balance = models.PositiveIntegerField(default=0)
    role = models.CharField(max_length=1, choices=Role.choices, default=Role.NORMAL)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    

    def __str__(self):
        return self.email

    @property
    def is_blocked(self):
        return bool(self.role == self.Role.BLOCKED)

    
class Profile(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profile")

    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)

    country = models.CharField(max_length=120)
    city = models.CharField(max_length=120)
    detailed_address = models.CharField(max_length=200)

    phone_regex = RegexValidator(regex="\(?\d{3}\)?-? *\d{3}-? *-?\d{4}", 
                                message="Phone number format must be like: (XXX) XXX XXXX")
                                
    phone_number = models.CharField(max_length=15, validators=[phone_regex])

    passport_number = models.CharField(max_length=10)

    
    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"