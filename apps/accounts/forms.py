from django import forms
from accounts.models import User

import random

class RegisterUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ("email", "password")
    
    def save(self, commit= True): 
        user = super(RegisterUserForm, self).save(commit = False)
        user.userid = random.randint(1, 99999999999999)

        if commit:
            user.save()
            
        return user
    