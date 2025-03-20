from django.urls import path
from . import views  # Asegúrate de que las vistas estén importadas
from django.conf import settings
from django.conf.urls.static import static

# Definir el nombre de la aplicación para los nombres de las rutas
app_name = 'web'

# Definir las rutas de URL para la aplicación
urlpatterns = [
    # Ruta para la vista principal del índice
    path('', views.index, name='index'),  # Cambia esto por las vistas que tengas
    path('player/', views.PlayerListView.as_view(), name='playerView'),  # Vista de lista de jugadores

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)