from django.shortcuts import redirect

from accounts.models import User

class RestaurantRegisterMixin():
    '''
        If user have already registered restaurant, he will be redirected
    '''
    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if user.add_food and user.restaurant:
            return redirect("restaurant:restaurant-dashboard")

        return super().dispatch(request, *args, **kwargs)

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