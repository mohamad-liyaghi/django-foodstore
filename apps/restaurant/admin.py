from django.contrib import admin

from .models import Restaurant
# Register your models here.

class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "email")
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Restaurant, RestaurantAdmin)