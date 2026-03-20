"""
Admin configuration for User app
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin interface for User model"""
    
    list_display = [
        'username', 'email', 'first_name', 'last_name',
        'fitness_level', 'age', 'is_active', 'created_at'
    ]
    list_filter = [
        'fitness_level', 'gender', 'is_active', 'created_at'
    ]
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-created_at']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Información de Fitness', {
            'fields': (
                'height_cm', 'weight_kg', 'age', 'gender',
                'fitness_level', 'bio', 'profile_picture'
            )
        }),
        ('Estado', {
            'fields': ('is_active', 'created_at', 'updated_at', 'last_login')
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at', 'last_login']
