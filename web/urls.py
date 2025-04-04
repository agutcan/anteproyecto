from django.urls import path
from . import views  # Asegúrate de que las vistas estén importadas
from django.conf import settings
from django.conf.urls.static import static

# Definir el nombre de la aplicación para los nombres de las rutas
app_name = 'web'

# Definir las rutas de URL para la aplicación
urlpatterns = [

    path("api/tournaments/", views.TournamentListAPI.as_view(), name="tournamentListApi"),
    # Ruta para la vista principal del índice
    path('', views.PublicIndexView.as_view(), name='publicIndex'),  # Cambia esto por las vistas que tengas
    path('start/', views.IndexView.as_view(), name='index'),  # Cambia esto por las vistas que tengas
    path('player/<int:pk>', views.PlayerDetailView.as_view(), name='playerDetailView'),  # Vista de lista de jugadores
    path('premium/', views.BecomePremiumView.as_view(), name='becomePremium'),  # Vista de lista de jugadores
    path('tournament/<int:pk>', views.TournamentDetailView.as_view(), name='tournamentDetailView'),  # Vista los detalles de un torneo
    path('tournament/create/', views.TournamentCreateView.as_view(), name='tournamentCreateView'),  # Vista los detalles de un torneo
    path('profile/<int:pk>', views.PlayerProfileDetailView.as_view(), name='playerProfileDetailView'),  # Vista de lista de jugadores
    path('ranking/', views.RankingView.as_view(), name='rankingView'),  # Vista para mostrar un ranking de jugadores
    path('privacy_policy/', views.PrivacyPolicyView.as_view(), name='privacyPolicyView'),  # Vista para mostrar un ranking de jugadores
    path('rewards/', views.RewardListView.as_view(), name='rewardListView'),  # Vista para mostrar las recompensas
    path('game/<int:pk>', views.GameDetailView.as_view(), name='gameDetailView'),  # Vista de lista de juegos con sus torneos
    path('accounts/register/', views.RegisterView.as_view(), name='register'),  # Vista para registro de usuarios

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)