"""
Activity Models for Octofit Tracker
"""

from django.db import models
from django.core.validators import MinValueValidator
from octofit_tracker.apps.users.models import User


class Activity(models.Model):
    """Model for tracking user activities"""
    
    ACTIVITY_TYPES = [
        ('running', 'Correr'),
        ('walking', 'Caminar'),
        ('cycling', 'Ciclismo'),
        ('swimming', 'Natación'),
        ('gym', 'Gimnasio'),
        ('yoga', 'Yoga'),
        ('sports', 'Deportes'),
        ('other', 'Otro'),
    ]
    
    INTENSITY_LEVELS = [
        ('low', 'Baja'),
        ('medium', 'Media'),
        ('high', 'Alta'),
        ('very_high', 'Muy Alta'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='activity',
        help_text='Usuario que realizó la actividad'
    )
    activity_type = models.CharField(
        max_length=50,
        choices=ACTIVITY_TYPES,
        help_text='Tipo de actividad'
    )
    name = models.CharField(
        max_length=200,
        help_text='Nombre de la actividad'
    )
    duration_minutes = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text='Duración en minutos'
    )
    distance_km = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text='Distancia recorrida en kilómetros'
    )
    calories_burned = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text='Calorías quemadas'
    )
    intensity_level = models.CharField(
        max_length=20,
        choices=INTENSITY_LEVELS,
        default='medium',
        help_text='Nivel de intensidad'
    )
    notes = models.TextField(
        blank=True,
        null=True,
        help_text='Notas adicionales sobre la actividad'
    )
    performed_at = models.DateTimeField(
        help_text='Fecha y hora en que se realizó la actividad'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Actividad'
        verbose_name_plural = 'Actividades'
        ordering = ['-performed_at']
        indexes = [
            models.Index(fields=['user', '-performed_at']),
            models.Index(fields=['activity_type']),
            models.Index(fields=['performed_at']),
        ]
    
    def __str__(self):
        return f'{self.user.username} - {self.get_activity_type_display()} - {self.performed_at}'
    
    def get_activity_type_display_es(self):
        """Get Spanish activity type display"""
        return dict(self.ACTIVITY_TYPES).get(self.activity_type)
