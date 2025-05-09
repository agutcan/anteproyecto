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
from django.db.models import Prefetch
from django.http import HttpResponseForbidden



# Create your views here.



class TournamentListAPI(generics.ListAPIView):
    """
    API endpoint que permite listar todos los torneos disponibles en el sistema.
    
    Proporciona una interfaz de solo lectura (GET) para acceder a la información
    básica de los torneos. Utiliza el serializer TournamentSerializer para definir
    la estructura de los datos devueltos.

    Atributos:
        queryset (QuerySet): Todos los objetos Tournament existentes
        serializer_class (Serializer): Clase que controla la serialización a JSON

    Métodos heredados:
        get: Maneja las solicitudes GET y devuelve la lista de jugadores serializados.
    """
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer

    def get_queryset(self):
            """
            Versión optimizada del queryset que incluye prefetch de relaciones comunes.
            
            Returns:
                QuerySet: Torneos con sus relaciones precargadas para mejor performance
            """
            return super().get_queryset().select_related('created_by').prefetch_related('teams', 'matches')
        
class PlayerStatsListAPI(generics.ListAPIView):
    """
    API endpoint que permite ver las estadísticas de todos los jugadores en formato JSON.
    
    Hereda de ListAPIView para proporcionar un endpoint de solo lectura (GET).
    Utiliza PlayerStatsSerializer para convertir los objetos Player a formato JSON.

    Atributos:
        queryset (QuerySet): Todos los objetos Player existentes en la base de datos.
        serializer_class (Serializer): Clase serializadora que define la representación JSON.

    Métodos heredados de ListAPIView:
        get: Maneja las solicitudes GET y devuelve la lista de jugadores serializados.
    """
    queryset = Player.objects.all()
    serializer_class = PlayerStatsSerializer

    def get_queryset(self):
        """
        Opcional: Sobrescribe el queryset base para agregar filtros o optimizaciones.
        
        Returns:
            QuerySet: Conjunto de jugadores potencialmente filtrado/optimizado.
        """
        return super().get_queryset().select_related('team')

class IndexView(LoginRequiredMixin, TemplateView):
    """
    Vista principal que muestra la página de inicio de la aplicación.
    
    Requiere que el usuario esté autenticado (heredando de LoginRequiredMixin)
    y muestra una lista de todos los juegos disponibles en el sistema.

    Atributos:
        template_name (str): Ruta al template HTML que renderiza la vista.

    Métodos:
        get_context_data(**kwargs): Añade la lista de juegos al contexto de renderizado.
    """
    template_name = 'web/index.html'

    def get_context_data(self, **kwargs):
        """
        Añade datos adicionales al contexto de la vista.

        Args:
            **kwargs: Argumentos clave adicionales.

        Returns:
            dict: Contexto enriquecido con la lista de todos los juegos.
        """
        context = super().get_context_data(**kwargs)
        context['game_list'] = Game.objects.all()
        return context

class PrivacyPolicyView(TemplateView):
    """
    Vista que muestra la política de privacidad del sitio web.
    
    Hereda de TemplateView para renderizar una plantilla HTML estática
    que contiene los términos y condiciones de privacidad de la plataforma.

    Atributos:
        template_name (str): Ruta a la plantilla que contiene el contenido HTML de la política de privacidad.
    """
    template_name = 'web/privacy_policy.html'

class TermsOfUseView(TemplateView):
    """
    Vista para mostrar los Términos y Condiciones de Uso de la plataforma.
    
    Renderiza una plantilla estática con el contenido legal de los términos de servicio.
    Ideal para cumplir con requisitos legales y de transparencia con los usuarios.

    Atributos:
        template_name (str): Ruta al template HTML que contiene los términos de uso.
    """
    template_name = 'web/terms_of_use.html'

class FaqView(TemplateView):
    """
    Vista para la página de Preguntas Frecuentes (FAQ) de la plataforma.
    
    Muestra contenido estático organizado por categorías de preguntas y respuestas.
    Permite agregar lógica dinámica para FAQs personalizadas según el perfil del usuario.

    Atributos:
        template_name (str): Ruta al template HTML ('web/templates/web/faq.html')
     """

    template_name = 'web/faq.html'

class RankingView(LoginRequiredMixin, TemplateView):
    """
    Vista que muestra el ranking de jugadores ordenado por MMR (Match Making Rating).
    
    Requiere autenticación (LoginRequiredMixin) y muestra una lista paginada de jugadores
    ordenados por su puntuación MMR de mayor a menor.

    Atributos:
        template_name (str): Ruta al template que muestra el ranking (web/ranking.html)
        
    Métodos:
        get_context_data: Añade al contexto la lista de jugadores ordenada y paginada
    """
    template_name = 'web/ranking.html'

    def get_context_data(self, **kwargs):
        """
        Prepara el contexto para el template incluyendo:
        - Lista de jugadores ordenada por MMR
        - Datos adicionales del usuario

        Returns:
            dict: Contexto con los jugadores y datos de paginación
        """
        context = super().get_context_data(**kwargs)
        context['ranking_list'] = Player.objects.order_by('-mmr').select_related('user')
        return context


