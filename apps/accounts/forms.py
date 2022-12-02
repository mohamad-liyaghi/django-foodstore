from django import forms
from accounts.models import User, Request

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


class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ["attachment", "description"]
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(RequestForm, self).__init__(*args, **kwargs)
    
    def save(self, commit=True):
        request = super().save(commit=False)
        request.user = self.user
        request = request.save()
        return request
