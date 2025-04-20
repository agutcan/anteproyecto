from django.urls import path
from . import views  # Asegúrate de que las vistas estén importadas
from django.conf import settings
from django.conf.urls.static import static

# Definir el nombre de la aplicación para los nombres de las rutas
app_name = 'web'

# Definir las rutas de URL para la aplicación
urlpatterns = [

    path("api/tournaments/", views.TournamentListAPI.as_view(), name="tournamentListApi"),
    path('api/player-stats/', views.PlayerStatsListAPI.as_view(), name='playerStatsListApi'),

    # Ruta para la vista principal del índice
    path('', views.PublicIndexView.as_view(), name='publicIndex'),  # Cambia esto por las vistas que tengas
    path('start/', views.IndexView.as_view(), name='indexView'),  # Cambia esto por las vistas que tengas
    path('start/player/<int:pk>', views.PlayerDetailView.as_view(), name='playerDetailView'),  # Vista de lista de jugadores
    path('start/premium/', views.BecomePremiumView.as_view(), name='becomePremiumView'),  # Vista de lista de jugadores
    path('start/support/', views.SupportView.as_view(), name='supportView'),  # Vista de lista de jugadores
    path('start/faq/', views.FaqView.as_view(), name='faqView'),  # Vista de lista de jugadores
    path('start/tournament/<int:pk>', views.TournamentDetailView.as_view(), name='tournamentDetailView'),  # Vista los detalles de un torneo
    path('start/tournament/match/<int:pk>', views.MatchDetailView.as_view(), name='matchDetailView'),  # Vista los detalles de un torneo
    path('start/tournaments/', views.TournamentListView.as_view(), name='tournamentListView'),  # Vista los detalles de un torneo
    path('start/tournament/<int:pk>/join/', views.JoinTeamListView.as_view(), name='joinTeamListView'),
    path('start/tournament/<int:pk>/create_team/', views.TeamCreateView.as_view(), name='teamCreateView'),
    path('start/tournament/create/', views.TournamentCreateView.as_view(), name='tournamentCreateView'),
    path('start/tournament/leave/<int:pk>', views.LeaveTournamentView.as_view(), name='leaveTournamentView'),
    path('start/my_tournaments/<int:pk>', views.MyTournamentListView.as_view(), name='myTournamentListView'),  # Vista los detalles de un torneo
    path('start/games/', views.GameListView.as_view(), name='gameListView'),  # Vista los detalles de un torneo
    path('start/tournament/create/', views.TournamentCreateView.as_view(), name='tournamentCreateView'),  # Vista los detalles de un torneo
    path('start/profile/<int:pk>', views.PlayerProfileDetailView.as_view(), name='playerProfileDetailView'),  # Vista de lista de jugadores
    path('start/profile/update/<int:pk>/', views.PlayerUpdateView.as_view(), name='playerUpdateView'),  # Vista de lista de jugadores
    path('start/ranking/', views.RankingView.as_view(), name='rankingView'),  # Vista para mostrar un ranking de jugadores
    path('privacy_policy/', views.PrivacyPolicyView.as_view(), name='privacyPolicyView'),  # Vista para mostrar un ranking de jugadores
    path('temrs_of_use/', views.TermsOfUseView.as_view(), name='termsOfUseView'),  # Vista para mostrar un ranking de jugadores
    path('start/rewards/', views.RewardListView.as_view(), name='rewardListView'),  # Vista para mostrar las recompensas
    path('start/how_it_works/', views.HowItWorkView.as_view(), name='howItWorkView'),  # Vista para mostrar las recompensas
    path('start/game/<int:pk>', views.GameDetailView.as_view(), name='gameDetailView'),  # Vista de lista de juegos con sus torneos
    path('accounts/register/', views.RegisterView.as_view(), name='register'),  # Vista para registro de usuarios

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)