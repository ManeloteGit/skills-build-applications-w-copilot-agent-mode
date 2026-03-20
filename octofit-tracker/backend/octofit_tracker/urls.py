"""
URL configuration for octofit_tracker project.
"""

import os
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Codespace configuration for URLs
codespace_name = os.environ.get('CODESPACE_NAME')
if codespace_name:
    base_url = f"https://{codespace_name}-8000.app.github.dev"
else:
    base_url = "http://localhost:8000"

@api_view(['GET'])
def api_root(request):
    """API root endpoint"""
    return Response({
        'message': 'Welcome to Octofit Tracker API',
        'version': '1.0.0',
        'endpoints': {
            'users': f'{base_url}/api/users/',
            'activities': f'{base_url}/api/activities/',
            'teams': f'{base_url}/api/teams/',
            'leaderboard': f'{base_url}/api/leaderboard/',
            'recommendations': f'{base_url}/api/recommendations/',
        }
    })

# Initialize routers
router = routers.DefaultRouter()

# Register app routers
from octofit_tracker.apps.users.views import UserViewSet
from octofit_tracker.apps.activities.views import ActivityViewSet
from octofit_tracker.apps.teams.views import TeamViewSet, TeamMemberViewSet
from octofit_tracker.apps.leaderboard.views import LeaderboardViewSet
from octofit_tracker.apps.recommendations.views import RecommendationViewSet

router.register(r'users', UserViewSet)
router.register(r'activities', ActivityViewSet)
router.register(r'teams', TeamViewSet)
router.register(r'team-members', TeamMemberViewSet)
router.register(r'leaderboard', LeaderboardViewSet)
router.register(r'recommendations', RecommendationViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api_root, name='api-root'),
    path('api/', include(router.urls)),
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
]
