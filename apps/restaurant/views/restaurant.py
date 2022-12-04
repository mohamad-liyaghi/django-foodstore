from django.views.generic import FormView, UpdateView, DetailView, TemplateView, ListView, View
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse, reverse_lazy

from restaurant.forms import RestaurantForm
from restaurant.mixins import RestaurantUpdateMixin, OrderListMixin, OrderArivedMixin
from restaurant.models import Restaurant, Food
from customer.models import Order


class RegisterRestaurantView(LoginRequiredMixin, FormView):
    '''
        Register a new restaurant
    '''
    template_name = "restaurant/register-restaurant.html"
    form_class = RestaurantForm
    success_url = reverse_lazy("customer:home")


    def dispatch(self, request, *args, **kwargs):
        '''Check if user doesnt have a blocked or pending request.'''
        
        if self.request.user.restaurant.filter(status="p"):
            messages.success(self.request, "You have a pending request, please wait for its result.", "warning")
            return redirect("customer:home")
        
        if self.request.user.restaurant.filter(status="b"):
            messages.success(self.request, "You are blocked. You can not add restaurant.", "danger")
            return redirect("customer:home")

        return super().dispatch(request, *args, **kwargs)


    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Your restaurant request is submitted. wait for results.", "success")
        return super().form_valid(form)


    def form_invalid(self, form):
        messages.success(self.request, "sth went wrong with your information...", "alert")
    

    def get_form_kwargs(self):
        kwargs = super(RegisterRestaurantView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class UpdateRestaurantView(LoginRequiredMixin, RestaurantUpdateMixin, UpdateView):
    '''
        Update restaurant page
    '''
    template_name = "restaurant/update-restaurant.html"
    fields = ["name", "picture", "description", "country", "city", "detailed_address", "email"]

    def get_object(self):
        return get_object_or_404(Restaurant, pk=self.kwargs["pk"],
                                         slug=self.kwargs["slug"], owner= self.request.user)

class ProfileRestaurant(DetailView):
    '''
        Restaurant profile page
    '''
    template_name = "restaurant/profile-restaurant.html"

    def get_object(self):
        return get_object_or_404(Restaurant, pk=self.kwargs["pk"], slug=self.kwargs["slug"])

class DashBoardRestaurant(TemplateView):
    '''
        Dashboard page
    '''
    template_name = "restaurant/dashboard-restaurant.html"

    def get_context_data(self, **kwargs):
        context = super(DashBoardRestaurant, self).get_context_data(**kwargs)
        context['food'] = Food.objects.filter(provider= self.request.user.restaurant).count()
        context['restaurant'] = Restaurant.objects.filter(owner= self.request.user).first()
        return context

class OrdersRestaurant(LoginRequiredMixin, OrderListMixin,ListView):
    '''
        Get all orders related to a restaurant
    '''
    template_name = "restaurant/orders-restaurant.html"
    context_object_name = "orders"
    def get_queryset(self):
        return Order.objects.filter(Q(items__in= self.request.user.restaurant.foods.all()), Q(status="preparing"),
                                    ~Q(prepared_items__in = self.request.user.restaurant.foods.all()))

class OrderSending(LoginRequiredMixin, OrderListMixin, View):
    '''
        Change status of an order
    '''

    def get(self, request, id, orderid):
        object = get_object_or_404(Order, id= self.kwargs["id"], orderid=self.kwargs["orderid"])
        foods = object.items.all()
        for food in foods:
                if food in self.request.user.restaurant.foods.all():
                    object.prepared_items.add(food)

        if object.items.count() == object.prepared_items.count():
            object.status = "sending"

        object.save()
        return redirect("restaurant:restaurant-orders")

class OrderArrived(LoginRequiredMixin, OrderArivedMixin, View):
    '''
        Change status of an order to Arrived
    '''

    def get(self, request, id, orderid):
        object = get_object_or_404(Order, id= self.kwargs["id"], orderid=self.kwargs["orderid"])
        object.status = "Arrived"
        object.save()
        return redirect("customer:cart")
