from django.views.generic import  FormView, UpdateView, ListView, DeleteView
from django.shortcuts import  redirect, get_object_or_404
from django.contrib import  messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy

from restaurant.models import  Food
from customer.views import Order
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
        return  redirect("restaurant:food-list")
    

    def form_invalid(self, form):
        messages.success(self.request, "Sth went wrong with your information", "danger")
        return  redirect("restaurant:food-list")


    def get_form_kwargs(self, **kwargs):
        kwargs = super(FoodCreateView, self).get_form_kwargs()
        kwargs['restaurants'] = self.request.user.restaurant.filter(status="a")
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
        


class FoodListView(LoginRequiredMixin, ListView):
    '''
        List of all foods of a restaurant
    '''
    template_name = "food/food-list.html"
    context_object_name = "foods"

    def get_queryset(self):
        return Food.objects.filter(provider__in=self.request.user.restaurant.all())


class FoodDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "food/food-delete.html"
    success_url = reverse_lazy("restaurant:food-list")

    def get_object(self):
        return get_object_or_404(Food,token=self.kwargs["token"], 
                                    provider__in=self.request.user.restaurant.filter(status="a"))

    def post(self, request, *args, **kwargs):
        #TODO fix the query later.
        unprepared_order = Order.objects.filter(Q(items=self.get_object()) & 
                                                ~Q(prepared_items=self.get_object()) & Q(is_paid=True))

        if unprepared_order.exists():
            messages.success(self.request, "You have orders that you havnt prepared.", "danger")
            return redirect("restaurant:food-detail", token=self.get_object().token)
        
        messages.success(self.request, "food deleted successfully", "success")
        return super().post(request, *args, **kwargs)