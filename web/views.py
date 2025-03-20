from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.views.generic import ListView

from web.models import *


def index(request):
    return HttpResponse("¡Bienvenido a la página principal!")


class PlayerListView(ListView):
    model = Player
    template_name = 'web/player.html'
    context_object_name = 'player_list'

    def get_queryset(self):
        # Optimizamos la consulta con select_related y prefetch_related
        return Player.objects.select_related(
            'team'
        ).all()