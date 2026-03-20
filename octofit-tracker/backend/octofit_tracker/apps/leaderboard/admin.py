"""
Admin configuration for Leaderboard app
"""

from django.contrib import admin
from .models import Leaderboard, TeamLeaderboard


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    """Admin interface for Leaderboard model"""
    
    list_display = [
        'user', 'week_id', 'rank', 'points',
        'activities_count', 'total_calories'
    ]
    list_filter = ['week_id', 'rank']
    search_fields = ['user__username', 'week_id']
    ordering = ['week_id', 'rank']
    
    fieldsets = (
        ('Información del Usuario', {
            'fields': ('user', 'week_id')
        }),
        ('Estadísticas', {
            'fields': (
                'points', 'activities_count', 'total_duration_minutes',
                'total_calories', 'rank'
            )
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']


@admin.register(TeamLeaderboard)
class TeamLeaderboardAdmin(admin.ModelAdmin):
    """Admin interface for TeamLeaderboard model"""
    
    list_display = [
        'team', 'week_id', 'rank', 'points',
        'total_activities', 'total_calories'
    ]
    list_filter = ['week_id', 'rank']
    search_fields = ['team__name', 'week_id']
    ordering = ['week_id', 'rank']
    
    fieldsets = (
        ('Información del Equipo', {
            'fields': ('team', 'week_id')
        }),
        ('Estadísticas', {
            'fields': (
                'points', 'total_activities', 'total_duration_minutes',
                'total_calories', 'rank'
            )
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
