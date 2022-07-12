from django.urls import path
from .views.restaurant_views import (RegisterRestaurantView, UpdateRestaurantView,
                                     ProfileRestaurant, DashBoardRestaurant, OrdersRestaurant, OrderSending)
from .views.food_views import (CreateFoodView, UpdateFoodView, DetailFoodView, ListFoodView)

app_name = "restaurant"


urlpatterns = [
    path("", DashBoardRestaurant.as_view(), name="restaurant-dashboard"),
    path("foods/", ListFoodView.as_view(), name="list-food"),

    path("register/", RegisterRestaurantView.as_view(), name="register-restaurant"),
    path("create-food/", CreateFoodView.as_view(), name="create-food"),

    path("update/<int:pk>/<str:slug>/", UpdateRestaurantView.as_view(), name="restaurant-update"),
    path("update-food/<int:pk>/<str:slug>/", UpdateFoodView.as_view(), name="update-food"),

    path("detail-food/<int:pk>/<str:slug>/", DetailFoodView.as_view(), name="detail-food"),
    path("profile/<int:pk>/<str:slug>/", ProfileRestaurant.as_view(), name="restaurant-profile"),

    path('orders/', OrdersRestaurant.as_view(), name= "restaurant-orders"),
    path('order-send/<int:id>/<int:orderid>/', OrderSending.as_view(), name="food-sending")
]