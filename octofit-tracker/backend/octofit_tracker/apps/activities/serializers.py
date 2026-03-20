"""
Serializers for Activity API
"""

from rest_framework import serializers
from .models import Activity
from octofit_tracker.apps.users.serializers import UserSerializer


class ActivitySerializer(serializers.ModelSerializer):
    """Serializer for Activity model"""
    
    user_username = serializers.CharField(
        source='user.username',
        read_only=True
    )
    activity_type_display = serializers.CharField(
        source='get_activity_type_display_es',
        read_only=True
    )
    intensity_display = serializers.CharField(
        source='get_intensity_level_display',
        read_only=True
    )
    
    class Meta:
        model = Activity
        fields = [
            'id', 'user', 'user_username', 'activity_type', 'activity_type_display',
            'name', 'duration_minutes', 'distance_km', 'calories_burned',
            'intensity_level', 'intensity_display', 'notes', 'performed_at',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_duration_minutes(self, value):
        """Validate duration is positive"""
        if value <= 0:
            raise serializers.ValidationError(
                'La duración debe ser mayor a 0 minutos.'
            )
        return value


class ActivityDetailSerializer(ActivitySerializer):
    """Detailed serializer for Activity with user information"""
    
    user = UserSerializer(read_only=True)
    
    class Meta(ActivitySerializer.Meta):
        fields = ActivitySerializer.Meta.fields


class ActivityCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating activities"""
    
    class Meta:
        model = Activity
        fields = [
            'activity_type', 'name', 'duration_minutes',
            'distance_km', 'calories_burned', 'intensity_level',
            'notes', 'performed_at'
        ]


class ActivityStatsSerializer(serializers.Serializer):
    """Serializer for activity statistics"""
    
    total_activities = serializers.IntegerField()
    total_duration_minutes = serializers.IntegerField()
    total_distance_km = serializers.FloatField()
    total_calories_burned = serializers.IntegerField()
    average_duration = serializers.FloatField()
    average_calories = serializers.FloatField()
    most_common_type = serializers.CharField()
    last_activity = serializers.DateTimeField()
