from django.db import models
from django.contrib.auth.models import AbstractUser
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

