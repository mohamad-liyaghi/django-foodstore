from django.urls import path
from .views.restaurant_views import (RegisterRestaurantView)
urlpatterns = [
    path("register/", RegisterRestaurantView.as_view(), name="register-restaurant"),
]