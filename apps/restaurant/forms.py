from django import forms
from restaurant.models import Restaurant, Food

class RestaurantForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(RestaurantForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Restaurant
        fields = ("name", "picture", "description", "country", "city",
                 "detailed_address", "email")

    def save(self, commit=True):
        form = super().save(commit=False)
        form.owner = self.user
        form.save()
        return form


class FoodForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.restaurants = kwargs.pop('restaurants', None)
        super(FoodForm, self).__init__(*args, **kwargs)
        self.fields["provider"].queryset = self.restaurants


    class Meta:
        model = Food
        fields = ("name", "picture", "description", "category", 
                "inventory", "price", "provider")

    def save(self, commit=True):
        form =  super().save(commit=False)
        form.save()
        return form
