from django.urls import path
from .views.restaurant_views import (RegisterRestaurantView, UpdateRestaurantView, ProfileRestaurant, DashBoardRestaurant)
urlpatterns = [
    path("", DashBoardRestaurant.as_view(), name="restaurant-dashboard"),
    path("register/", RegisterRestaurantView.as_view(), name="register-restaurant"),
    path("update/<int:pk>/<str:slug>/", UpdateRestaurantView.as_view(), name="update-restaurant"),
    path("profile/<int:pk>/<str:slug>/", ProfileRestaurant.as_view(), name="profile-restaurant"),
]