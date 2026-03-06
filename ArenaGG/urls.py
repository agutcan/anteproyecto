"""
URL configuration for ArenaGG project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls

# DRF router
from rest_framework import routers
from web import views as web_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = routers.DefaultRouter()
router.register(r'games', web_views.GameViewSet)
router.register(r'teams', web_views.TeamViewSet)
router.register(r'players', web_views.PlayerViewSet)
router.register(r'tournaments', web_views.TournamentViewSet)
router.register(r'tournament-teams', web_views.TournamentTeamViewSet)
router.register(r'matches', web_views.MatchViewSet)
router.register(r'match-results', web_views.MatchResultViewSet)
router.register(r'match-logs', web_views.MatchLogViewSet)
router.register(r'rewards', web_views.RewardViewSet)
router.register(r'redemptions', web_views.RedemptionViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('web.urls')),
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

] + debug_toolbar_urls()
