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
    pass


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

        # Guardamos el torneo
        tournament = form.save()

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
        return super().form_valid(form)