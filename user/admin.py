# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Customize the UserAdmin for your User model
class CustomUserAdmin(UserAdmin):
    # Fields to display in the list view of the admin panel
    list_display = ('email', 'username', 'is_verified', 'is_active', 'is_admin')
    list_filter = ('is_admin', 'is_verified', 'is_active')  # Filters for the list view
    search_fields = ('email', 'username')  # Fields to search by in the admin panel

    # Fieldsets for the add/edit user page
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Permissions', {'fields': ('is_verified', 'is_active', 'is_admin')}),
    )

    # Fieldsets for the add user page
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )

    ordering = ('email',)  # Default ordering for the list view
    filter_horizontal = ()  # No many-to-many fields to filter

# Register the User model with the CustomUserAdmin
admin.site.register(User, CustomUserAdmin)