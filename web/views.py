from datetime import timedelta, datetime

from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from web.forms import *
from django.urls import reverse
from django.shortcuts import redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, FormView, DetailView, CreateView, UpdateView
from rest_framework import generics

from .functions import record_match_result
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


class TeamCreateView(LoginRequiredMixin, CreateView):
    model = Team
    template_name = 'web/team_create.html'
    fields = ['name']

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
            player.save()

        # Redirigir al usuario a la vista de los equipos en el torneo
        return redirect('web:joinTeamListView', pk=self.tournament.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tournament'] = self.tournament
        return context

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

        # Verificar si el usuario es jugador en este partido
        user_is_player = match.team1.player_set.filter(user=self.request.user).exists() or \
                         match.team2.player_set.filter(user=self.request.user).exists()

        # Si el usuario es un jugador, agregar el botón para confirmar el resultado
        context['user_is_player'] = user_is_player

        return context

class MatchConfirmView(LoginRequiredMixin, View):
    """Vista para confirmar el resultado de un partido."""

    def dispatch(self, request, *args, **kwargs):
        # Obtener el partido que se va a confirmar
        self.match = get_object_or_404(Match, pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Procesar la confirmación del resultado del partido."""
        winner = request.POST.get('winner')
        match = get_object_or_404(Match, pk=self.kwargs['pk'])

        # Verificar si el usuario pertenece a uno de los equipos
        if request.user.player.team != match.team1 and request.user.player.team != match.team2:
            return HttpResponse('No estás en ninguno de los equipos de este partido', status=403)

        # Marcar la confirmación del equipo
        if request.user.player.team == match.team1:
            match.team1_confirmed = True
            match.team1_winner = (winner == 'team1')
        elif request.user.team == match.team2:
            match.team2_confirmed = True
            match.team2_winner = (winner == 'team2')

        match.save()

        # Comprobar si ambos equipos han confirmado el resultado
        if match.team1_confirmed and match.team2_confirmed:
            if match.team1_winner:
                match.winner = match.team1
                record_match_result(match, match.winner,)
            elif match.team2_winner:
                match.winner = match.team2
                record_match_result(match, match.winner,)

            match.save()
            return redirect('web:matchDetailView', pk=match.id)

        return redirect('web:matchDetailView', pk=match.id)

    def get_context_data(self, **kwargs):
        context = {
            'match': self.match,
        }
        return context

class MatchReadyView(LoginRequiredMixin, View):
    """Vista para confirmar que el equipo está listo para jugar."""

    def post(self, request, *args, **kwargs):
        # Obtener el partido
        match = get_object_or_404(Match, pk=self.kwargs['pk'])

        # Verificar que el usuario pertenece a uno de los equipos
        if request.user.team != match.team1 and request.user.team != match.team2:
            return HttpResponse('No estás en ninguno de los equipos de este partido', status=403)

        # Marcar el equipo como listo
        if request.user.team == match.team1:
            match.team1_ready = True
        elif request.user.team == match.team2:
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


