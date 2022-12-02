from django.urls import path
from .views import (ProfileView, MoneyView, RequestCreateView,
                                     RequestListView, RequestDetailView, RequestStatusView)

app_name = "accounts"

urlpatterns = [
    path("profile/", ProfileView.as_view(), name='profile'),
    path("profile/<int:id>/", ProfileView.as_view(), name='profile'),
    path("exchange/", MoneyView.as_view(), name="exchange-money"), 

    path("add-request/", RequestCreateView.as_view(), name="add-request"),
    path('request-list/', RequestListView.as_view(), name="request-list"),
    path('request-detail/<str:token>/', RequestDetailView.as_view(), name="request-detail"),
    path('request-status/<int:request_token>/<str:status>/', RequestStatusView.as_view(), name="request-status")
]