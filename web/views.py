from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from web.forms import *
from django.shortcuts import redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, FormView, DetailView, CreateView
from rest_framework import generics
from .serializers import TournamentSerializer
from web.models import *
from django.core.mail import send_mail
from django.conf import settings


# Create your views here.



class TournamentListAPI(generics.ListAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer

class PublicIndexView(TemplateView):
    template_name = 'web/public_index.html'

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
        context['ranking_list'] = Player.objects.order_by('-mmr')
        return context


class PlayerDetailView(LoginRequiredMixin, DetailView):
    model = Player
    template_name = 'web/player_detail.html'
    context_object_name = 'player'

class TournamentListView(LoginRequiredMixin, ListView):
    model = Tournament
    template_name = 'web/tournament_list.html'
    context_object_name = 'tournament_list'

    def get_queryset(self):
        return Tournament.objects.all()

class MyTournamentListView(LoginRequiredMixin, ListView):
    model = Tournament
    template_name = 'web/my_tournament_list.html'
    context_object_name = 'tournament_list'

    def get_queryset(self):
        return Tournament.objects.all().filter(pk=self.kwargs['pk'])

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

class PlayerProfileDetailView(LoginRequiredMixin, DetailView):
    model = Player
    template_name = 'web/player_profile_detail.html'
    context_object_name = 'player'

class RewardListView(LoginRequiredMixin, ListView):
    model = Reward
    template_name = 'web/reward.html'
    context_object_name = 'reward_list'

    def get_queryset(self):
        return Reward.objects.all()

class BecomePremiumView(LoginRequiredMixin, TemplateView):
    template_name = 'web/premium.html'

class HowItWorkView(LoginRequiredMixin, TemplateView):
    template_name = 'web/how_it_work.html'

class SupportView(LoginRequiredMixin, TemplateView):
    template_name = 'web/support.html'

class GameDetailView(LoginRequiredMixin, DetailView):
    model = Game
    template_name = 'web/game.html'
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
        Cuando el formulario es válido, guardamos el torneo y redirigimos a la página del juego
        relacionado.
        """
        # Asignar el campo `created_by` al usuario actual
        form.instance.created_by = self.request.user
        form.instance.prize_pool = 1000
        form.instance.game = self.kwargs['pk']
        # Guardamos el torneo
        tournament = form.save()

        # Enviar correo al usuario
        send_mail(
            subject='🎮 Has creado un nuevo torneo en ArenaGG',
            message=f'Hola {self.request.user.username},\n\nHas creado con éxito el torneo "{tournament.name}".\n\n¡Mucha suerte a todos los participantes!\n\n- El equipo de ArenaGG',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.request.user.email],
            fail_silently=False,
        )

        # Usamos `reverse` directamente para obtener la URL
        return redirect(reverse_lazy('web:gameDetailView', kwargs={'pk': tournament.game.pk}))

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