from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from web.forms import *

# Create your views here.

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, FormView, DetailView

from web.models import *


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'web/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['game_list'] = Game.objects.all()  # Ordena por renombre y desempata por winrate
        return context

class RankingView(LoginRequiredMixin, TemplateView):
    template_name = 'web/ranking.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ranking_list'] = Player.objects.order_by('-mmr')
        return context

class PlayerListView(LoginRequiredMixin, ListView):
    model = Player
    template_name = 'web/player.html'
    context_object_name = 'player_list'

    def get_queryset(self):
        # Optimizamos la consulta con select_related y prefetch_related
        return Player.objects.select_related(
            'team'
        ).all()

class PlayerDetailView(LoginRequiredMixin, DetailView):
    model = Player
    template_name = 'web/player_detail.html'
    context_object_name = 'player'

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

class GameDetailView(LoginRequiredMixin, DetailView):
    model = Reward
    template_name = 'web/game.html'
    context_object_name = 'game_list'

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