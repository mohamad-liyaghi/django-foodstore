from django.views.generic import  FormView, UpdateView, ListView
from django.shortcuts import  redirect, get_object_or_404
from django.contrib import  messages
from django.contrib.auth.mixins import LoginRequiredMixin

from restaurant.models import  Food
from restaurant.mixins import AddFoodMixin
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
        messages.success(self.request, "food created successfully", "success")
        return  redirect("restaurant:list-food")
    

    def form_invalid(self, form):
        messages.success(self.request, "Sth went wrong with your information", "danger")
        return  redirect("restaurant:list-food")


    def get_form_kwargs(self, **kwargs):
        kwargs = super(FoodCreateView, self).get_form_kwargs()
        kwargs['restaurants'] = self.request.user.restaurant.all()
        return kwargs
        


class FoodDetailView(UpdateView):
    '''
        Detail page for foods
        Also update page for provider
    '''

    template_name = "food/food-detail.html"
    fields = ["name", "description", "picture", "inventory", "price"]
    context_object_name = "food"

    def get_object(self):
        return  get_object_or_404(Food, token=self.kwargs["token"])
    
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user == self.get_object().provider.owner:
                super().post(request, *args, **kwargs)
                messages.success(request, "Food updated successfuly.", "success")    
                return redirect("restaurant:food-detail", token=self.get_object().token)

            messages.success(request, "You are not this foods provider.", "danger")    
            return redirect("restaurant:food-detail", token=self.get_object().token)
                
        
        messages.success(request, "Unknown users cannot update this object.", "danger")
        return redirect("restaurant:food-detail", token=self.get_object().token)
        


class ListFoodView(ListView):
    '''
        List of all foods of a restaurant
    '''
    template_name = "food/list-food.html"
    context_object_name = "foods"

    def get_queryset(self):
        return Food.objects.filter(provider= self.request.user.restaurant)