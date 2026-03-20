"""
Leaderboard Models for Octofit Tracker
"""

from django.db import models
from octofit_tracker.apps.users.models import User
from octofit_tracker.apps.teams.models import Team


class Leaderboard(models.Model):
    """Model for weekly competitive leaderboards"""
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='leaderboard_entries',
        help_text='Usuario'
    )
    week_id = models.CharField(
        max_length=10,
        help_text='Identificador de la semana (YYYY-WW)'
    )
    points = models.PositiveIntegerField(
        default=0,
        help_text='Puntos totales de la semana'
    )
    activities_count = models.PositiveIntegerField(
        default=0,
        help_text='Número de actividades realizadas'
    )
    total_duration_minutes = models.PositiveIntegerField(
        default=0,
        help_text='Duración total en minutos'
    )
    total_calories = models.PositiveIntegerField(
        default=0,
        help_text='Calorías totales quemadas'
    )
    rank = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text='Posición en el ranking'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Clasificación'
        verbose_name_plural = 'Clasificaciones'
        unique_together = [['week_id', 'user']]
        ordering = ['week_id', 'rank']
        indexes = [
            models.Index(fields=['week_id', 'rank']),
            models.Index(fields=['user', 'week_id']),
        ]
    
    def __str__(self):
        return f'{self.user.username} - Semana {self.week_id} (Rango: {self.rank})'


class TeamLeaderboard(models.Model):
    """Model for team competitive leaderboards"""
    
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='leaderboard_entries',
        help_text='Equipo'
    )
    week_id = models.CharField(
        max_length=10,
        help_text='Identificador de la semana (YYYY-WW)'
    )
    points = models.PositiveIntegerField(
        default=0,
        help_text='Puntos totales del equipo'
    )
    total_activities = models.PositiveIntegerField(
        default=0,
        help_text='Total de actividades del equipo'
    )
    total_duration_minutes = models.PositiveIntegerField(
        default=0,
        help_text='Duración total en minutos'
    )
    total_calories = models.PositiveIntegerField(
        default=0,
        help_text='Calorías totales quemadas'
    )
    rank = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text='Posición en el ranking'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Clasificación de Equipo'
        verbose_name_plural = 'Clasificaciones de Equipos'
        unique_together = [['week_id', 'team']]
        ordering = ['week_id', 'rank']
        indexes = [
            models.Index(fields=['week_id', 'rank']),
            models.Index(fields=['team', 'week_id']),
        ]
    
    def __str__(self):
        return f'{self.team.name} - Semana {self.week_id} (Rango: {self.rank})'
