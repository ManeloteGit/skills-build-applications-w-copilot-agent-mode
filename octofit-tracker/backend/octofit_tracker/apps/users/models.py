"""
User Models for Octofit Tracker
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator


class User(AbstractUser):
    """Extended user model with fitness profile information"""
    
    GENDER_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]
    
    FITNESS_LEVEL_CHOICES = [
        ('beginner', 'Principiante'),
        ('intermediate', 'Intermedio'),
        ('advanced', 'Avanzado'),
        ('athlete', 'Atleta'),
    ]
    
    # Profile information
    height_cm = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(100), MaxValueValidator(250)],
        help_text='Altura en centímetros'
    )
    weight_kg = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(30), MaxValueValidator(300)],
        help_text='Peso en kilogramos'
    )
    age = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(13), MaxValueValidator(120)],
        help_text='Edad del usuario'
    )
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        null=True,
        blank=True,
        help_text='Género del usuario'
    )
    fitness_level = models.CharField(
        max_length=20,
        choices=FITNESS_LEVEL_CHOICES,
        default='beginner',
        help_text='Nivel de aptitud física'
    )
    bio = models.TextField(
        blank=True,
        null=True,
        help_text='Biografía del usuario'
    )
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        null=True,
        blank=True,
        help_text='Foto de perfil'
    )
    
    # Account status
    is_active = models.BooleanField(
        default=True,
        help_text='Indica si el usuario está activo'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['email']),
        ]
    
    def __str__(self):
        return f'{self.get_full_name()} ({self.username})'
    
    def get_bmi(self):
        """Calculate BMI (Body Mass Index)"""
        if self.height_cm and self.weight_kg:
            height_m = self.height_cm / 100
            return round(self.weight_kg / (height_m ** 2), 2)
        return None
    
    def get_fitness_level_display_es(self):
        """Get Spanish fitness level display"""
        return dict(self.FITNESS_LEVEL_CHOICES).get(self.fitness_level)
