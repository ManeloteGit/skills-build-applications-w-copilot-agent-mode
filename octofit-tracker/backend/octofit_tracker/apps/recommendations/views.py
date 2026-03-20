"""
Views for Recommendation API
"""

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Recommendation
from .serializers import (
    RecommendationSerializer, RecommendationDetailSerializer,
    RecommendationCreateSerializer, RecommendationUpdateSerializer,
    RecommendationActionSerializer
)


class RecommendationViewSet(viewsets.ModelViewSet):
    """ViewSet for Recommendation management"""
    
    serializer_class = RecommendationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'reason']
    ordering_fields = ['created_at', 'recommendation_type', 'status']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Return recommendations for current user"""
        if self.request.user.is_staff:
            return Recommendation.objects.all()
        return Recommendation.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'retrieve':
            return RecommendationDetailSerializer
        elif self.action == 'create':
            return RecommendationCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return RecommendationUpdateSerializer
        return self.serializer_class
    
    def perform_create(self, serializer):
        """Set user to current user when creating (admin only)"""
        if not self.request.user.is_staff:
            return Response(
                {'detail': 'Solo administradores pueden crear recomendaciones.'},
                status=status.HTTP_403_FORBIDDEN
            )
        user_id = self.request.data.get('user_id')
        serializer.save(user_id=user_id)
    
    @action(detail=True, methods=['post'])
    def view(self, request, pk=None):
        """Mark recommendation as viewed"""
        recommendation = self.get_object()
        recommendation.mark_as_viewed()
        serializer = self.get_serializer(recommendation)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        """Accept recommendation"""
        recommendation = self.get_object()
        recommendation.accept()
        serializer = self.get_serializer(recommendation)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Reject recommendation"""
        recommendation = self.get_object()
        recommendation.status = 'rejected'
        recommendation.save()
        serializer = self.get_serializer(recommendation)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Mark recommendation as completed"""
        recommendation = self.get_object()
        recommendation.complete()
        serializer = self.get_serializer(recommendation)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def pending(self, request):
        """Get pending recommendations"""
        recommendations = self.get_queryset().filter(status='pending')
        page = self.paginate_queryset(recommendations)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(recommendations, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get active recommendations (pending and viewed)"""
        recommendations = self.get_queryset().filter(
            status__in=['pending', 'viewed']
        )
        page = self.paginate_queryset(recommendations)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(recommendations, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def completed(self, request):
        """Get completed recommendations"""
        recommendations = self.get_queryset().filter(status='completed')
        page = self.paginate_queryset(recommendations)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(recommendations, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get recommendation statistics"""
        queryset = self.get_queryset()
        stats = {
            'total_recommendations': queryset.count(),
            'pending': queryset.filter(status='pending').count(),
            'viewed': queryset.filter(status='viewed').count(),
            'accepted': queryset.filter(status='accepted').count(),
            'rejected': queryset.filter(status='rejected').count(),
            'completed': queryset.filter(status='completed').count(),
        }
        return Response(stats)
