from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name','is_superuser', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    readonly_fields = ('date_joined',)

    # Fields to be used when creating a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    
    # Define which fields can be searched in the list view
    search_fields = ('email', 'username')
    ordering = ('username',)

# Register the custom user model with the custom admin
admin.site.register(CustomUser, CustomUserAdmin)
