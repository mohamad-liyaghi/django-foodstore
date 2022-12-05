from django.urls import path
from .views.restaurant import (RegisterRestaurantView,
                                     RestaurantProfileView, DashBoardRestaurant, RestaurantRequestListView,
                                     OrdersRestaurant, OrderSending, OrderArrived)
from .views.food import (CreateFoodView, UpdateFoodView, DetailFoodView, ListFoodView)

app_name = "restaurant"


urlpatterns = [
    path("", DashBoardRestaurant.as_view(), name="restaurant-dashboard"),
    path("foods/", ListFoodView.as_view(), name="list-food"),

    path("register/", RegisterRestaurantView.as_view(), name="register-restaurant"),
    path("create-food/", CreateFoodView.as_view(), name="create-food"),
    path("requests/", RestaurantRequestListView.as_view(), name='restaurant-request-list'),

    path("update-food/<int:pk>/<str:slug>/", UpdateFoodView.as_view(), name="update-food"),

    path("detail-food/<int:pk>/<str:slug>/", DetailFoodView.as_view(), name="detail-food"),
    path("profile/<str:token>/", RestaurantProfileView.as_view(), name="restaurant-profile"),

    path('orders/', OrdersRestaurant.as_view(), name= "restaurant-orders"),
    path('order-send/<int:id>/<int:orderid>/', OrderSending.as_view(), name="food-sending"),
    path('order-arrived/<int:id>/<int:orderid>/', OrderArrived.as_view(), name="food-arrived"),

]