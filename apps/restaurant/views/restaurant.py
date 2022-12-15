from django.views.generic import FormView, UpdateView, DeleteView, TemplateView, ListView, View
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse, reverse_lazy

from restaurant.forms import RestaurantForm
from restaurant.mixins import OrderListMixin
from restaurant.models import Restaurant, Food
from customer.models import OrderItem
from customer.models import Order


class RegisterRestaurantView(LoginRequiredMixin, FormView):
    '''
        Register a new restaurant
    '''
    template_name = "restaurant/restaurant-register.html"
    form_class = RestaurantForm
    success_url = reverse_lazy("restaurant:restaurant-request-list")


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



class RestaurantProfileView(LoginRequiredMixin, UpdateView):
    '''
        Restaurant profile and update page.
    '''
    template_name = "restaurant/restaurant-profile.html"
    fields = ["name", "picture", "description", "country", "city",
                 "detailed_address", "email"]

    def dispatch(self, request, *args, **kwargs):
        '''
            Check if restaurant is accepted 
            if not only admins and requested user can access that page
        '''

        if self.get_object().status != "a":

                if request.user.is_authenticated:
                    if request.user == self.get_object().owner or request.user.role in ["a", "s"]:
                        return super().dispatch(request, *args, **kwargs)

                return redirect("customer:home")

        return super().dispatch(request, *args, **kwargs)
            

    def get_object(self):
        return get_object_or_404(Restaurant, token=self.kwargs["token"])

    def post(self, request, *args, **kwargs):
        '''Check if objects status is pending'''

        if request.user == self.get_object().owner \
            and self.get_object().status == "p":
            messages.success(self.request, "Restaurant updated.", "success")
            return super().post(request, *args, **kwargs)
        
        messages.success(self.request, "couldnt update the object.", "danger")
        return redirect("customer:home")
    
    def get_success_url(self):
        return reverse("restaurant:restaurant-profile", kwargs={"token" : self.get_object().token})
        


class RestaurantRequestListView(LoginRequiredMixin, ListView):
    '''
        List of restaurant requests.
    '''

    template_name = "restaurant/restaurant-request-list.html"
    context_object_name = "requests"

    def get_queryset(self):
        if self.request.user.is_admin:
            return Restaurant.objects.filter(status="p")

        return Restaurant.objects.filter(owner=self.request.user)



class RestaurantRequestStatusView(LoginRequiredMixin, View):
    '''Change a restaurants status (accept, decline or block)'''
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_admin:
            return super().dispatch(request, *args, **kwargs)
        
        if not self.kwargs["status"] in ["a", "r", "b"]:
            messages.success(self.request, "Please insert a valid operation.", 'warning')
            return redirect("customer:home")
        
        messages.success(self.request, "Only admin users can access this page.", "warning")
        return redirect("customer:home")
    

    def get(self, request, restaurant_token, status):

        restaurant = get_object_or_404(Restaurant, token=self.kwargs["restaurant_token"], status="p")

        if restaurant.owner == self.request.user:
            messages.success(self.request, "You can not accept your own request.", "warning")
            return redirect("customer:home")

        restaurant.status = status
        restaurant.save()

        messages.success(self.request, f"Request status changed to {status}.")
        return redirect("restaurant:restaurant-request-list")



class RestaurantDeleteView(LoginRequiredMixin, DeleteView):
    '''Delete a restaurant'''
    template_name = "restaurant/restaurant-delete.html"
    context_object_name = "restaurant"
    success_url = reverse_lazy("customer:home")

    def dispatch(self, request, *args, **kwargs):
        if OrderItem.objects.filter(Q(item__provider=self.get_object()) & Q(order__is_paid=True) &
                                    ~Q(prepared=True)).exists():
            messages.success(self.request, "You can not delete a restaurant while there are some orders.", "danger")
            return redirect("restaurant:restaurant-orders")
            
        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        return get_object_or_404(self.request.user.restaurant, 
                                token=self.kwargs["token"])


class DashBoardRestaurant(LoginRequiredMixin, TemplateView):
    '''
        Dashboard page
    '''
    template_name = "restaurant/dashboard-restaurant.html"
    def dispatch(self, request, *args, **kwargs):
        self.restaurants = Restaurant.objects.filter(owner=self.request.user)
        if self.restaurants.exists():
            return super().dispatch(request, *args, **kwargs)

        messages.success(self.request, "This page is only available for users who registered a restaurant.", "danger")
        return redirect("restaurant:register-restaurant")

    def get_context_data(self, **kwargs):
        context = super(DashBoardRestaurant, self).get_context_data(**kwargs)
        
        context['restaurants'] = Restaurant.objects.filter(owner= self.request.user)
        context['food'] = Food.objects.filter(provider__in=self.restaurants).count()
        return context


class RestaurantOrderList(LoginRequiredMixin, OrderListMixin, ListView):
    '''
        Get all orders related to a restaurant
    '''
    template_name = "restaurant/orders-restaurant.html"
    context_object_name = "orders"

    def get_queryset(self):
        foods = Food.objects.only("name").filter(provider__owner=self.request.user)
        return OrderItem.objects.filter(Q(item__in=foods) & Q(prepared=False))


class ItemPreparedView(LoginRequiredMixin, OrderListMixin, View):
    '''
        Change status of an order
    '''

    def get(self, request, id):
        item = get_object_or_404(OrderItem, id=self.kwargs["id"], prepared=False,
                                    item__provider__in=self.request.user.restaurant.all())
        
        item.prepared = True
        item.save()


        if item.order.items.filter(prepared=False).count() == 0:
            item.order.status = "Sending"
            item.order.save()

        messages.success(request, "Item prepared.", "success")
        return redirect("restaurant:restaurant-orders")

class OrderArrived(LoginRequiredMixin, View):
    '''
        Change status of an order to Arrived
    '''

    def get(self, request, order_id):
        object = get_object_or_404(Order, order_id=self.kwargs["order_id"], user=request.user,
                                    status="Sending")

        object.status = "Arrived"
        object.save()
        return redirect("customer:cart-page")
