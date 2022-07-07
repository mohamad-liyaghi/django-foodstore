from django.views.generic import  FormView
from django.shortcuts import  redirect
from django.template.defaultfilters import slugify
from django.contrib import  messages
from django.contrib.auth.mixins import LoginRequiredMixin

from restaurant.mixins import AddFoodMixin
from restaurant.forms import FoodForm

class CreateFoodView(LoginRequiredMixin, AddFoodMixin, FormView):
    '''
        Create a new food
    '''

    form_class = FoodForm
    template_name = "food/create-food.html"

    def form_valid(self, form):
        form = self.form_class(self.request.POST, self.request.FILES)
        form = form.save(commit=False)
        form.provider = self.request.user.restaurant
        form.slug = slugify(form.name) + slugify(form.provider)
        form.save()
        form.save_m2m()
        messages.success(self.request, "food created successfully")
        return  redirect("restaurant:restaurant-dashboard")



