from django.contrib.auth.models import BaseUserManager
import random

class UserManager(BaseUserManager):
    def create_user(self, full_name, email, country, city, detailed_address, password):

        if not full_name:
            raise ValueError("Users must have full name!")

        if not email:
            raise ValueError("Users must have Email")


        user_id = random.randint(10000000000000, 99999999999999)

        user = self.model(
            email= email, full_name= full_name,  userid= user_id,
            country= country, city= city, detailed_address= detailed_address
        )
        user.set_password(password)
        user.save(using= self._db)
        return user


    def create_superuser(self, full_name, email, country, city, detailed_address, password):
        user = self.create_user(full_name, email, country, city, detailed_address, password)
        user.is_admin = True
        user.save(using=self._db)
        return user