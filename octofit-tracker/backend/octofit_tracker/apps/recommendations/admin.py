"""
Admin configuration for Recommendations app
"""

from django.contrib import admin
from .models import Recommendation


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    """Admin interface for Recommendation model"""
    
    list_display = [
        'title', 'user', 'recommendation_type', 'intensity',
        'status', 'created_at'
    ]
    list_filter = [
        'recommendation_type', 'intensity', 'status', 'created_at'
    ]
    search_fields = ['user__username', 'title', 'description', 'reason']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Información General', {
            'fields': ('user', 'recommendation_type', 'title', 'description')
        }),
        ('Detalles', {
            'fields': (
                'intensity', 'estimated_duration_minutes', 'reason', 'status'
            )
        }),
        ('Tracking', {
            'fields': ('created_at', 'viewed_at', 'accepted_at', 'completed_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'viewed_at', 'accepted_at', 'completed_at']
    
    actions = ['mark_as_pending', 'mark_as_viewed', 'mark_as_completed']
    
    def mark_as_pending(self, request, queryset):
        """Admin action to mark as pending"""
        updated = queryset.update(status='pending')
        self.message_user(request, f'{updated} recomendaciones marcadas como pendientes.')
    mark_as_pending.short_description = 'Marcar como pendiente'
    
    def mark_as_viewed(self, request, queryset):
        """Admin action to mark as viewed"""
        from django.utils import timezone
        queryset.update(status='viewed', viewed_at=timezone.now())
        updated = queryset.count()
        self.message_user(request, f'{updated} recomendaciones marcadas como vistas.')
    mark_as_viewed.short_description = 'Marcar como visto'
    
    def mark_as_completed(self, request, queryset):
        """Admin action to mark as completed"""
        from django.utils import timezone
        queryset.update(status='completed', completed_at=timezone.now())
        updated = queryset.count()
        self.message_user(request, f'{updated} recomendaciones marcadas como completadas.')
    mark_as_completed.short_description = 'Marcar como completadas'