class TournamentListView(LoginRequiredMixin, ListView):
    """
    Vista que muestra una lista paginada de torneos con capacidades de filtrado.
    
    Requiere autenticación (LoginRequiredMixin) y proporciona funcionalidad para filtrar
    torneos por nombre, juego asociado y estado del torneo.

    Atributos:
        model (Model): Modelo Tournament que representa los torneos
        template_name (str): Ruta al template que renderiza la lista (web/tournament_list.html)
        context_object_name (str): Nombre de la variable de contexto para la lista de torneos

    Métodos:
        get_queryset: Personaliza el QuerySet base añadiendo filtros según parámetros GET
        get_context_data: Añade al contexto la lista de juegos disponibles
    """
    model = Tournament
    template_name = 'web/tournament_list.html'
    context_object_name = 'tournament_list'

    def get_queryset(self):
        """
        Construye el QuerySet de torneos aplicando filtros opcionales basados en:
        - Búsqueda por nombre (parámetro GET 'search')
        - Filtro por juego (parámetro GET 'game')
        - Filtro por estado (parámetro GET 'status')

        Returns:
            QuerySet: Torneos filtrados según los parámetros recibidos
        """
        queryset = Tournament.objects.all()

        # Filtrar por nombre de torneo
        search_term = self.request.GET.get('search', '')
        if search_term:
            queryset = queryset.filter(name__icontains=search_term)

        # Filtrar por juego
        game_filter = self.request.GET.get('game', '')
        if game_filter:
            queryset = queryset.filter(game__id=game_filter)

        # Filtrar por estado
        status_filter = self.request.GET.get('status', '')
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        return queryset

    def get_context_data(self, **kwargs):
        """
        Extiende el contexto base añadiendo:
        - games: Lista de todos los juegos disponibles

        Args:
            **kwargs: Argumentos variables adicionales

        Returns:
            dict: Contexto enriquecido para el template
        """
        context = super().get_context_data(**kwargs)
        games = Game.objects.all()

        context['games'] = games
        return context


class MyTournamentListView(LoginRequiredMixin, ListView):
    """
    Vista que muestra la lista de torneos en los que participa el equipo del jugador actual.
    
    Requiere autenticación y muestra solo los torneos donde el equipo del jugador
    está registrado. Si el jugador no tiene equipo asociado, devuelve una lista vacía.

    Atributos:
        model (Model): Modelo Tournament utilizado para la consulta
        template_name (str): Ruta al template que renderiza la vista
        context_object_name (str): Nombre de la variable de contexto para la lista

    Métodos:
        get_queryset: Filtra los torneos donde participa el equipo del jugador
    """
    model = Tournament
    template_name = 'web/my_tournament_list.html'
    context_object_name = 'tournament_list'

    def get_queryset(self):
        """
        Obtiene los torneos asociados al equipo del jugador actual.
        
        Returns:
            QuerySet: Torneos donde participa el equipo del jugador o queryset vacío si:
                     - El usuario no existe
                     - No tiene jugador asociado
                     - El jugador no tiene equipo
        """
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        player = Player.objects.filter(user=user).first()

        if player and player.team:
            return Tournament.objects.filter(
                tournamentteam__team=player.team
            ).distinct()
        return Tournament.objects.none()


class GameListView(LoginRequiredMixin, ListView):
    """
    Vista que muestra una lista paginada de todos los juegos disponibles en la plataforma.
    
    Requiere que el usuario esté autenticado (LoginRequiredMixin) y muestra un listado
    completo de juegos registrados en el sistema.

    Atributos:
        model (Model): Modelo Game utilizado para obtener los datos
        template_name (str): Ruta al template que renderiza la lista (web/game_list.html)
        context_object_name (str): Nombre de la variable de contexto para la lista de juegos

    Métodos:
        get_queryset: Retorna todos los juegos sin filtros adicionales
    """
    model = Game
    template_name = 'web/game_list.html'
    context_object_name = 'game_list'

    def get_queryset(self):
        """
        Obtiene el QuerySet base de todos los juegos registrados en el sistema.
        
        Returns:
            QuerySet: Todos los objetos Game existentes en la base de datos
        """
        return Game.objects.all()

