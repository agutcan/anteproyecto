from datetime import timedelta, datetime
from collections import defaultdict
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from django.db.models import Q
from web.forms import *
from django.urls import reverse
from django.shortcuts import redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, FormView, DetailView, CreateView, UpdateView
from rest_framework import generics

from .functions import record_match_result, create_match_log, update_players_stats, increase_player_renombre
from .serializers import *
from web.models import *
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseForbidden



# Create your views here.



class TournamentListAPI(generics.ListAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer

class PlayerStatsListAPI(generics.ListAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerStatsSerializer

class PublicIndexView(TemplateView):
    template_name = 'web/public_index.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('web:indexView')
        return super().dispatch(request, *args, **kwargs)

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'web/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['game_list'] = Game.objects.all()
        return context

class PrivacyPolicyView(TemplateView):
    template_name = 'web/privacy_policy.html'

class TermsOfUseView(TemplateView):
    template_name = 'web/terms_of_use.html'

class FaqView(TemplateView):
    template_name = 'web/faq.html'

class RankingView(LoginRequiredMixin, TemplateView):
    template_name = 'web/ranking.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ranking_list'] = Player.objects.order_by('-mmr').select_related('user')
        return context


class TournamentListView(LoginRequiredMixin, ListView):
    model = Tournament
    template_name = 'web/tournament_list.html'
    context_object_name = 'tournament_list'

    def get_queryset(self):
        queryset = Tournament.objects.all()

        # Filtrar por nombre de torneo
        search_term = self.request.GET.get('search', '')
        if search_term:
            queryset = queryset.filter(name__icontains=search_term)

        # Filtrar por juego
        game_filter = self.request.GET.get('game', '')
        if game_filter:
            queryset = queryset.filter(game__id=game_filter)  # Filtrar por ID del juego

        # Filtrar por estado
        status_filter = self.request.GET.get('status', '')
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        games = Game.objects.all()

        context['games'] = games
        return context



class MyTournamentListView(LoginRequiredMixin, ListView):
    model = Tournament
    template_name = 'web/my_tournament_list.html'
    context_object_name = 'tournament_list'

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        player = Player.objects.filter(user=user).first()

        if player and player.team:
            return Tournament.objects.filter(
                tournamentteam__team=player.team
            ).distinct()
        return Tournament.objects.none()


class GameListView(LoginRequiredMixin, ListView):
    model = Game
    template_name = 'web/game_list.html'
    context_object_name = 'game_list'

    def get_queryset(self):
        return Game.objects.all()

class TournamentDetailView(LoginRequiredMixin, DetailView):
    model = Tournament
    template_name = 'web/tournament_detail.html'
    context_object_name = 'tournament'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tournament = self.get_object()
        user = self.request.user

        # Por defecto asumimos que no está registrado
        is_registered = False

        if user.is_authenticated:
            try:
                player = Player.objects.get(user=user)
                is_registered = TournamentTeam.objects.filter(
                    tournament=tournament,
                    team__player=player
                ).exists()
            except Player.DoesNotExist:
                is_registered = False

        context['is_registered'] = is_registered
        return context

class PlayerProfileDetailView(LoginRequiredMixin, DetailView):
    model = Player
    template_name = 'web/player_profile_detail.html'
    context_object_name = 'player'

class PlayerUpdateView(LoginRequiredMixin, UpdateView):
    model = Player
    form_class = PlayerForm  # Tu formulario personalizado o ModelForm
    template_name = 'web/player_profile_update.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Player, user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['player'] = self.get_object()
        return context

    def get_success_url(self):
        return reverse('web:playerProfileDetailView', kwargs={'pk': self.object.pk})


class RewardListView(LoginRequiredMixin, ListView):
    model = Reward
    template_name = 'web/reward.html'
    context_object_name = 'reward_list'

    def get_queryset(self):
        return Reward.objects.all()

class JoinTeamListView(LoginRequiredMixin, ListView):
    model = TournamentTeam
    template_name = 'web/join_team.html'
    context_object_name = 'team_list'

    def get_queryset(self):
        tournament = get_object_or_404(Tournament, pk=self.kwargs['pk'])
        return TournamentTeam.objects.filter(tournament=tournament)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tournament = get_object_or_404(Tournament, pk=self.kwargs['pk'])

        tournament_teams = TournamentTeam.objects.filter(tournament=tournament)

        context['tournament'] = tournament
        context['team_list'] = tournament_teams
        return context

class PremiumView(LoginRequiredMixin, TemplateView):
    template_name = 'web/premium.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        player = Player.objects.get(user=self.request.user)
        context['player'] = player
        return context

class UpgradeToPremiumView(LoginRequiredMixin, View):
    """Convierte al usuario en Premium (gratis por tiempo limitado)."""
    def get(self, request, *args, **kwargs):
        player = Player.objects.get(user=request.user)
        player.role = Player.PREMIUM
        player.save()
        return redirect(reverse_lazy('web:premiumView'))

class HowItWorkView(LoginRequiredMixin, TemplateView):
    template_name = 'web/how_it_work.html'

class GameDetailView(LoginRequiredMixin, DetailView):
    model = Game
    template_name = 'web/game_detail.html'
    context_object_name = 'game'



class TournamentCreateView(LoginRequiredMixin, CreateView):
    """
    Vista para crear una nueva facción.

    Utiliza un formulario de creación (`FactionDefaultForm`) para que el usuario
    pueda crear una nueva facción.
    """

    model = Tournament  # Especifica el modelo relacionado
    form_class = TournamentForm  # Usamos el formulario `FactionDefaultForm`
    template_name = 'web/tournament_create.html'  # Especifica el template para renderizar la vista

    def form_valid(self, form):
        """
        Cuando el formulario es válido, guardamos el torneo.
        La validación de max_teams par ahora se hace en el modelo.
        """
        try:
            # Asignar campos automáticos
            form.instance.created_by = self.request.user
            form.instance.prize_pool = 1000  # Valor por defecto

            # El método save() automáticamente llama a full_clean()
            # que ejecuta las validaciones del modelo
            tournament = form.save()

            # Enviar correo de confirmación
            send_mail(
                subject='🎮 Torneo creado en ArenaGG',
                message=f'Hola {self.request.user.username},\n\nHas creado el torneo "{tournament.name}" para {tournament.max_teams} equipos.\n\nFecha: {tournament.start_date.strftime("%d/%m/%Y")}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[self.request.user.email],
                fail_silently=True,
            )

            return redirect('web:tournamentListView')

        except ValidationError as e:
            # Captura errores de validación del modelo y los muestra en el formulario
            for field, errors in e.message_dict.items():
                for error in errors:
                    form.add_error(field, error)
            return self.form_invalid(form)

        except Exception as e:
            # Para otros errores inesperados
            form.add_error(None, f"Error al crear torneo: {str(e)}")
            return self.form_invalid(form)


class TeamCreateInTournamentView(LoginRequiredMixin, CreateView):
    model = Team
    template_name = 'web/team_create_in_tournament.html'
    form_class = TeamForm

    def dispatch(self, request, *args, **kwargs):
        # Obtener el torneo al que se le va a asociar el equipo
        self.tournament = get_object_or_404(Tournament, pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Crear el equipo
        team = form.save()

        # Asociar el equipo con el torneo
        TournamentTeam.objects.create(tournament=self.tournament, team=team)

        # Asignar el jugador logueado al equipo recién creado
        player = Player.objects.filter(user=self.request.user).first()
        if player:
            player.team = team
            team.leader = player
            player.save()
            team.save()

        # Redirigir al usuario a la vista de los equipos en el torneo
        return redirect('web:joinTeamListView', pk=self.tournament.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tournament'] = self.tournament
        return context

class TeamCreateView(LoginRequiredMixin, CreateView):
    model = Team
    template_name = 'web/team_create.html'
    form_class = TeamForm

    def form_valid(self, form):
        # Crear el equipo
        team = form.save()

        # Asignar el jugador logueado al equipo recién creado
        player = Player.objects.filter(user=self.request.user).first()
        if player:
            player.team = team
            team.leader = player
            player.save()
            team.save()

        # Redirigir al usuario a la vista de los equipos en el torneo
        return redirect('web:playerTeamDetailView', pk=player.id)


class TeamDeleteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        # Obtener el equipo a eliminar
        team = get_object_or_404(Team, pk=kwargs['pk'])

        # Verificar si el jugador es el líder del equipo
        if team.leader.user != request.user:
            messages.error(request, "No tienes permiso para eliminar este equipo.")
            return redirect('web:playerTeamDetailView', pk=request.user.player.pk)

        # Verificar si el equipo está inscrito en algún torneo
        if TournamentTeam.objects.filter(team=team).exists():
            # Si está inscrito en algún torneo, no se puede eliminar
            messages.error(request, "No se puede eliminar el equipo porque está inscrito en un torneo.")
            return redirect('web:playerTeamDetailView', pk=request.user.player.pk)

        # Eliminar el equipo
        team.delete()

        # Redirigir a la vista del jugador después de la eliminación
        messages.success(request, "El equipo ha sido eliminado exitosamente.")
        return redirect('web:playerTeamDetailView', pk=request.user.player.pk)

class ToggleSearchingTeammatesView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        team = get_object_or_404(Team, pk=pk)
        player = Player.objects.get(user=request.user)

        if team.leader != player:
            messages.error(request, "No tienes permiso para modificar este equipo.")
            return redirect('web:playerTeamDetailView', pk=player.pk)

        # Solo aplicar restricciones si se está intentando ACTIVAR la búsqueda
        if not team.searching_teammates:
            # Verificar si participa en torneos en curso
            ongoing_tournaments = team.tournament_set.filter(status='Ongoing')
            if ongoing_tournaments.exists():
                messages.error(
                    request,
                    "No puedes activar la búsqueda de jugadores mientras el equipo esté participando en un torneo en curso."
                )
                return redirect('web:playerTeamDetailView', pk=player.pk)

            # Verificar si está lleno en torneos próximos
            upcoming_tournaments = team.tournament_set.filter(status='Upcoming')
            for tournament in upcoming_tournaments:
                if team.player_set.count() >= tournament.max_players_per_team:
                    messages.error(
                        request,
                        f"No puedes activar la búsqueda de jugadores porque el equipo ya está completo en el torneo '{tournament.name}'."
                    )
                    return redirect('web:playerTeamDetailView', pk=player.pk)

        # Alternar el estado
        team.searching_teammates = not team.searching_teammates
        team.save()

        if team.searching_teammates:
            messages.success(request, "La búsqueda de jugadores ha sido activada.")
        else:
            messages.success(request, "La búsqueda de jugadores ha sido desactivada.")

        return redirect('web:playerTeamDetailView', pk=player.pk)

class TeamJoinView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # Filtrar equipos que están buscando jugadores
        team_list = Team.objects.filter(searching_teammates=True)

        return render(request, 'web/team_join.html', {
            'teams': team_list
        })

    def post(self, request, *args, **kwargs):
        team_id = request.POST.get('team_id')
        team = get_object_or_404(Team, id=team_id)
        player = Player.objects.get(user=request.user)

        # Unir al jugador al equipo
        player.team = team
        player.save()

        return redirect('web:playerTeamDetailView', pk=player.pk)

class TeamKickView(LoginRequiredMixin, View):
    def post(self, request, team_id, player_id, *args, **kwargs):
        team = Team.objects.get(pk=team_id)
        player = Player.objects.get(pk=player_id)

        if player.team == team:
            # Desvincular al jugador del equipo
            player.team = None
            player.save()
            # Enviar correo de confirmación
            send_mail(
                subject='Has sido expulsado!!',
                message=(
                    f'Hola {player.user},\n\n'
                    'Se te ha expulsado de tu equipo.\n\n'
                    '¡Esperemos que este no sea un adios para siempre!\n\n'
                    '- El equipo de ArenaGG'
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[player.user.email],
                fail_silently=False,
            )
            messages.success(request, "Has expulsado al jugador del equipo correctamente.")
        else:
            messages.error(request, "El jugador que intentas expulsar no está en el equipo.")

        return redirect('web:playerTeamDetailView', pk=team.leader.pk)

class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        # Crear automáticamente un Gamer asociado al usuario
        Player.objects.create(user=user)
        login(self.request, user)

        # Enviar correo de confirmación
        send_mail(
            subject='✅ ¡Bienvenido a ArenaGG!',
            message=(
                f'Hola {user.username},\n\n'
                'Tu cuenta ha sido creada exitosamente. Ya puedes participar en torneos, crear equipos y mucho más.\n\n'
                '¡Nos alegra tenerte a bordo!\n\n'
                '- El equipo de ArenaGG'
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

        return super().form_valid(form)


class LeaveTournamentView(LoginRequiredMixin, TemplateView):
    template_name = 'web/leave_tournament_confirm.html'  # si quieres una página de confirmación

    def post(self, request, *args, **kwargs):
        tournament_id = self.kwargs['pk']
        tournament = get_object_or_404(Tournament, pk=tournament_id)
        player = get_object_or_404(Player, user=request.user)

        team = player.team
        if not team:
            messages.warning(request, "No estás en ningún equipo.")
            return redirect('web:tournamentDetailView', tournament.id)

        tt = TournamentTeam.objects.filter(tournament=tournament, team=team).first()
        if not tt:
            messages.warning(request, "Tu equipo no pertenece a este torneo.")
            return redirect('web:tournamentDetailView', tournament.id)

        # Quitar al jugador del equipo
        player.team = None
        player.save()

        # Si el equipo está vacío, eliminarlo junto con la relación
        if team.player_set.count() == 0:
            tt.delete()
            team.delete()
            messages.success(request, "Has abandonado el torneo y tu equipo ha sido eliminado.")
        else:
            messages.success(request, "Has abandonado el torneo.")

        return redirect('web:tournamentDetailView', tournament.id)


class MatchDetailView(LoginRequiredMixin, DetailView):
    model = Match
    template_name = 'web/match_detail.html'
    context_object_name = 'match'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        match = self.get_object()

        # Verificar si el usuario pertenece a alguno de los equipos
        is_team1_player = match.team1.player_set.filter(user=self.request.user).exists()
        is_team2_player = match.team2.player_set.filter(user=self.request.user).exists()

        print(f"Is user in team 1: {is_team1_player}")  # Depuración
        print(f"Is user in team 2: {is_team2_player}")  # Depuración

        context['user_is_player'] = is_team1_player or is_team2_player

        # Instanciar el formulario si el usuario pertenece a un equipo
        if is_team1_player or is_team2_player:
            form = MatchResultForm()

            # Actualizar los labels dinámicamente
            form.fields['team1_score'].label = f"Puntaje de {match.team1.name}"
            form.fields['team2_score'].label = f"Puntaje de {match.team2.name}"

            context['form'] = form

        if is_team1_player:
            context['team_ready'] = match.team1_ready
            context['team_confirmed'] = match.team1_confirmed
        elif is_team2_player:
            context['team_ready'] = match.team2_ready
            context['team_confirmed'] = match.team2_confirmed
        else:
            context['team_ready'] = False
            context['team_confirmed'] = False

        return context

class MatchConfirmView(LoginRequiredMixin, View):
    """Vista para confirmar el resultado de un partido."""

    def dispatch(self, request, *args, **kwargs):
        self.match = get_object_or_404(Match, pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        match = self.match
        form = MatchResultForm(request.POST)

        if not form.is_valid():
            return render(request, 'web/match_detail.html', {
                'form': form,
                'match': match
            })

        # Verificar si el usuario pertenece a uno de los equipos
        user_team = request.user.player.team
        if user_team != match.team1 and user_team != match.team2:
            return HttpResponse('No estás en ninguno de los equipos de este partido', status=403)

        winner = form.cleaned_data['winner']
        team1_score = form.cleaned_data['team1_score']
        team2_score = form.cleaned_data['team2_score']

        # Marcar la confirmación del equipo
        if user_team == match.team1:
            match.team1_confirmed = True
            match.team1_winner = (winner == 'team1')
            create_match_log(match, f"Equipo 1 ({match.team1.name}) ha confirmado el resultado.", team=match.team1)

        elif user_team == match.team2:
            match.team2_confirmed = True
            match.team2_winner = (winner == 'team2')
            create_match_log(match, f"Equipo 2 ({match.team2.name}) ha confirmado el resultado.", team=match.team2)

        # Verificar si ambos equipos han confirmado el resultado
        if match.team1_confirmed and match.team2_confirmed:
            # Comparar si ambos equipos están de acuerdo con el ganador
            if match.team1_winner != match.team2_winner:
                # Enviar un correo de notificación al soporte si los equipos no están de acuerdo
                send_mail(
                    'Inconsistencia en el resultado del partido',
                    f'El partido {match.id} tiene un desacuerdo entre los equipos sobre el ganador.\n\n'
                    f'Equipo 1 seleccionado como ganador: {match.team1_winner}\n'
                    f'Equipo 2 seleccionado como ganador: {match.team2_winner}',
                    settings.DEFAULT_FROM_EMAIL,  # Remitente
                    [settings.SUPPORT_EMAIL],  # Correo de soporte
                    fail_silently=False
                )
                # Agregar el mensaje de error al formulario
                messages.error(request, 'Los dos equipos no están de acuerdo sobre el ganador. El administrador ha sido notificado.')
                return render(request, 'web/match_detail.html', {
                    'form': form,
                    'match': match
                })

            # Verificar que el puntaje sea coherente con el ganador
            if winner == 'team1' and team1_score <= team2_score:
                send_mail(
                    'Inconsistencia en el puntaje del partido',
                    f'El equipo 1 no puede ganar con un puntaje inferior o igual al del equipo 2. Partido ID: {match.id}\n\n'
                    f'Puntaje del equipo 1: {team1_score}, Puntaje del equipo 2: {team2_score}',
                    settings.DEFAULT_FROM_EMAIL,  # Remitente
                    [settings.SUPPORT_EMAIL],  # Correo de soporte
                    fail_silently=False
                )
                messages.error(request, 'El equipo 1 no puede ganar con un puntaje inferior o igual al del equipo 2. El administrador ha sido notificado.')
                return render(request, 'web/match_detail.html', {
                    'form': form,
                    'match': match
                })

            elif winner == 'team2' and team2_score <= team1_score:
                send_mail(
                    'Inconsistencia en el puntaje del partido',
                    f'El equipo 2 no puede ganar con un puntaje inferior o igual al del equipo 1. Partido ID: {match.id}\n\n'
                    f'Puntaje del equipo 1: {team1_score}, Puntaje del equipo 2: {team2_score}',
                    settings.DEFAULT_FROM_EMAIL,  # Remitente
                    [settings.SUPPORT_EMAIL],  # Correo de soporte
                    fail_silently=False
                )
                messages.error(request, 'El equipo 2 no puede ganar con un puntaje inferior o igual al del equipo 1. El administrador ha sido notificado.')
                return render(request, 'web/match_detail.html', {
                    'form': form,
                    'match': match
                })

            # Si ambos equipos han confirmado y los resultados son coherentes
            if match.team1_winner:
                match.winner = match.team1
                update_players_stats(match.team1, is_winner=True)
                update_players_stats(match.team2)  # Los jugadores del equipo perdedor también se actualizan

            elif match.team2_winner:
                match.winner = match.team2
                update_players_stats(match.team2, is_winner=True)
                update_players_stats(match.team1)  # Los jugadores del equipo perdedor también se actualizan

            # Aumentar el renombre a todos los jugadores del partido
            for player in match.team1.player_set.all():
                increase_player_renombre(player, amount=5, reason="Participación en partido completado con éxito")

            for player in match.team2.player_set.all():
                increase_player_renombre(player, amount=5, reason="Participación en partido completado con éxito")


            # Llamar a la función `record_match_result` para guardar el resultado
            record_match_result(match, match.winner, team1_score, team2_score)
            create_match_log(match, "El partido ha sido completado. Ganador: " + match.winner.name)

        match.save()

        # Redirigir a la vista de detalles del partido
        return redirect('web:matchDetailView', pk=match.id)

    def get(self, request, *args, **kwargs):
        match = self.match
        form = MatchResultForm(initial={
            'team1_score': 1,  # Valor predeterminado para el puntaje de team1
            'team2_score': 1,  # Valor predeterminado para el puntaje de team2
        })

        return render(request, 'web/match_detail.html', {
            'form': form,
            'match': match
        })

class MatchReadyView(LoginRequiredMixin, View):
    """Vista para confirmar que el equipo está listo para jugar."""

    def post(self, request, *args, **kwargs):
        # Obtener el partido
        match = get_object_or_404(Match, pk=self.kwargs['pk'])

        # Verificar que el usuario pertenece a uno de los equipos
        if request.user.player.team != match.team1 and request.user.player.team != match.team2:
            return HttpResponse('No estás en ninguno de los equipos de este partido', status=403)

        # Marcar el equipo como listo
        if request.user.player.team == match.team1:
            match.team1_ready = True
        elif request.user.player.team == match.team2:
            match.team2_ready = True

        match.save()

        return redirect('web:matchDetailView', pk=match.id)


class SupportView(LoginRequiredMixin, FormView):
    template_name = 'web/support.html'
    form_class = SupportForm
    success_url = reverse_lazy('web:supportView')

    def form_valid(self, form):
        # Procesar los datos del formulario
        user_email = form.cleaned_data['email']
        subject = form.cleaned_data['subject']
        message_content = form.cleaned_data['message']
        username = self.request.user.username

        # Construir el mensaje
        message = f"""
        Mensaje de contacto de ArenaGG:

        Usuario: {username}
        Email: {user_email}
        Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

        Asunto: {subject}

        Mensaje:
        {message_content}
        """

        # Enviar el correo electrónico
        try:
            send_mail(
                subject=f"[Contacto ArenaGG] {subject}",
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.SUPPORT_EMAIL],
                fail_silently=False,
            )

            messages.success(
                self.request,
                '¡Mensaje enviado con éxito! '
                'Nuestro equipo te responderá a la brevedad.'
            )
        except Exception as e:
            messages.error(
                self.request,
                f'Ocurrió un error al enviar tu mensaje. '
                f'Por favor intenta nuevamente. Error: {str(e)}'
            )
            return self.form_invalid(form)

        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.user.is_authenticated:
            kwargs['initial'] = {'email': self.request.user.email}
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

class RewardRedemptionView(LoginRequiredMixin, View):
    def post(self, request, pk):
        reward = get_object_or_404(Reward, id=pk)
        player = request.user.player  # Asumes que cada user tiene un perfil Player

        if player.coins >= reward.coins_cost:
            # Restar las monedas y guardar
            player.coins -= reward.coins_cost
            player.save()
            reward.stock -= 1
            reward.save()
            if reward.stock == 0:
                send_mail(
                    subject='Recompensa acabada',
                    message=f'Se ha acabado el stock de la recompensa: {reward.name}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.DEFAULT_FROM_EMAIL],
                    fail_silently=True,
                )

            # Crear la redención
            Redemption.objects.create(user=request.user, reward=reward)

            messages.success(request, f'¡Has canjeado "{reward.name}" exitosamente!')
        else:
            messages.error(request, 'No tienes suficientes monedas para esta recompensa.')

        # Redirigir a la lista de recompensas
        return redirect('web:rewardListView')


class RedemptionListView(LoginRequiredMixin, ListView):
    model = Redemption
    template_name = 'web/redemption_list.html'
    context_object_name = 'redemption_list'

    def get_queryset(self):
        # Filtrar las redenciones del usuario actual
        return Redemption.objects.filter(user=self.request.user).order_by('-redeemed_at')


class TournamentLogsView(LoginRequiredMixin, DetailView):
    model = Tournament
    template_name = 'web/tournament_logs.html'
    context_object_name = 'tournament'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtener todos los logs de partidas relacionados con este torneo
        context['match_logs'] = MatchLog.objects.filter(match__tournament=self.object).select_related('match', 'player',
                                                                                                      'team').order_by(
            'match', 'created_at')

        return context

class PlayerTeamDetailView(LoginRequiredMixin, DetailView):
    model = Player
    template_name = 'web/player_team.html'
    context_object_name = 'player'

    def get_queryset(self):
        # Opcional: restringir a solo el jugador autenticado, si deseas
        return Player.objects.select_related('team')