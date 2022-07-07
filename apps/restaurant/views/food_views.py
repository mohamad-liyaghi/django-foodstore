from django.views.generic import  FormView, UpdateView, DetailView
from django.shortcuts import  redirect, get_object_or_404
from django.template.defaultfilters import slugify
from django.contrib import  messages
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin

from restaurant.models import  Food
from restaurant.mixins import AddFoodMixin, FoodUpdateMixin
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


class UpdateFoodView(LoginRequiredMixin, FoodUpdateMixin, UpdateView):
    '''
        Update foods status or price
    '''
    template_name = "food/update-food.html"


    fields = ["inventory","price", "is_available"]

    def get_object(self):
        return get_object_or_404(Food, pk=self.kwargs["pk"],
                                 slug=self.kwargs["slug"], provider=self.request.user.restaurant)

    def get_success_url(self):
        return reverse("restaurant:restaurant-dashboard")

class DetailFoodView(DetailView):
    '''
        Detail page for foods
    '''
    template_name = "food/detail-food.html"

    def get_object(self):
        return  get_object_or_404(Food, pk=self.kwargs["pk"],
                          slug=self.kwargs["slug"], provider=self.request.user.restaurant)