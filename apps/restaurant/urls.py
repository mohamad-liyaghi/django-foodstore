from django.urls import path
from .views.restaurant_views import (RegisterRestaurantView, UpdateRestaurantView)
urlpatterns = [
    path("register/", RegisterRestaurantView.as_view(), name="register-restaurant"),
    path("update/<int:pk>/<str:slug>/", UpdateRestaurantView.as_view(), name="update-restaurant"),
]