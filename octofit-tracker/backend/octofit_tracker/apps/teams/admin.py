"""
Admin configuration for Team app
"""

from django.contrib import admin
from .models import Team, TeamMember


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    """Admin interface for Team model"""
    
    list_display = ['name', 'leader', 'member_count', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'leader__username']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Información del Equipo', {
            'fields': ('name', 'description', 'leader', 'is_active')
        }),
        ('Estadísticas', {
            'fields': ('member_count',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at', 'member_count']


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    """Admin interface for TeamMember model"""
    
    list_display = ['user', 'team', 'role', 'joined_at']
    list_filter = ['team', 'role', 'joined_at']
    search_fields = ['user__username', 'team__name']
    ordering = ['-joined_at']
    
    fieldsets = (
        ('Miembro del Equipo', {
            'fields': ('team', 'user', 'role')
        }),
        ('Metadata', {
            'fields': ('joined_at',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['joined_at']
