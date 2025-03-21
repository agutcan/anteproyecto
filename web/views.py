from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from web.forms import *

# Create your views here.

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, FormView

from web.models import *


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'web/index.html'

class PlayerListView(LoginRequiredMixin, ListView):
    model = Player
    template_name = 'web/player.html'
    context_object_name = 'player_list'

    def get_queryset(self):
        # Optimizamos la consulta con select_related y prefetch_related
        return Player.objects.select_related(
            'team'
        ).all()

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