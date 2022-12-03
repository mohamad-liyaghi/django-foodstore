from django.contrib import admin

from .models import Restaurant, Food, Category

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "email")

class FoodAdmin(admin.ModelAdmin):
    list_display = ("name" ,"price", "is_available")
    prepopulated_fields = {"slug" : ("name", "provider")}

admin.site.register(Food, FoodAdmin)
admin.site.register(Category)