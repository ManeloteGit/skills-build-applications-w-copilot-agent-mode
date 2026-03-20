"""
Recommendations App - Configuration for personalized workout suggestions
"""

from django.apps import AppConfig


class RecommendationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'octofit_tracker.apps.recommendations'
    verbose_name = 'Personalized Recommendations'
