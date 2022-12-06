from django.contrib import admin

from .models import Restaurant, Food, Category

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "email")

@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "is_available")

admin.site.register(Category)