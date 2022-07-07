from django.contrib import admin

from .models import Restaurant, Food, Category
# Register your models here.

class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "email")
    prepopulated_fields = {'slug':('name',)}

class FoodAdmin(admin.ModelAdmin):
    list_display = ("name" ,"price", "is_available")
    prepopulated_fields = {"slug" : ("name", "provider")}

admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Food, FoodAdmin)
admin.site.register(Category)