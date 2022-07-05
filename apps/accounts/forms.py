from django import forms
from accounts.models import User

import random

class RegisterUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ("email", "full_name","country", 'city',"detailed_address" , "password")
    
    def save(self, commit= True): 
        user = super(RegisterUserForm, self).save(commit = False)
        user.userid = random.randint(10000000000000, 99999999999999)

        if commit:
            user.save()
            
        return user
    