"""
Admin configuration for Activity app
"""

from django.contrib import admin
from .models import Activity


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    """Admin interface for Activity model"""
    
    list_display = [
        'name', 'user', 'activity_type', 'duration_minutes',
        'calories_burned', 'intensity_level', 'performed_at'
    ]
    list_filter = [
        'activity_type', 'intensity_level', 'performed_at', 'created_at'
    ]
    search_fields = ['user__username', 'name', 'notes']
    ordering = ['-performed_at']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('user', 'activity_type', 'name', 'performed_at')
        }),
        ('Detalles de la Actividad', {
            'fields': (
                'duration_minutes', 'distance_km', 'calories_burned',
                'intensity_level', 'notes'
            )
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def get_readonly_fields(self, request, obj=None):
        """Make user field readonly when editing"""
        if obj:
            return self.readonly_fields + ['user']
        return self.readonly_fields
