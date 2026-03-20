"""
Views for Team API
"""

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Team, TeamMember
from .serializers import (
    TeamSerializer, TeamDetailSerializer, TeamCreateUpdateSerializer,
    TeamMemberSerializer, TeamMemberUpdateSerializer
)


class TeamViewSet(viewsets.ModelViewSet):
    """ViewSet for Team management"""
    
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'member_count']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Return teams where user is member or leader"""
        return Team.objects.filter(
            Q(leader=self.request.user) |
            Q(members__user=self.request.user)
        ).distinct()
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'retrieve':
            return TeamDetailSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return TeamCreateUpdateSerializer
        return self.serializer_class
    
    def perform_create(self, serializer):
        """Set leader to current user when creating"""
        serializer.save(leader=self.request.user)
    
    @action(detail=True, methods=['post'])
    def add_member(self, request, pk=None):
        """Add member to team"""
        team = self.get_object()
        
        # Check if user is leader or manager
        if team.leader != request.user:
            member = TeamMember.objects.filter(
                team=team,
                user=request.user,
                role__in=['coach', 'manager']
            ).first()
            if not member:
                return Response(
                    {'detail': 'No tiene permisos para agregar miembros.'},
                    status=status.HTTP_403_FORBIDDEN
                )
        
        user_id = request.data.get('user_id')
        if not user_id:
            return Response(
                {'detail': 'user_id es requerido.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        from octofit_tracker.apps.users.models import User
        user = get_object_or_404(User, id=user_id)
        
        # Check if user is already member
        if TeamMember.objects.filter(team=team, user=user).exists():
            return Response(
                {'detail': 'El usuario ya es miembro del equipo.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        member = TeamMember.objects.create(team=team, user=user)
        serializer = TeamMemberSerializer(member)
        
        # Update member count
        team.member_count = team.get_members_count()
        team.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def remove_member(self, request, pk=None):
        """Remove member from team"""
        team = self.get_object()
        
        # Check if user is leader
        if team.leader != request.user:
            return Response(
                {'detail': 'No tiene permisos para remover miembros.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        user_id = request.data.get('user_id')
        member = get_object_or_404(TeamMember, team=team, user_id=user_id)
        
        if member.user == team.leader:
            return Response(
                {'detail': 'No puede remover al líder del equipo.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        member.delete()
        
        # Update member count
        team.member_count = team.get_members_count()
        team.save()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        """Get team members"""
        team = self.get_object()
        members = team.members.all()
        serializer = TeamMemberSerializer(members, many=True)
        return Response(serializer.data)


class TeamMemberViewSet(viewsets.ModelViewSet):
    """ViewSet for TeamMember management"""
    
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user__username', 'team__name']
    ordering_fields = ['joined_at', 'role']
    ordering = ['-joined_at']
    
    def get_queryset(self):
        """Return team memberships for current user"""
        return TeamMember.objects.filter(
            Q(user=self.request.user) |
            Q(team__leader=self.request.user)
        ).distinct()
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action in ['update', 'partial_update']:
            return TeamMemberUpdateSerializer
        return self.serializer_class
    
    def perform_update(self, serializer):
        """Validate member update permissions"""
        member = self.get_object()
        if member.team.leader != self.request.user:
            raise PermissionError('No tiene permisos para actualizar miembros.')
        serializer.save()
