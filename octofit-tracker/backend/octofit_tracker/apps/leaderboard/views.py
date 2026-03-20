"""
Views for Leaderboard API
"""

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Leaderboard, TeamLeaderboard
from .serializers import (
    LeaderboardSerializer, LeaderboardDetailSerializer,
    TeamLeaderboardSerializer, TeamLeaderboardDetailSerializer
)


def get_week_id(date=None):
    """Get week ID in format YYYY-WW"""
    if date is None:
        date = timezone.now()
    iso_year, iso_week, iso_weekday = date.isocalendar()
    return f"{iso_year}-{iso_week:02d}"


class LeaderboardViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Leaderboard"""
    
    serializer_class = LeaderboardSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['rank', 'points', 'activities_count']
    ordering = ['rank']
    
    def get_queryset(self):
        """Return leaderboard for specified or current week"""
        week_id = self.request.query_params.get(
            'week_id',
            get_week_id()
        )
        return Leaderboard.objects.filter(week_id=week_id).select_related('user')
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'retrieve':
            return LeaderboardDetailSerializer
        return self.serializer_class
    
    @action(detail=False, methods=['get'])
    def current_week(self, request):
        """Get current week's leaderboard"""
        week_id = get_week_id()
        leaderboard = self.get_queryset().filter(week_id=week_id)
        
        page = self.paginate_queryset(leaderboard)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(leaderboard, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def top_ten(self, request):
        """Get top 10 users overall"""
        from django.db.models import Sum
        from octofit_tracker.apps.users.models import User
        
        users = User.objects.annotate(
            total_points=Sum('leaderboard_entries__points')
        ).order_by('-total_points')[:10]
        
        return Response({
            'top_users': [
                {
                    'rank': idx + 1,
                    'user': user.username,
                    'total_points': user.total_points or 0
                }
                for idx, user in enumerate(users)
            ]
        })
    
    @action(detail=False, methods=['get'])
    def user_history(self, request):
        """Get leaderboard history for a user"""
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response(
                {'detail': 'user_id query parameter es requerido.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        history = self.get_queryset().filter(user_id=user_id).order_by('-week_id')
        serializer = self.get_serializer(history, many=True)
        return Response(serializer.data)


class TeamLeaderboardViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Team Leaderboard"""
    
    serializer_class = TeamLeaderboardSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['rank', 'points']
    ordering = ['rank']
    
    def get_queryset(self):
        """Return team leaderboard for specified or current week"""
        week_id = self.request.query_params.get(
            'week_id',
            get_week_id()
        )
        return TeamLeaderboard.objects.filter(
            week_id=week_id
        ).select_related('team')
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'retrieve':
            return TeamLeaderboardDetailSerializer
        return self.serializer_class
    
    @action(detail=False, methods=['get'])
    def current_week(self, request):
        """Get current week's team leaderboard"""
        week_id = get_week_id()
        leaderboard = self.get_queryset().filter(week_id=week_id)
        
        page = self.paginate_queryset(leaderboard)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(leaderboard, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def team_history(self, request):
        """Get leaderboard history for a team"""
        team_id = request.query_params.get('team_id')
        if not team_id:
            return Response(
                {'detail': 'team_id query parameter es requerido.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        history = self.get_queryset().filter(team_id=team_id).order_by('-week_id')
        serializer = self.get_serializer(history, many=True)
        return Response(serializer.data)
