from django.urls import path
from .views import Profile, MoneyView, AddRequestView

app_name = "accounts"

urlpatterns = [
    path("profile/", Profile.as_view(), name='profile'),
    path("profile/<int:id>/", Profile.as_view(), name='profile'),
    path("exchange/", MoneyView.as_view(), name="exchange-money"), 

    path("add-request/", AddRequestView.as_view(), name="add-request")
]