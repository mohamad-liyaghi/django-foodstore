from django.urls import path
from .views import HomePageView, FoodSearchView

app_name = "customer"

urlpatterns =[
    path("", HomePageView.as_view(), name= "home"),
    path("foods/", FoodSearchView.as_view(), name="food-result"),
]