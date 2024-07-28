from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):

    list_display = ('email', 'phone', 'name', 'is_admin', 'is_staff', 'is_superuser')
    list_filter = ('is_admin', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('phone', 'name')}),
        ('Permissions', {'fields': ('is_admin', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone', 'name', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'phone', 'name')
    ordering = ('-id',)
    filter_horizontal = ()

admin.site.register(User, UserAdmin)
