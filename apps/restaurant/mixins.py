from django.shortcuts import redirect, get_object_or_404

from customer.models import Order
from accounts.models import User


class RestaurantUpdateMixin():
    '''
        Mixin for updating a restaurants information
    '''

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user

        if not user.add_food and user.restaurant:
            return redirect("restaurant:register-restaurant")

        return super().dispatch(request, *args, **kwargs)

class AddFoodMixin(RestaurantUpdateMixin):
    '''
        Mixin for adding food
    '''
    pass

class FoodUpdateMixin(RestaurantUpdateMixin):
    '''
        Mixin for updating food
    '''
    pass

class OrderListMixin(RestaurantUpdateMixin):
    '''
        Check if user can access to orders page
    '''
    pass

class OrderArivedMixin():
    '''
        Check if an order belongs to a user
    '''

    def dispatch(self, request, *args, **kwargs):
        object = get_object_or_404(Order, id=self.kwargs["id"], orderid=self.kwargs["orderid"])
        if object.user == self.request.user:
            return super().dispatch(request, *args, **kwargs)

        return  redirect("customer:home")