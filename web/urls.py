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
    path('start/premium/', views.PremiumView.as_view(), name='premiumView'),  # Vista de lista de jugadores
    path('start/premium/upgrade/', views.UpgradeToPremiumView.as_view(), name='upgradeToPremiumView'),
    path('start/support/', views.SupportView.as_view(), name='supportView'),  # Vista de lista de jugadores
    path('start/faq/', views.FaqView.as_view(), name='faqView'),  # Vista de lista de jugadores
    path('start/tournament/<int:pk>', views.TournamentDetailView.as_view(), name='tournamentDetailView'),  # Vista los detalles de un torneo
    path('start/tournament/match/<int:pk>', views.MatchDetailView.as_view(), name='matchDetailView'),  # Vista los detalles de un torneo
    path('start/tournament/', views.TournamentListView.as_view(), name='tournamentListView'),  # Vista los detalles de un torneo
    path('start/tournament/<int:pk>/join/', views.JoinTeamListView.as_view(), name='joinTeamListView'),
    path('start/tournament/<int:pk>/create_team/', views.TeamCreateInTournamentView.as_view(), name='teamCreateInTournamentView'),
    path('start/tournament/create_team/', views.TeamCreateView.as_view(), name='teamCreateView'),
    path('start/tournament/create/', views.TournamentCreateView.as_view(), name='tournamentCreateView'),
    path('start/tournament/leave/<int:pk>', views.LeaveTournamentView.as_view(), name='leaveTournamentView'),
    path('start/my_tournaments/<int:pk>', views.MyTournamentListView.as_view(), name='myTournamentListView'),  # Vista los detalles de un torneo
    path('start/my_team/<int:pk>', views.PlayerTeamDetailView.as_view(), name='playerTeamDetailView'),  # Vista los detalles de un torneo
    path('start/game/', views.GameListView.as_view(), name='gameListView'),  # Vista los detalles de un torneo
    path('team/<int:pk>/delete/', views.TeamDeleteView.as_view(), name='teamDeleteView'),
    path('start/tournament/create/', views.TournamentCreateView.as_view(), name='tournamentCreateView'),  # Vista los detalles de un torneo
    path('start/join_team/', views.TeamJoinView.as_view(), name='teamJoinView'),
    path('start/team/<int:pk>/search_players/', views.ToggleSearchingTeammatesView.as_view(), name='toggleSearchingTeammatesView'),

    path('start/profile/<int:pk>', views.PlayerProfileDetailView.as_view(), name='playerProfileDetailView'),  # Vista de lista de jugadores
    path('start/profile/update/<int:pk>/', views.PlayerUpdateView.as_view(), name='playerUpdateView'),  # Vista de lista de jugadores
    path('start/ranking/', views.RankingView.as_view(), name='rankingView'),  # Vista para mostrar un ranking de jugadores
    path('privacy_policy/', views.PrivacyPolicyView.as_view(), name='privacyPolicyView'),  # Vista para mostrar un ranking de jugadores
    path('temrs_of_use/', views.TermsOfUseView.as_view(), name='termsOfUseView'),  # Vista para mostrar un ranking de jugadores
    path('start/reward/', views.RewardListView.as_view(), name='rewardListView'),  # Vista para mostrar las recompensas
    path('start/reward/<int:pk>/redeem/', views.RewardRedemptionView.as_view(), name='redeemRewardView'),
    path('start/<int:pk>/redemptions/', views.RedemptionListView.as_view(), name='redemptionListView'),
    path('start/how_it_works/', views.HowItWorkView.as_view(), name='howItWorkView'),  # Vista para mostrar las recompensas
    path('start/game/<int:pk>', views.GameDetailView.as_view(), name='gameDetailView'),  # Vista de lista de juegos con sus torneos
    path('accounts/register/', views.RegisterView.as_view(), name='register'),  # Vista para registro de usuarios
    path('start/match/confirm_result/<int:pk>/', views.MatchConfirmView.as_view(), name='matchConfirmView'),
    path('start/match/ready/<int:pk>/', views.MatchReadyView.as_view(), name='matchReadyView'),
    path('start/tournament/<int:pk>/logs/', views.TournamentLogsView.as_view(), name='tournamentLogsView'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)