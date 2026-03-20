"""
Recommendation Models for Octofit Tracker
"""

from django.db import models
from octofit_tracker.apps.users.models import User


class Recommendation(models.Model):
    """Model for personalized workout recommendations"""
    
    RECOMMENDATION_TYPES = [
        ('workout', 'Entrenamiento'),
        ('rest', 'Descanso'),
        ('recovery', 'Recuperación'),
        ('stretching', 'Estiramientos'),
        ('motivation', 'Motivación'),
    ]
    
    INTENSITY_LEVELS = [
        ('low', 'Baja'),
        ('medium', 'Media'),
        ('high', 'Alta'),
        ('very_high', 'Muy Alta'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('viewed', 'Visto'),
        ('accepted', 'Aceptado'),
        ('rejected', 'Rechazado'),
        ('completed', 'Completado'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recommendations',
        help_text='Usuario destinatario'
    )
    recommendation_type = models.CharField(
        max_length=100,
        choices=RECOMMENDATION_TYPES,
        help_text='Tipo de recomendación'
    )
    title = models.CharField(
        max_length=200,
        help_text='Título de la recomendación'
    )
    description = models.TextField(
        help_text='Descripción detallada'
    )
    intensity = models.CharField(
        max_length=20,
        choices=INTENSITY_LEVELS,
        default='medium',
        null=True,
        blank=True,
        help_text='Nivel de intensidad'
    )
    estimated_duration_minutes = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text='Duración estimada en minutos'
    )
    reason = models.CharField(
        max_length=500,
        help_text='Razón de la recomendación'
    )
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='pending',
        help_text='Estado de la recomendación'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    viewed_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Fecha en que el usuario vio la recomendación'
    )
    accepted_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Fecha en que fue aceptada'
    )
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Fecha en que fue completada'
    )
    
    class Meta:
        verbose_name = 'Recomendación'
        verbose_name_plural = 'Recomendaciones'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f'{self.user.username} - {self.title} ({self.get_status_display()})'
    
    def mark_as_viewed(self):
        """Mark recommendation as viewed"""
        if not self.viewed_at:
            from django.utils import timezone
            self.viewed_at = timezone.now()
            self.status = 'viewed'
            self.save()
    
    def accept(self):
        """Accept recommendation"""
        from django.utils import timezone
        self.accepted_at = timezone.now()
        self.status = 'accepted'
        self.save()
    
    def complete(self):
        """Mark recommendation as completed"""
        from django.utils import timezone
        self.completed_at = timezone.now()
        self.status = 'completed'
        self.save()
