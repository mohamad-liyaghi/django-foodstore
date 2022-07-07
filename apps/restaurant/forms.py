from django import forms
from restaurant.models import Restaurant, Food

class RegisterRestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ("name", "picture", "description", "country", "city", "detailed_address", "owner", "email", "slug")

class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ("name", "slug", "picture", "description", "category", "provider", "inventory", "price", "is_available")