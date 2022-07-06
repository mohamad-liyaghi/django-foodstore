from django.shortcuts import redirect

from accounts.models import User

class RestaurantRegisterMixin():
    '''
        If user have already registered restaurant, he will be redirected
    '''
    def dispatch(self, request, *args, **kwargs):
        user = User.objects.filter(email= self.request.user.email, full_name= self.request.user.full_name).first()
        if user.add_food and user.restaurant:
            return redirect("#")

        return super().dispatch(request, *args, **kwargs)