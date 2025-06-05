from django.urls import path
from . import views  # Asegúrate de que las vistas estén importadas
from django.conf import settings
from django.conf.urls.static import static

# Definir el nombre de la aplicación para los nombres de las rutas
app_name = 'web'

# Definir las rutas de URL para la aplicación
urlpatterns = [

    #path("api/tournaments/", views.TournamentListAPI.as_view(), name="tournamentListApi"),  # Api para el calendario con los torneos
    path('api/player-stats/', views.PlayerStatsListAPI.as_view(), name='playerStatsListApi'),  # Api para el gráfico con las estadísticas de cada jugador

    path('', views.IndexView.as_view(), name='indexView'),  # Vista principal
    path('premium/', views.PremiumView.as_view(), name='premiumView'),  # Vista para la página de Premium/VIP
    path('premium/upgrade/', views.UpgradeToPremiumView.as_view(), name='upgradeToPremiumView'),  # Vista para actualizar el rol a Premium
    path('support/', views.SupportView.as_view(), name='supportView'),  # Vista para la página de contacto
    path('faq/', views.FaqView.as_view(), name='faqView'),  # Vista para la página de preguntas 
    path('game/<int:pk>', views.GameDetailView.as_view(), name='gameDetailView'),  # Vista para mostrar los detalles de un juego
    path('game/', views.GameListView.as_view(), name='gameListView'),  # Vista para listar todos los juegos
    path('tournament/', views.TournamentListView.as_view(), name='tournamentListView'),  # Vista para listar todos los torneos
    path('tournament/<int:pk>', views.TournamentDetailView.as_view(), name='tournamentDetailView'),  # Vista para los detalles de un torneo
    path('tournament/match/<int:pk>', views.MatchDetailView.as_view(), name='matchDetailView'),  # Vista para los detalles de una partida
    path('tournament/<int:pk>/join/', views.JoinTeamInTournamentListView.as_view(), name='joinTeamInTournamentListView'),   # Vista para ver los torneos a los que te puedes unir
    path('tournament/<int:pk>/create_team/', views.TeamCreateInTournamentView.as_view(), name='teamCreateInTournamentView'),   # Vista para crear un equipo dentro de un torneo
    path('tournament/<int:tournament_id>/<int:team_id>/inscribe_team/', views.TeamInscribeInTournamentView.as_view(), name='teamInscribeInTournamentView'),   # Vista para crear un equipo dentro de un torneo
    path('tournament/create_team/', views.TeamCreateView.as_view(), name='teamCreateView'),   # Vista para crear un equipo
    path('tournament/create/', views.TournamentCreateView.as_view(), name='tournamentCreateView'),   # Vista para crear un torneo
    path('tournament/leave/<int:pk>', views.LeaveTournamentView.as_view(), name='leaveTournamentView'),   # Vista para abandonar un torneo
    path('tournament/<int:pk>/logs/', views.TournamentLogsView.as_view(), name='tournamentLogsView'),  # Vista para listar los logs de las partidas de un torneo
    path('my_tournaments/<int:pk>', views.MyTournamentListView.as_view(), name='myTournamentListView'),  # Vista para listar los torneos en los que he participado o estoy inscrito
    path('my_team/<int:pk>', views.PlayerTeamDetailView.as_view(), name='playerTeamDetailView'),  # Vista para mostrar los detalles del equipo al que pertenece
    path('team/<int:pk>/delete/', views.TeamDeleteView.as_view(), name='teamDeleteView'),   # Vista para eliminar un equipo
    path('team/<int:team_id>/<int:player_id>/', views.TeamKickView.as_view(), name='teamKickView'),
    path('team/<int:pk>/search_players/', views.ToggleSearchingTeammatesView.as_view(), name='toggleSearchingTeammatesView'),  # Vista para cambiar el estado del campo search_players
    path('join_team_list/', views.TeamJoinListView.as_view(), name='teamJoinListView'),   # Vista para listar los torneos a los que te puedes unir dentro de un torneo
    path('join_team/<int:pk>', views.JoinTeamView.as_view(), name='joinTeamView'),   # Vista para listar los torneos a los que te puedes unir dentro de un torneo
    path('leave_team/<int:pk>', views.LeaveTeamView.as_view(), name='leaveTeamView'),   # Vista para listar los torneos a los que te puedes unir dentro de un torneo
    path('profile/<int:pk>', views.PlayerProfileDetailView.as_view(), name='playerProfileDetailView'),  # Vista para los detalles del perfil de un usuario
    path('profile/update/<int:pk>/', views.PlayerUpdateView.as_view(), name='playerUpdateView'),  # Vista para actualizar los detalles del perfil de un usuario
    path('ranking/', views.RankingView.as_view(), name='rankingView'),  # Vista para mostrar un ranking de jugadores
    path('privacy_policy/', views.PrivacyPolicyView.as_view(), name='privacyPolicyView'),  # Vista para mostrar las politicas de privacidad
    path('temrs_of_use/', views.TermsOfUseView.as_view(), name='termsOfUseView'),  # Vista para mostrar los terminos de uso
    path('reward/', views.RewardListView.as_view(), name='rewardListView'),  # Vista para listar todas las recompensas
    path('reward/<int:pk>/redeem/', views.RewardRedemptionView.as_view(), name='redeemRewardView'),  # Vista para reclamar una recompensa
    path('redemptions/<int:pk>', views.RedemptionListView.as_view(), name='redemptionListView'),  # Vista para listar todas las recompensas reclamadas
    path('how_it_works/', views.HowItWorkView.as_view(), name='howItWorkView'),  # Vista para la página de como usar la web
    path('accounts/register/', views.RegisterView.as_view(), name='register'),  # Vista para registro de usuarios
    path('match/confirm_result/<int:pk>/', views.MatchConfirmView.as_view(), name='matchConfirmView'),  # Vista para confirmar el resultado de una partida
    path('match/ready/<int:pk>/', views.MatchReadyView.as_view(), name='matchReadyView'),  # Vista para marcar el equipo como preparado
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
