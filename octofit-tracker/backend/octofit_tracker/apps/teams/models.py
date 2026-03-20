"""
Team Models for Octofit Tracker
"""

from django.db import models
from octofit_tracker.apps.users.models import User


class Team(models.Model):
    """Model for team management"""
    
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text='Nombre del equipo'
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text='Descripción del equipo'
    )
    leader = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='led_teams',
        help_text='Líder del equipo'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    member_count = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(
        default=True,
        help_text='Indica si el equipo está activo'
    )
    
    class Meta:
        verbose_name = 'Equipo'
        verbose_name_plural = 'Equipos'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['leader']),
        ]
    
    def __str__(self):
        return f'{self.name} (Líder: {self.leader.username})'
    
    def get_members_count(self):
        """Get actual count of team members"""
        return self.members.count()


class TeamMember(models.Model):
    """Model for team membership"""
    
    ROLE_CHOICES = [
        ('member', 'Miembro'),
        ('coach', 'Entrenador'),
        ('manager', 'Gerente'),
    ]
    
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='members',
        help_text='Equipo'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='team_memberships',
        help_text='Usuario miembro'
    )
    joined_at = models.DateTimeField(auto_now_add=True)
    role = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES,
        default='member',
        help_text='Rol del miembro en el equipo'
    )
    
    class Meta:
        verbose_name = 'Miembro del Equipo'
        verbose_name_plural = 'Miembros del Equipo'
        unique_together = [['team', 'user']]
        ordering = ['-joined_at']
        indexes = [
            models.Index(fields=['team', 'user']),
            models.Index(fields=['user']),
        ]
    
    def __str__(self):
        return f'{self.user.username} - {self.team.name} ({self.get_role_display()})'
    
    def is_coach(self):
        """Check if user is coach"""
        return self.role == 'coach'
    
    def is_manager(self):
        """Check if user is manager"""
        return self.role == 'manager'
