from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    # These fields are displayed in the list view of the user list.
    list_display = ('email', 'name', 'phone', 'type', 'is_active', 'is_admin')
    
    # Define the fields that can be used to filter the users in the list view.
    list_filter = ('is_admin', 'is_active', 'type')

    # Define the fields that are shown when editing a user.
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('phone', 'name', 'type')}),
        ('Permissions', {'fields': ('is_active', 'is_admin', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
# Register the custom User model and UserAdmin with the admin site.
admin.site.register(User, UserAdmin)
