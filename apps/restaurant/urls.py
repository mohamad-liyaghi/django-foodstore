from django.urls import path
from .views.restaurant import (RegisterRestaurantView,
                                     RestaurantProfileView, DashBoardRestaurant, RestaurantRequestListView,
                                     RestaurantRequestStatusView, RestaurantDeleteView, OrdersRestaurant, OrderSending, OrderArrived)
from .views.food import (FoodCreateView, UpdateFoodView, FoodDetailView, ListFoodView)

app_name = "restaurant"


urlpatterns = [
    path("", DashBoardRestaurant.as_view(), name="restaurant-dashboard"),
    path("foods/", ListFoodView.as_view(), name="list-food"),

    path("register/", RegisterRestaurantView.as_view(), name="register-restaurant"),
    path("add-food/", FoodCreateView.as_view(), name="add-food"),
    path("requests/", RestaurantRequestListView.as_view(), name='restaurant-request-list'),
    path('restaurant-status/<str:restaurant_token>/<str:status>/', RestaurantRequestStatusView.as_view(), name="restaurant-status"),
    
    path("delete-restaurant/<str:token>/", RestaurantDeleteView.as_view(), name="delete-restaurant"),

    path("update-food/<int:pk>/<str:slug>/", UpdateFoodView.as_view(), name="update-food"),

    path("food-detail/<str:token>/", FoodDetailView.as_view(), name="detail-food"),
    path("profile/<str:token>/", RestaurantProfileView.as_view(), name="restaurant-profile"),

    path('orders/', OrdersRestaurant.as_view(), name= "restaurant-orders"),
    path('order-send/<int:id>/<int:orderid>/', OrderSending.as_view(), name="food-sending"),
    path('order-arrived/<int:id>/<int:orderid>/', OrderArrived.as_view(), name="food-arrived"),

]