"""
Views for User API
"""

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from .models import User
from .serializers import (
    UserSerializer, UserDetailSerializer, UserRegistrationSerializer,
    UserProfileUpdateSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for User management"""
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['created_at', 'fitness_level']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'retrieve':
            return UserDetailSerializer
        elif self.action == 'update_profile':
            return UserProfileUpdateSerializer
        elif self.action == 'create':
            return UserRegistrationSerializer
        return self.serializer_class
    
    def get_permissions(self):
        """Set permissions based on action"""
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action in ['update', 'partial_update', 'update_profile', 'change_password']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Get current authenticated user"""
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data)
    
    @action(detail=True, methods=['put', 'patch'], permission_classes=[IsAuthenticated])
    def update_profile(self, request, pk=None):
        """Update user profile information"""
        user = get_object_or_404(User, pk=pk)
        
        # Check if user is updating their own profile or is admin
        if request.user != user and not request.user.is_staff:
            return Response(
                {'detail': 'No tiene permiso para actualizar este perfil.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def change_password(self, request):
        """Change user password"""
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        new_password2 = request.data.get('new_password2')
        
        if not user.check_password(old_password):
            return Response(
                {'old_password': 'Contraseña actual incorrecta.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if new_password != new_password2:
            return Response(
                {'new_password2': 'Las contraseñas no coinciden.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user.set_password(new_password)
        user.save()
        
        return Response({'detail': 'Contraseña actualizada correctamente.'})
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def leaderboard(self, request):
        """Get users ranked by fitness points"""
        from django.db.models import Sum, Count
        from octofit_tracker.apps.activities.models import Activity
        
        users = User.objects.annotate(
            total_activities=Count('activity'),
            total_duration=Sum('activity__duration_minutes'),
            total_calories=Sum('activity__calories_burned')
        ).order_by('-total_calories')
        
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
