"""
Serializers for Team API
"""

from rest_framework import serializers
from .models import Team, TeamMember
from octofit_tracker.apps.users.serializers import UserSerializer


class TeamSerializer(serializers.ModelSerializer):
    """Serializer for Team model"""
    
    leader_username = serializers.CharField(
        source='leader.username',
        read_only=True
    )
    actual_member_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Team
        fields = [
            'id', 'name', 'description', 'leader', 'leader_username',
            'member_count', 'actual_member_count', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_actual_member_count(self, obj):
        """Get actual member count"""
        return obj.get_members_count()


class TeamDetailSerializer(TeamSerializer):
    """Detailed serializer for Team with members"""
    
    leader = UserSerializer(read_only=True)
    members = serializers.SerializerMethodField()
    
    class Meta(TeamSerializer.Meta):
        fields = TeamSerializer.Meta.fields + ['members']
    
    def get_members(self, obj):
        """Get team members"""
        members = obj.members.all()
        return TeamMemberSerializer(members, many=True).data


class TeamCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating teams"""
    
    class Meta:
        model = Team
        fields = ['name', 'description']


class TeamMemberSerializer(serializers.ModelSerializer):
    """Serializer for TeamMember model"""
    
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    role_display = serializers.CharField(
        source='get_role_display',
        read_only=True
    )
    
    class Meta:
        model = TeamMember
        fields = [
            'id', 'team', 'user', 'user_id', 'role', 'role_display',
            'joined_at'
        ]
        read_only_fields = ['id', 'joined_at']


class TeamMemberUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating team members"""
    
    class Meta:
        model = TeamMember
        fields = ['role']
