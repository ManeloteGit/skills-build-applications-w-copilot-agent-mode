"""
Views for Activity API
"""

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Sum, Avg, Max
from django.utils import timezone
from datetime import timedelta
from .models import Activity
from .serializers import (
    ActivitySerializer, ActivityDetailSerializer,
    ActivityCreateUpdateSerializer, ActivityStatsSerializer
)


class ActivityViewSet(viewsets.ModelViewSet):
    """ViewSet for Activity management"""
    
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'activity_type', 'notes']
    ordering_fields = ['performed_at', 'calories_burned', 'duration_minutes']
    ordering = ['-performed_at']
    
    def get_queryset(self):
        """Return activities for current user or all if admin"""
        if self.request.user.is_staff:
            return Activity.objects.all()
        return Activity.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'retrieve':
            return ActivityDetailSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ActivityCreateUpdateSerializer
        return self.serializer_class
    
    def perform_create(self, serializer):
        """Set user to current user when creating"""
        serializer.save(user=self.request.user)
    
    def perform_update(self, serializer):
        """Ensure user cannot change the activity owner"""
        activity = self.get_object()
        if activity.user != self.request.user and not self.request.user.is_staff:
            raise PermissionError('No puede modificar actividades de otros usuarios.')
        serializer.save()
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get statistics for user activities"""
        activities = self.get_queryset()
        
        stats = {
            'total_activities': activities.count(),
            'total_duration_minutes': activities.aggregate(
                Sum('duration_minutes')
            )['duration_minutes__sum'] or 0,
            'total_distance_km': activities.aggregate(
                Sum('distance_km')
            )['distance_km__sum'] or 0,
            'total_calories_burned': activities.aggregate(
                Sum('calories_burned')
            )['calories_burned__sum'] or 0,
            'average_duration': activities.aggregate(
                Avg('duration_minutes')
            )['duration_minutes__avg'] or 0,
            'average_calories': activities.aggregate(
                Avg('calories_burned')
            )['calories_burned__avg'] or 0,
            'most_common_type': (
                activities.values('activity_type')
                .annotate(count=Count('id'))
                .order_by('-count')
                .first() or {}
            ).get('activity_type', 'N/A'),
            'last_activity': activities.aggregate(
                Max('performed_at')
            )['performed_at__max'] or None,
        }
        
        serializer = ActivityStatsSerializer(stats)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def today(self, request):
        """Get today's activities"""
        today = timezone.now().date()
        activities = self.get_queryset().filter(
            performed_at__date=today
        )
        serializer = self.get_serializer(activities, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def week(self, request):
        """Get current week's activities"""
        today = timezone.now()
        week_start = today - timedelta(days=today.weekday())
        activities = self.get_queryset().filter(
            performed_at__gte=week_start
        )
        serializer = self.get_serializer(activities, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def month(self, request):
        """Get current month's activities"""
        today = timezone.now()
        month_start = today.replace(day=1)
        activities = self.get_queryset().filter(
            performed_at__gte=month_start
        )
        serializer = self.get_serializer(activities, many=True)
        return Response(serializer.data)
