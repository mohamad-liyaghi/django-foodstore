from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from accounts.models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'userid', 'balance')
    list_filter = ('email',)
    search_fields = ('email', 'userid')
    ordering = ('email',)

    filter_horizontal = ()

    fieldsets = (
		(None, {'fields':('email', 'userid', "balance", "role", 'password')}),
		('Permissions', {'fields':('is_staff', "is_superuser", 'last_login')}),
	)

    add_fieldsets = (
        (None, {'fields':('email', 'password1', 'password2')}),
    )
    
