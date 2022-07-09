from django.urls import path
from .views import HomePageView, FoodSearchView, CartPageView

app_name = "customer"

urlpatterns =[
    path("", HomePageView.as_view(), name= "home"),
    path("foods/", FoodSearchView.as_view(), name="food-result"),

    path("cart/", CartPageView.as_view(), name="cart-page")
]