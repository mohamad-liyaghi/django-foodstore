from django import forms
from restaurant.models import Restaurant

class RegisterRestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ("name", "picture", "description", "country", "city", "detailed_address", "owner", "email", "slug")