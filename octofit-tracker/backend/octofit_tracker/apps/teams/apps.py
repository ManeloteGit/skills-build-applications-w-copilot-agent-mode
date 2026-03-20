"""
Teams App - Configuration for team management
"""

from django.apps import AppConfig


class TeamsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'octofit_tracker.apps.teams'
    verbose_name = 'Team Management'
