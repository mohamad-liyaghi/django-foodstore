from django.views.generic import  FormView, UpdateView, DetailView, ListView
from django.shortcuts import  redirect, get_object_or_404
from django.template.defaultfilters import slugify
from django.contrib import  messages
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin

from restaurant.models import  Food
from restaurant.mixins import AddFoodMixin, FoodUpdateMixin
from restaurant.forms import FoodForm

class FoodCreateView(LoginRequiredMixin, AddFoodMixin, FormView):
    '''
        Add food to database
    '''

    form_class = FoodForm
    template_name = "food/add-food.html"

    def form_valid(self, form):
        form.save()
        form.save_m2m()
        messages.success(self.request, "food created successfully")
        return  redirect("restaurant:list-food")
    

    def form_invalid(self, form):
        messages.success(self.request, "Sth went wrong with your information", "danger")
        return  redirect("restaurant:list-food")


    def get_form_kwargs(self, **kwargs):
        kwargs = super(FoodCreateView, self).get_form_kwargs()
        kwargs['restaurants'] = self.request.user.restaurant.all()
        return kwargs
        

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
        return reverse("restaurant:list-food")

class FoodDetailView(DetailView):
    '''
        Detail page for foods
    '''
    template_name = "food/food-detail.html"
    context_object_name = "food"

    def get_object(self):
        return  get_object_or_404(Food, token=self.kwargs["token"])


class ListFoodView(ListView):
    '''
        List of all foods of a restaurant
    '''
    template_name = "food/list-food.html"
    context_object_name = "foods"

    def get_queryset(self):
        return Food.objects.filter(provider= self.request.user.restaurant)