from django.views.generic import FormView
from django.contrib import messages
from django.template.defaultfilters import slugify
from django.contrib.auth.mixins import LoginRequiredMixin

from restaurant.forms import RegisterRestaurantForm
from restaurant.mixins import RestaurantRegisterMixin
from accounts.models import User

class RegisterRestaurantView(LoginRequiredMixin, RestaurantRegisterMixin, FormView):
    '''
        Register a new restaurant
    '''
    template_name = "restaurant/register-restaurant.html"
    form_class = RegisterRestaurantForm

    def form_valid(self, form):
        form = self.form_class(self.request.POST, self.request.FILES)
        user = User.objects.filter(email= self.request.user.email, full_name= self.request.user.full_name).first()
        user.add_food = True
        form = form.save(commit=False)
        form.owner = self.request.user
        form.slug = slugify(form.name)
        form.save()
        user.save()
        messages.success(self.request,"restaurant registered successfully", "success")
    
    def form_invalid(self, form):
        messages.success(self.request, "sth went wrong with your information...", "alert")
