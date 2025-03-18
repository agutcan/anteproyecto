from django.urls import path
from . import views  # Asegúrate de que las vistas estén importadas

# Definir el nombre de la aplicación para los nombres de las rutas
app_name = 'web'

# Definir las rutas de URL para la aplicación
urlpatterns = [
    # Ruta para la vista principal del índice
    path('', views.index, name='index'),  # Cambia esto por las vistas que tengas

]