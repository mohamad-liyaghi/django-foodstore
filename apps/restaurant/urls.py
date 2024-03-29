from django.urls import path
from .views.restaurant import (RegisterRestaurantView,
                                     RestaurantProfileView, DashBoardRestaurant, RestaurantRequestListView,
                                     RestaurantRequestStatusView, RestaurantDeleteView, RestaurantOrderList, ItemPreparedView, 
                                     OrderArrived)
from .views.food import (FoodCreateView, FoodDetailView, FoodListView, FoodDeleteView)

app_name = "restaurant"


urlpatterns = [
    path("", DashBoardRestaurant.as_view(), name="restaurant-dashboard"),
    path("foods/", FoodListView.as_view(), name="food-list"),

    path("register/", RegisterRestaurantView.as_view(), name="register-restaurant"),
    path("add-food/", FoodCreateView.as_view(), name="add-food"),
    path("delete-food/<str:token>/", FoodDeleteView.as_view(), name="delete-food"),
    path("requests/", RestaurantRequestListView.as_view(), name='restaurant-request-list'),
    path('restaurant-status/<str:restaurant_token>/<str:status>/', RestaurantRequestStatusView.as_view(), name="restaurant-status"),
    
    path("delete-restaurant/<str:token>/", RestaurantDeleteView.as_view(), name="delete-restaurant"),

    path("food-detail/<str:token>/", FoodDetailView.as_view(), name="food-detail"),
    path("profile/<str:token>/", RestaurantProfileView.as_view(), name="restaurant-profile"),

    path('orders/', RestaurantOrderList.as_view(), name= "restaurant-orders"),
    path('item-prepared/<int:id>/', ItemPreparedView.as_view(), name="item-prepared"),
    path('order-arrived/<int:order_id>/', OrderArrived.as_view(), name="food-arrived"),

]