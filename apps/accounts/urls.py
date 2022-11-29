from django.urls import path
from .views import Profile

app_name = "accounts"

urlpatterns = [
    path("profile/<int:id>/", Profile.as_view(), name='profile')
]