"""
Serializers for Recommendation API
"""

from rest_framework import serializers
from .models import Recommendation
from octofit_tracker.apps.users.serializers import UserSerializer


class RecommendationSerializer(serializers.ModelSerializer):
    """Serializer for Recommendation model"""
    
    user_username = serializers.CharField(
        source='user.username',
        read_only=True
    )
    recommendation_type_display = serializers.CharField(
        source='get_recommendation_type_display',
        read_only=True
    )
    status_display = serializers.CharField(
        source='get_status_display',
        read_only=True
    )
    
    class Meta:
        model = Recommendation
        fields = [
            'id', 'user', 'user_username', 'recommendation_type',
            'recommendation_type_display', 'title', 'description',
            'intensity', 'estimated_duration_minutes', 'reason',
            'status', 'status_display', 'created_at', 'viewed_at',
            'accepted_at', 'completed_at'
        ]
        read_only_fields = [
            'id', 'created_at', 'viewed_at', 'accepted_at', 'completed_at'
        ]


class RecommendationDetailSerializer(RecommendationSerializer):
    """Detailed serializer for Recommendation with user info"""
    
    user = UserSerializer(read_only=True)
    
    class Meta(RecommendationSerializer.Meta):
        fields = RecommendationSerializer.Meta.fields


class RecommendationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating recommendations"""
    
    class Meta:
        model = Recommendation
        fields = [
            'recommendation_type', 'title', 'description',
            'intensity', 'estimated_duration_minutes', 'reason'
        ]


class RecommendationUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating recommendations"""
    
    class Meta:
        model = Recommendation
        fields = [
            'title', 'description', 'intensity',
            'estimated_duration_minutes', 'reason', 'status'
        ]


class RecommendationActionSerializer(serializers.Serializer):
    """Serializer for recommendation actions"""
    
    action = serializers.ChoiceField(
        choices=['view', 'accept', 'reject', 'complete']
    )