class TournamentDetailView(LoginRequiredMixin, DetailView):
    """
    Vista que muestra los detalles de un torneo específico.

    Requiere autenticación (LoginRequiredMixin) y muestra información detallada
    de un torneo individual, incluyendo el estado de registro del usuario actual.

    Atributos:
        model (Model): Modelo Tournament que contiene los datos del torneo
        template_name (str): Ruta al template que renderiza la vista (web/tournament_detail.html)
        context_object_name (str): Nombre de la variable que contendrá el objeto Tournament en el contexto del template

    Métodos heredados de DetailView:
        get_object: Obtiene el objeto Tournament basado en los parámetros de la URL
        get_context_data: Proporciona el contexto para renderizar el template
    """
    model = Tournament
    template_name = 'web/tournament_detail.html'
    context_object_name = 'tournament'

    def get_context_data(self, **kwargs):
        """
        Extiende el contexto base con información sobre si el usuario actual
        está registrado en el torneo.

        Returns:
            dict: Contexto que incluye:
                - is_registered: Booleano indicando si el usuario está registrado en el torneo
                - player: Objeto player con los datos del jugador
                - tournament_teams: Lista de objetos tournamentTeams con los datos de los equipos que participan en el torneo
        """
        context = super().get_context_data(**kwargs)
        tournament = context['tournament']
        user = self.request.user

        is_registered = False
        player = None

        if user.is_authenticated:
            try:
                player = Player.objects.select_related('team').get(user=user)
                is_registered = TournamentTeam.objects.filter(
                    tournament=tournament,
                    team__player=player
                ).exists()
            except Player.DoesNotExist:
                is_registered = False

        # Pre-cargar equipos del torneo con sus jugadores y usuarios
        tournament_teams = TournamentTeam.objects.filter(tournament=tournament).select_related(
            'team'
        ).prefetch_related(
        Prefetch('team__player_set', queryset=Player.objects.select_related('user'))
    )

        context['is_registered'] = is_registered
        context['player'] = player
        context['tournament_teams'] = tournament_teams

        return context

class PlayerProfileDetailView(LoginRequiredMixin, DetailView):
    """
    Vista que muestra el perfil detallado de un jugador específico.
    
    Requiere que el usuario esté autenticado (LoginRequiredMixin) para acceder
    a la información del perfil. Muestra los datos del jugador obtenidos a través
    del modelo Player.

    Atributos:
        model (Model): Modelo Player que contiene los datos del jugador
        template_name (str): Ruta al template que renderiza la vista
                           (web/player_profile_detail.html)
        context_object_name (str): Nombre de la variable que contendrá el objeto
                                 Player en el contexto del template

    Métodos heredados de DetailView:
        get_object: Obtiene el objeto Player basado en los parámetros de la URL
        get_context_data: Proporciona el contexto para renderizar el template
    """
    model = Player
    template_name = 'web/player_profile_detail.html'
    context_object_name = 'player'

class PlayerUpdateView(LoginRequiredMixin, UpdateView):
    """
    Vista para actualizar el perfil de un jugador.

    Requiere autenticación (LoginRequiredMixin) y permite editar
    los datos del perfil del jugador utilizando un formulario personalizado.

    Atributos:
        model (Model): Modelo Player que representa al jugador
        form_class (Form): Formulario personalizado para edición del perfil
        template_name (str): Ruta al template del formulario de edición

    Métodos:
        get_context_data: Añade el objeto Player al contexto
        get_success_url: Define la URL de redirección tras actualización exitosa
    """
    model = Player
    form_class = PlayerForm
    template_name = 'web/player_profile_update.html'

    def get_context_data(self, **kwargs):
        """
        Añade el objeto Player del usuario actual al contexto.

        Args:
            **kwargs: Argumentos clave adicionales

        Returns:
            dict: Contexto enriquecido con el objeto Player
        """
        context = super().get_context_data(**kwargs)
        context['player'] = Player.objects.get(user=self.request.user)
        return context

    def get_success_url(self):
        """
        Obtiene la URL de redirección después de una actualización exitosa.

        Returns:
            str: URL para redirigir al detalle del perfil del jugador
        """
        return reverse('web:playerProfileDetailView', kwargs={'pk': self.kwargs['pk']})


class RewardListView(LoginRequiredMixin, ListView):
    """
    Vista que muestra un listado de todas las recompensas disponibles.

    Requiere autenticación (LoginRequiredMixin) y muestra una lista paginada
    de objetos Reward. Utiliza el template 'web/reward.html' para renderizar
    la vista.

    Atributos:
        model (Model): Modelo Reward utilizado para obtener los datos
        template_name (str): Ruta al template que renderiza la vista
        context_object_name (str): Nombre de la variable de contexto para la lista

    Métodos heredados de ListView:
        get_queryset: Retorna todos los objetos Reward sin filtros
    """
    model = Reward
    template_name = 'web/reward.html'
    context_object_name = 'reward_list'

    def get_queryset(self):
        """
        Obtiene el queryset base de todas las recompensas disponibles.

        Returns:
            QuerySet: Todos los objetos Reward existentes en la base de datos
        """
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

        tournament_teams = TournamentTeam.objects.filter(
            tournament=tournament,
            team__searching_teammates=True
        )

        context['tournament'] = tournament
        context['team_list'] = tournament_teams
        return context

class PremiumView(LoginRequiredMixin, TemplateView):
    """
    Vista que muestra la página de membresía Premium del jugador.

    Requiere autenticación (LoginRequiredMixin) y muestra información
    relacionada con la suscripción Premium del jugador actual.

    Atributos:
        template_name (str): Ruta al template que renderiza la vista (web/premium.html)

    Métodos:
        get_context_data: Añade al contexto el objeto Player del usuario actual
    """
    template_name = 'web/premium.html'

    def get_context_data(self, **kwargs):
        """
        Obtiene y añade al contexto el perfil del jugador actual.

        Returns:
            dict: Contexto con el objeto Player del usuario autenticado
        """
        context = super().get_context_data(**kwargs)
        context['player'] = Player.objects.get(user=self.request.user)
        return context

