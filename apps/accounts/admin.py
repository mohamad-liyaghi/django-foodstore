from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


from accounts.models import User


class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'full_name', 'add_food')
    list_filter = ('email',)
    search_fields = ('email', 'full_name')
    
    ordering = ('full_name',)

    filter_horizontal = ()

    fieldsets = (
		(None, {'fields':('email', 'full_name','userid','country', 'city', 'detailed_address', 'password')}),
		('Permissions', {'fields':('is_admin', 'last_login', 'add_food')}),
	)

    add_fieldsets = (
        (None, {'fields':('email', 'full_name', 'country', 'city', 'detailed_address', 'password1', 'password2')}),
    )
admin.site.register(User, UserAdmin)
