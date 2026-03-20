"""
Users App - Configuration and apps for user management
"""

from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'octofit_tracker.apps.users'
    verbose_name = 'User Management'
