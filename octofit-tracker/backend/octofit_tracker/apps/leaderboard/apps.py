"""
Leaderboard App - Configuration for competitive leaderboards
"""

from django.apps import AppConfig


class LeaderboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'octofit_tracker.apps.leaderboard'
    verbose_name = 'Competitive Leaderboard'
