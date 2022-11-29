from django.contrib.auth.models import BaseUserManager
import random


class UserManager(BaseUserManager):
    '''Override save method of User class'''

    def create_user(self, email, password, **kwargs):

        if not email:
            raise ValueError("Users must have Email")

        userid = random.randint(1, 99999999999999)
        email = self.normalize_email(email)

        user = self.model(
            email=email, userid=userid, **kwargs
        )

        user.set_password(password)
        user.save(using= self._db)

        return user


    def create_superuser(self, email, password, **kwargs):
        '''Create a superuser'''

        user = self.create_user(email=email,  password=password,
            role="s", is_staff=True, is_superuser=True, is_active=True)
        
        user.save(using=self._db)
        return user