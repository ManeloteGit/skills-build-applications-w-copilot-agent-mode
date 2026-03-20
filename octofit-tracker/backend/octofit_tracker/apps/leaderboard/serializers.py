"""
Serializers for Leaderboard API
"""

from rest_framework import serializers
from .models import Leaderboard, TeamLeaderboard
from octofit_tracker.apps.users.serializers import UserSerializer
from octofit_tracker.apps.teams.serializers import TeamSerializer


class LeaderboardSerializer(serializers.ModelSerializer):
    """Serializer for Leaderboard model"""
    
    user_username = serializers.CharField(
        source='user.username',
        read_only=True
    )
    
    class Meta:
        model = Leaderboard
        fields = [
            'id', 'user', 'user_username', 'week_id', 'points',
            'activities_count', 'total_duration_minutes', 'total_calories',
            'rank', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class LeaderboardDetailSerializer(LeaderboardSerializer):
    """Detailed serializer for Leaderboard with user info"""
    
    user = UserSerializer(read_only=True)
    
    class Meta(LeaderboardSerializer.Meta):
        fields = LeaderboardSerializer.Meta.fields


class TeamLeaderboardSerializer(serializers.ModelSerializer):
    """Serializer for TeamLeaderboard model"""
    
    team_name = serializers.CharField(
        source='team.name',
        read_only=True
    )
    
    class Meta:
        model = TeamLeaderboard
        fields = [
            'id', 'team', 'team_name', 'week_id', 'points',
            'total_activities', 'total_duration_minutes', 'total_calories',
            'rank', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class TeamLeaderboardDetailSerializer(TeamLeaderboardSerializer):
    """Detailed serializer for TeamLeaderboard with team info"""
    
    team = TeamSerializer(read_only=True)
    
    class Meta(TeamLeaderboardSerializer.Meta):
        fields = TeamLeaderboardSerializer.Meta.fields