class UpgradeToPremiumView(LoginRequiredMixin, View):
    """
    Vista que actualiza el rol del jugador a Premium de forma gratuita.
    
    Requiere autenticación (LoginRequiredMixin) y realiza la conversión
    del rol del jugador a Premium cuando se accede a la vista mediante GET.
    Redirige a la página de Premium después de la actualización.

    Métodos:
        get: Realiza la actualización del rol y redirecciona
    """
    def get(self, request, *args, **kwargs):
        """
        Actualiza el rol del jugador a Premium y redirige.
        
        Returns:
            HttpResponseRedirect: Redirección a la vista premiumView
        """
        player = Player.objects.get(user=request.user)
        player.role = Player.PREMIUM
        player.save()
        return redirect(reverse_lazy('web:premiumView'))

class HowItWorkView(LoginRequiredMixin, TemplateView):
    """
    Vista que muestra la página de "Cómo funciona" de la plataforma.
    
    Requiere autenticación (LoginRequiredMixin) y renderiza una plantilla estática
    con información sobre el funcionamiento de la plataforma.

    Atributos:
        template_name (str): Ruta al template que contiene la explicación
    """
    template_name = 'web/how_it_work.html'

class GameDetailView(LoginRequiredMixin, DetailView):
    """
    Vista que muestra los detalles de un juego específico.

    Requiere autenticación (LoginRequiredMixin) y muestra información detallada
    de un juego individual, incluyendo sus características y torneos asociados.

    Atributos:
        model (Model): Modelo Game que representa los juegos
        template_name (str): Ruta al template de detalle (web/game_detail.html)
        context_object_name (str): Nombre de la variable de contexto para el objeto Game

    Métodos heredados de DetailView:
        get_object: Obtiene el objeto Game basado en los parámetros de la URL
        get_context_data: Proporciona el contexto para renderizar el template
    """
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
    """
    Vista para crear un nuevo equipo dentro de un torneo específico.

    Requiere autenticación (LoginRequiredMixin) y permite a un usuario crear
    un equipo que será automáticamente asociado al torneo especificado.

    Atributos:
        model (Model): Modelo Team utilizado para la creación
        template_name (str): Ruta al template del formulario de creación
        form_class (Form): Clase del formulario para crear equipos

    Métodos:
        dispatch: Obtiene el torneo asociado antes de procesar la solicitud
        form_valid: Procesa el formulario válido creando las relaciones necesarias
        get_context_data: Añade el torneo al contexto del template
    """
    model = Team
    template_name = 'web/team_create_in_tournament.html'
    form_class = TeamForm

    def dispatch(self, request, *args, **kwargs):
        """
        Prepara la vista obteniendo el torneo asociado antes de procesar la solicitud.

        Args:
            request: Objeto HttpRequest
            *args: Argumentos variables
            **kwargs: Argumentos clave variables

        Returns:
            HttpResponse: Respuesta del método dispatch de la superclase
        """
        self.tournament = get_object_or_404(Tournament, pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """
        Procesa un formulario válido realizando:
        1. Creación del equipo
        2. Asociación con el torneo
        3. Asignación del jugador como miembro y líder
        4. Redirección a la vista de equipos del torneo

        Args:
            form (Form): Formulario de creación de equipo validado

        Returns:
            HttpResponseRedirect: Redirección a la vista de equipos del torneo
        """
        team = form.save()
        TournamentTeam.objects.create(tournament=self.tournament, team=team)
        
        player = Player.objects.filter(user=self.request.user).first()
        if player:
            player.team = team
            team.leader = player
            if self.tournament.max_player_per_team > 1:
                team.searching_teammates = True
            player.save()
            team.save()

        return redirect('web:tournamentDetailView', pk=self.tournament.pk)

    def get_context_data(self, **kwargs):
        """
        Añade el torneo al contexto del template.

        Args:
            **kwargs: Argumentos clave adicionales

        Returns:
            dict: Contexto enriquecido con el objeto Tournament
        """
        context = super().get_context_data(**kwargs)
        context['tournament'] = self.tournament
        return context

class TeamCreateView(LoginRequiredMixin, CreateView):
    """
    Vista para la creación de un nuevo equipo.

    Requiere autenticación (LoginRequiredMixin) y permite a un usuario crear
    un nuevo equipo, asignándose automáticamente como miembro y líder del mismo.

    Atributos:
        model (Model): Modelo Team utilizado para la creación
        template_name (str): Ruta al template del formulario de creación
        form_class (Form): Clase del formulario para crear equipos

    Métodos:
        form_valid: Procesa el formulario válido creando el equipo y asignando al usuario
    """
    model = Team
    template_name = 'web/team_create.html'
    form_class = TeamForm

    def form_valid(self, form):
        """
        Procesa un formulario válido realizando:
        1. Creación del equipo
        2. Asignación del jugador como miembro y líder
        3. Redirección a la vista de detalle del equipo

        Args:
            form (Form): Formulario de creación de equipo validado

        Returns:
            HttpResponseRedirect: Redirección a la vista de detalle del equipo del jugador
        """
        team = form.save()
        player = Player.objects.filter(user=self.request.user).first()
        if player:
            player.team = team
            team.leader = player
            player.save()
            team.save()

        return redirect('web:playerTeamDetailView', pk=player.id)


class TeamDeleteView(LoginRequiredMixin, View):
    """
    Vista para eliminar un equipo existente.

    Requiere autenticación (LoginRequiredMixin) y verifica que el usuario sea el líder
    del equipo y que el equipo no esté registrado en ningún torneo antes de permitir
    su eliminación.

    Métodos:
        post: Maneja la solicitud de eliminación con las validaciones correspondientes
    """
    def post(self, request, *args, **kwargs):
        """
        Procesa la solicitud de eliminación de equipo realizando:
        1. Verificación de permisos (solo el líder puede eliminar)
        2. Verificación de participación en torneos
        3. Eliminación del equipo si se cumplen las condiciones
        4. Redirección con mensajes de retroalimentación

        Args:
            request: Objeto HttpRequest
            *args: Argumentos variables
            **kwargs: Argumentos clave variables (incluye 'pk' del equipo)

        Returns:
            HttpResponseRedirect: Redirección a la vista de detalle del jugador
        """
        team = get_object_or_404(Team, pk=kwargs['pk'])

        if team.leader.user != request.user:
            messages.error(request, "No tienes permiso para eliminar este equipo.")
            return redirect('web:playerTeamDetailView', pk=request.user.player.pk)

        if TournamentTeam.objects.filter(team=team).exists():
            messages.error(request, "No se puede eliminar el equipo porque está inscrito en un torneo.")
            return redirect('web:playerTeamDetailView', pk=request.user.player.pk)

        team.delete()
        messages.success(request, "El equipo ha sido eliminado exitosamente.")
        return redirect('web:playerTeamDetailView', pk=request.user.player.pk)

class ToggleSearchingTeammatesView(LoginRequiredMixin, View):
    """
    Vista para activar/desactivar la búsqueda de compañeros de equipo.

    Requiere autenticación y permisos de líder del equipo para modificar
    el estado de búsqueda de jugadores. Incluye validaciones para evitar
    cambios no permitidos durante torneos activos o cuando el equipo está lleno.

    Métodos:
        post: Maneja la solicitud de cambio de estado con todas las validaciones
    """
    def post(self, request, pk, *args, **kwargs):
        """
        Procesa la solicitud de cambio de estado de búsqueda realizando:
        1. Verificación de permisos (solo el líder puede modificar)
        2. Validación de participación en torneos en curso
        3. Verificación de capacidad en torneos próximos
        4. Cambio de estado si se cumplen las condiciones
        5. Redirección con mensajes de retroalimentación

        Args:
            request: Objeto HttpRequest
            pk: ID del equipo a modificar
            *args: Argumentos variables
            **kwargs: Argumentos clave variables

        Returns:
            HttpResponseRedirect: Redirección a la vista de detalle del equipo
        """
        team = get_object_or_404(Team, pk=pk)
        player = Player.objects.get(user=request.user)

        if team.leader != player:
            messages.error(request, "No tienes permiso para modificar este equipo.")
            return redirect('web:playerTeamDetailView', pk=player.pk)

        if not team.searching_teammates:
            ongoing_tournaments = team.tournament_set.filter(status='Ongoing')
            if ongoing_tournaments.exists():
                messages.error(
                    request,
                    "No puedes activar la búsqueda de jugadores mientras el equipo esté participando en un torneo en curso."
                )
                return redirect('web:playerTeamDetailView', pk=player.pk)

            upcoming_tournaments = team.tournament_set.filter(status='Upcoming')
            for tournament in upcoming_tournaments:
                if team.player_set.count() >= tournament.max_players_per_team:
                    messages.error(
                        request,
                        f"No puedes activar la búsqueda de jugadores porque el equipo ya está completo en el torneo '{tournament.name}'."
                    )
                    return redirect('web:playerTeamDetailView', pk=player.pk)

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

        upcoming_tournaments = team.tournament_set.filter(status='Upcoming')
        for tournament in upcoming_tournaments:
            if team.player_set.count() >= tournament.max_players_per_team:
                messages.error(
                    request,
                    f"No puedes activar la búsqueda de jugadores porque el equipo ya está completo en el torneo '{tournament.name}'."
                )
                return redirect('web:playerTeamDetailView', pk=player.pk)

        # Unir al jugador al equipo
        player.team = team
        player.save()

        return redirect('web:playerTeamDetailView', pk=player.pk)

class TeamKickView(LoginRequiredMixin, View):
    def post(self, request, team_id, player_id, *args, **kwargs):
        team = Team.objects.get(pk=team_id)
        player = Player.objects.get(pk=player_id)

        if player.team == team or TournamentTeam.objects.filter(team=team).exists():
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
            messages.error(request, "El jugador que intentas expulsar no está en el equipo o el equipo ya está inscrito en algún torneo.")

        return redirect('web:playerTeamDetailView', pk=team.leader.pk)

class RegisterView(FormView):
    """
    Vista de registro de nuevos usuarios en la plataforma.

    Maneja el proceso de creación de cuentas mediante un formulario personalizado,
    creando automáticamente un perfil de jugador asociado y enviando un correo
    de confirmación al nuevo usuario registrado.

    Atributos:
        template_name (str): Ruta al template del formulario de registro
        form_class (Form): Clase del formulario personalizado para registro
        success_url (str): URL a la que redirigir tras registro exitoso

    Métodos:
        form_valid: Procesa el formulario válido, crea usuario y perfil asociado
    """
    template_name = 'registration/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        """
        Procesa un formulario de registro válido realizando:
        1. Creación del usuario
        2. Creación del perfil de jugador asociado
        3. Autenticación automática
        4. Envío de email de bienvenida

        Args:
            form (Form): Formulario de registro validado

        Returns:
            HttpResponseRedirect: Redirección a success_url
        """
        user = form.save()
        Player.objects.create(user=user)
        login(self.request, user)
        
        send_mail(
            subject='✅ ¡Bienvenido a ArenaGG!',
            message=(
                f'Hola {user.username},\n\n'
                'Tu cuenta ha sido creada exitosamente.\n\n'
                '- El equipo de ArenaGG'
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

        return super().form_valid(form)


class LeaveTournamentView(LoginRequiredMixin, TemplateView):
    """
    Vista para que un jugador abandone un torneo.

    Requiere autenticación y muestra una página de confirmación antes
    de procesar la solicitud de abandono del torneo.

    Atributos:
        template_name (str): Ruta al template de confirmación

    Métodos:
        post: Procesa la solicitud de abandono del torneo
    """
    template_name = 'web/leave_tournament_confirm.html'
    template_name = 'web/leave_tournament_confirm.html'  # si quieres una página de confirmación

    def post(self, request, *args, **kwargs):
        """
        Procesa la solicitud POST para abandonar un torneo:
        1. Verifica que el jugador pertenezca a un equipo
        2. Verifica que el equipo esté registrado en el torneo
        3. Verifica que el jugador sea el líder del equipo
        4. Elimina al equipo del torneo si se cumplen las condiciones

        Args:
            request: Objeto HttpRequest
            *args: Argumentos variables
            **kwargs: Argumentos clave variables (contiene 'pk' del torneo)

        Returns:
            HttpResponseRedirect: Redirección a la vista de detalle del torneo
        """
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

        if player != team.leader:
            messages.warning(request, "No eres el líder de tu equipo, no puedes realizar esta acción.")
            return redirect('web:tournamentDetailView', tournament.id)

        # Quitar al jugador del equipo
        tt.delete()
        messages.success(request, "Has abandonado el torneo.")

        return redirect('web:tournamentDetailView', tournament.id)

class MatchDetailView(LoginRequiredMixin, DetailView):
    """
    Vista que muestra los detalles de un partido específico, incluyendo información
    relevante para los jugadores participantes.

    Requiere autenticación (LoginRequiredMixin) y muestra los datos de un partido
    individual, con funcionalidad especial para los jugadores de los equipos
    involucrados.

    Atributos:
        model (Model): Modelo Match que contiene los datos del partido
        template_name (str): Ruta al template que renderiza la vista (web/match_detail.html)
        context_object_name (str): Nombre de la variable que contendrá el objeto Match
                                en el contexto del template

    Métodos heredados de DetailView:
        get_object: Obtiene el objeto Match basado en los parámetros de la URL
        get_context_data: Proporciona el contexto para renderizar el template
    """
    model = Match
    template_name = 'web/match_detail.html'
    context_object_name = 'match'

    def get_context_data(self, **kwargs):
        """
        Extiende el contexto base con información adicional sobre la participación
        del usuario actual en el partido.

        Returns:
            dict: Contexto que incluye:
                - user_is_player: Booleano indicando si el usuario es jugador de alguno de los equipos
                - form: Formulario para reportar resultados (solo para jugadores participantes)
                - team_ready: Estado de preparación del equipo del usuario
                - team_confirmed: Estado de confirmación del equipo del usuario
        """
        context = super().get_context_data(**kwargs)
        match = self.get_object()

        is_team1_player = match.team1.player_set.filter(user=self.request.user).exists()
        is_team2_player = match.team2.player_set.filter(user=self.request.user).exists()

        context['user_is_player'] = is_team1_player or is_team2_player

        if is_team1_player or is_team2_player:
            form = MatchResultForm()
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
    """
    Vista para confirmar el resultado de un partido.

    Maneja tanto la visualización del formulario de confirmación (GET)
    como el procesamiento de los resultados confirmados (POST). Incluye
    validaciones para asegurar la integridad de los resultados reportados.

    Métodos:
        dispatch: Obtiene el partido antes de procesar cualquier solicitud
        get: Muestra el formulario de confirmación de resultados
        post: Procesa la confirmación del resultado con todas las validaciones
    """
    def dispatch(self, request, *args, **kwargs):
        """
        Prepara la vista obteniendo el partido asociado.

        Args:
            request: Objeto HttpRequest
            *args: Argumentos variables
            **kwargs: Argumentos clave variables

        Returns:
            HttpResponse: Respuesta del método dispatch de la superclase
        """
        self.match = get_object_or_404(Match, pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Procesa la confirmación del resultado del partido realizando:
        1. Validación del formulario
        2. Verificación de pertenencia al equipo
        3. Registro de confirmación por equipo
        4. Validación de consistencia entre confirmaciones
        5. Actualización de estadísticas y registro final

        Args:
            request: Objeto HttpRequest con los datos del formulario
            *args: Argumentos variables
            **kwargs: Argumentos clave variables

        Returns:
            HttpResponseRedirect: Redirección a la vista de detalle del partido
        """
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
        """
        Muestra el formulario de confirmación de resultados.

        Args:
            request: Objeto HttpRequest
            *args: Argumentos variables
            **kwargs: Argumentos clave variables

        Returns:
            HttpResponse: Renderizado del template con el formulario
        """
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
    """
    Vista para marcar un equipo como listo para un partido.

    Requiere autenticación y permite a los jugadores confirmar que su equipo
    está preparado para comenzar el partido.

    Métodos:
        post: Procesa la confirmación de preparación del equipo
    """

    def post(self, request, *args, **kwargs):
        """
        Procesa la solicitud POST para marcar un equipo como listo:
        1. Obtiene el partido correspondiente
        2. Verifica que el usuario pertenezca a uno de los equipos
        3. Marca el equipo correspondiente como listo
        4. Guarda los cambios y redirige al detalle del partido

        Args:
            request: Objeto HttpRequest
            *args: Argumentos variables
            **kwargs: Argumentos clave variables (contiene 'pk' del partido)

        Returns:
            HttpResponseRedirect: Redirección a la vista de detalle del partido
            HttpResponse: Error 403 si el usuario no pertenece a ningún equipo del partido
        """
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
    """
    Vista para el formulario de contacto con soporte técnico.

    Requiere autenticación y permite a los usuarios enviar mensajes
    al equipo de soporte de la plataforma.

    Atributos:
        template_name (str): Ruta al template del formulario
        form_class (Form): Clase del formulario de contacto
        success_url (str): URL a redirigir tras envío exitoso

    Métodos:
        form_valid: Procesa el formulario válido y envía el correo
        get_form_kwargs: Personaliza los argumentos del formulario
        get_context_data: Proporciona contexto adicional al template
    """
    template_name = 'web/support.html'
    form_class = SupportForm
    success_url = reverse_lazy('web:supportView')

    def form_valid(self, form):
        """
        Procesa un formulario válido:
        1. Obtiene los datos del formulario
        2. Construye el mensaje de contacto
        3. Envía el correo electrónico al soporte
        4. Muestra mensajes de éxito/error al usuario

        Args:
            form (Form): Formulario validado

        Returns:
            HttpResponse: Redirección a success_url o respuesta de error
        """
        
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
        """
        Personaliza los argumentos del formulario:
        - Añade el email del usuario autenticado como valor inicial

        Returns:
            dict: Argumentos para instanciar el formulario
        """
        kwargs = super().get_form_kwargs()
        if self.request.user.is_authenticated:
            kwargs['initial'] = {'email': self.request.user.email}
        return kwargs

    def get_context_data(self, **kwargs):
        """
        Proporciona contexto adicional al template:
        - Añade el formulario al contexto

        Args:
            **kwargs: Argumentos clave variables

        Returns:
            dict: Contexto para renderizar el template
        """
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

class RewardRedemptionView(LoginRequiredMixin, View):
    """
    Vista para canjear recompensas por monedas del jugador.

    Requiere autenticación y permite a los jugadores canjear sus monedas
    por recompensas disponibles, verificando stock y fondos suficientes.

    Métodos:
        post: Procesa el canje de la recompensa
    """
    def post(self, request, pk):
        """
        Procesa la solicitud POST para canjear una recompensa:
        1. Verifica que la recompensa exista
        2. Comprueba que el jugador tenga monedas suficientes
        3. Actualiza saldos y stock
        4. Registra la transacción
        5. Notifica por email si el stock llega a cero
        6. Muestra mensajes de éxito/error al usuario

        Args:
            request: Objeto HttpRequest
            pk: ID de la recompensa a canjear

        Returns:
            HttpResponseRedirect: Redirección a la lista de recompensas
        """
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
    """
    Vista que muestra el historial de recompensas canjeadas por el usuario.

    Requiere autenticación y muestra solo las redenciones del usuario actual,
    ordenadas por fecha de canje descendente.

    Atributos:
        model (Model): Modelo Redemption que contiene los canjes
        template_name (str): Ruta al template que muestra la lista
        context_object_name (str): Nombre de la variable de contexto para la lista

    Métodos:
        get_queryset: Filtra y ordena las redenciones del usuario
    """
    model = Redemption
    template_name = 'web/redemption_list.html'
    context_object_name = 'redemption_list'

    def get_queryset(self):
        """
        Obtiene el queryset filtrado por el usuario actual y ordenado por fecha.

        Returns:
            QuerySet: Redenciones del usuario ordenadas por fecha descendente
        """
        # Filtrar las redenciones del usuario actual
        return Redemption.objects.filter(user=self.request.user).order_by('-redeemed_at')


class TournamentLogsView(LoginRequiredMixin, DetailView):
     """
    Vista que muestra los registros de actividad (logs) de un torneo específico.

    Requiere autenticación y muestra los registros de partidas asociadas
    al torneo seleccionado, incluyendo información detallada de cada evento.

    Atributos:
        model (Model): Modelo Tournament que contiene los datos del torneo
        template_name (str): Ruta al template que muestra los logs
        context_object_name (str): Nombre de la variable de contexto para el torneo

    Métodos:
        get_context_data: Añade los logs de partidas al contexto de la vista
    """
    model = Tournament
    template_name = 'web/tournament_logs.html'
    context_object_name = 'tournament'

    def get_context_data(self, **kwargs):
        """
        Extiende el contexto base con los logs de partidas del torneo:
        1. Obtiene todos los logs relacionados con partidas del torneo
        2. Incluye relaciones con partidos, jugadores y equipos
        3. Ordena por partido y fecha de creación

        Args:
            **kwargs: Argumentos clave variables

        Returns:
            dict: Contexto enriquecido con los logs de partidas
        """
        context = super().get_context_data(**kwargs)

        # Obtener todos los logs de partidas relacionados con este torneo
        context['match_logs'] = MatchLog.objects.filter(match__tournament=self.object).select_related('match', 'player',
                                                                                                      'team').order_by(
            'match', 'created_at')

        return context

class PlayerTeamDetailView(LoginRequiredMixin, DetailView):
    """
    Vista que muestra los detalles del equipo de un jugador.

    Requiere autenticación y muestra información sobre el equipo
    al que pertenece el jugador, incluyendo sus miembros y detalles.

    Atributos:
        model (Model): Modelo Player que contiene los datos del jugador
        template_name (str): Ruta al template que muestra la información del equipo
        context_object_name (str): Nombre de la variable de contexto para el jugador

    Métodos:
        get_queryset: Optimiza la consulta incluyendo la relación con el equipo
    """
    model = Player
    template_name = 'web/player_team.html'
    context_object_name = 'player'

    def get_queryset(self):
         """
        Obtiene el queryset del jugador incluyendo la relación con su equipo.

        Returns:
            QuerySet: Jugadores con su relación de equipo precargada
        """
        # Opcional: restringir a solo el jugador autenticado, si deseas
        return Player.objects.select_related('team')

class TeamInscribeInTournamentView(LoginRequiredMixin, View):
    """
    Vista para inscribir un equipo en un torneo específico.

    Requiere autenticación y verifica múltiples condiciones antes de permitir
    la inscripción de un equipo en un torneo.

    Métodos:
        post: Procesa la solicitud de inscripción con todas las validaciones necesarias
    """
    def post(self, request, tournament_id, team_id):
        """
        Procesa la solicitud POST para inscribir un equipo en un torneo realizando:
        1. Verificación de pertenencia al equipo
        2. Verificación de liderazgo del equipo
        3. Validación de inscripción previa
        4. Comprobación de cupos disponibles
        5. Verificación de tamaño del equipo
        6. Registro de la inscripción si se cumplen todas las condiciones

        Args:
            request: Objeto HttpRequest
            tournament_id: ID del torneo a inscribirse
            team_id: ID del equipo a inscribir

        Returns:
            HttpResponseRedirect: Redirección a la vista de detalle del torneo
        """
        tournament = get_object_or_404(Tournament, id=tournament_id)
        team = get_object_or_404(Team, id=team_id)
        player = Player.objects.get(user=request.user)

        # Verificar que el usuario forme parte del equipo
        if not team.player_set.filter(user=request.user).exists():
            messages.error(request, "No puedes inscribir un equipo al que no perteneces.")
            return redirect(reverse("web:tournamentDetailView", args=[tournament_id]))

        # Verificar que el usuario sea lider del equipo
        if team.leader != player:
            messages.error(request, "Solo el líder del equipo puede inscribir al equipo en el torneo.")
            return redirect(reverse("web:tournamentDetailView", args=[tournament_id]))

        # Verificar que el equipo no esté ya inscrito
        if TournamentTeam.objects.filter(tournament=tournament, team=team).exists():
            messages.warning(request, "Este equipo ya está inscrito en el torneo.")
            return redirect(reverse("web:tournamentDetailView", args=[tournament_id]))

        # Verificar si hay cupo en el torneo
        if TournamentTeam.objects.filter(tournament=tournament).count() >= tournament.max_teams:
            messages.error(request, "El torneo ya ha alcanzado el número máximo de equipos.")
            return redirect(reverse("web:tournamentDetailView", args=[tournament_id]))

        # Verificar que el equipo tenga el número correcto de jugadores
        if team.player_set.count() != tournament.max_player_per_team:
            messages.error(request, f"Tu equipo debe tener exactamente {tournament.max_player_per_team} jugadores para inscribirse.")
            return redirect(reverse("web:tournamentDetailView", args=[tournament_id]))

        # Inscribir el equipo
        TournamentTeam.objects.create(tournament=tournament, team=team)
        messages.success(request, f"¡Tu equipo {team.name} ha sido inscrito correctamente en el torneo {tournament.name}!")
        return redirect(reverse("web:tournamentDetailView", args=[tournament_id]))
