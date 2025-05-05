# Readme Inicial
---
# 🎮 Título del proyecto

**ArenaGG - Plataforma de gestión de torneos de videojuegos**

## 👤 Autor del proyecto

Aarón Gutiérrez Caña

## 📌 Tabla de Contenidos

## 📖 Introducción del proyecto

El objetivo principal del proyecto es desarrollar una plataforma web llamada **ArenaGG**, destinada a la organización y gestión de torneos de videojuegos como **Valorant**, **League of Legends**, **Counter-Strike 2**, etc... Esta plataforma permitirá a los usuarios inscribirse, gestionar sus equipos, seguir el progreso de los torneos y consultar resultados en tiempo real. 

## 🎯 Finalidad

La plataforma **ArenaGG** servirá para facilitar la creación, administración y seguimiento de torneos de videojuegos, ofreciendo una experiencia fluida tanto para organizadores como para participantes. Permitirá automatizar procesos como la inscripción, el emparejamiento de equipos y la publicación de resultados.

Además, los torneos podrán ofrecer puntos de la página que se podrán intercambiar por premios en efectivo, merchandising, suscripciones u otros beneficios, lo que fomentará la participación y la competitividad.

## ✅ Objetivos

Una vez puesta en marcha, la plataforma permitirá:

- 🔐 Registrar usuarios y crear perfiles personalizados.
- 📝 Inscribir equipos y jugadores en torneos específicos.
- 🔄 Automatizar el emparejamiento y generar los enfrentamientos.
- 📅 Mostrar calendarios y resultados en tiempo real.
- 🗂️ Gestionar múltiples torneos de forma simultánea.
- 🔔 Ofrecer un sistema de notificaciones para informar a los usuarios sobre partidas y resultados.
- Ganar puntos y reclamar recompensas.
- Ofrecer la posibilidad de ser VIP.
- Sistema de soporte.

## 🛠️ Medios hardware y software a utilizar

### 💻 Hardware

- 🖥️ Ordenador con procesador Intel i5 o superior, 8GB de RAM, 256GB de almacenamiento SSD.

### 📦 Software

- 🐍 **Lenguaje de programación:** Python (con Django para el backend)
- 🗄️ **Base de datos:** PostgreSQL
- 🌐 **Frontend:** HTML5, CSS3 (con Bootstrap 5), JavaScript
- 📦 **Contenerización:** Docker para empaquetar y **AWS** para desplegar la aplicación. 
- 🔄 **Control de versiones:** Git (con GitHub para la gestión del código)
- 🛠️ **Entorno de desarrollo:** PyCharm

## 📊 Planificación

### 📌 1. Análisis y diseño del sistema (1 semana)

- 📋 Definir requisitos funcionales y no funcionales.
- 📐 Crear diagramas de flujo y esquemas de base de datos.

### 🧑‍💻 2. Desarrollo del backend (3 semanas)

- 🔑 Implementar la autenticación de usuarios.
- 🏆 Crear el sistema de gestión de torneos.
- 🔢 Automatizar los emparejamientos y resultados.

### 🎨 3. Desarrollo del frontend (2 semanas)

- 🖌️ Diseñar las interfaces de usuario con **Bootstrap 5**.
- 🔗 Integrar las vistas con el backend.

### 📦 4. Contenerización y despliegue en AWS (2 semanas)

- 🐳 Dockerizar la aplicación para facilitar el despliegue.
- 🌐 Configurar la infraestructura en **AWS** (EC2 o ECS para la ejecución de contenedores).

### 🧪 5. Pruebas, validación y documentación (2 semanas)

- ✅ Realizar pruebas unitarias con **Django TestCase**.
- 📊 Validar el correcto funcionamiento de la plataforma.
- 📚 Redactar la documentación del sistema y el manual de usuario.

**⏳ Duración total estimada:** 10 semanas.
---

# Actualicaciones

## Hecho

- 📋 Definir requisitos funcionales y no funcionales.
- 📐 Crear diagramas de flujo y esquemas de base de datos.
- 🔑 Implementar la autenticación de usuarios.
- 🐳 Dockerizar la aplicación para facilitar el despliegue
- 📅 Mostrar calendarios y estadísticas con apis.
- 🔐 Registrar usuarios y crear perfiles personalizados.
- 📝 Inscribir equipos y jugadores en torneos específicos.
- 🔔 Ofrecer un sistema de notificaciones para informar a los usuarios sobre partidas y resultados. (Creado localmente es decir con mailpit, para despliegue tendría que cambiarlo)



## En proceso

- 🏆 Crear el sistema de gestión de torneos.
- 🔄 Automatizar el emparejamiento y generar los enfrentamientos.
- 📅 Mostrar resultados en tiempo real.
- 🗂️ Gestionar múltiples torneos de forma simultánea.
- 🔗 Integrar las vistas con el backend.
- 🖌️ Diseñar las interfaces de usuario con **Bootstrap 5**.
- Sistema de recompensas.
- Ofrecer la posibilidad de ser VIP.
- Sistema de soporte.


## Por hacer

- 🏆 Crear el sistema de gestión de torneos.
- 🗂️ Gestionar múltiples torneos de forma simultánea.
- 🔢 Automatizar los emparejamientos y resultados.
- Sistema de recompensas.
- Ofrecer la posibilidad de ser VIP. 
- 📅 Mostrar calendarios y resultados en tiempo real.
- 🔔 Ofrecer un sistema de notificaciones para informar a los usuarios sobre partidas y resultados.
- 🖌️ Diseñar las interfaces de usuario con **Bootstrap 5**.
- 🔗 Integrar las vistas con el backend.
- 🌐 Configurar la infraestructura en **AWS** (EC2 o ECS para la ejecución de contenedores).
- ✅ Realizar pruebas unitarias con **Django TestCase**.
- 📊 Validar el correcto funcionamiento de la plataforma.
- 📚 Redactar la documentación del sistema y el manual de usuario.
- 🛠️ Creación de tareas automatizadas.
- 🖥️ Apis para ver o crear algunos modelos.

## Modificaciones sobre el proyecto plantado inicialmente (“Si no hemos realizado todo lo planificado”)


## Posibles mejoras al proyecto (“Posibles mejoras futuras”)

- He decidido añadir tareas automatizadas para modificar el estado de cada torneo (por empezar, en proceso, finalizado) y enviar emails cada vez que vaya a empezar un torneo por ejemplo. (Con redis, celery y celery-beat)

## Bibliografía (“Si es posible con enlace a la fuente”)

- [Python – Documentación oficial](https://docs.python.org/3/)
- [JavaScript – MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
- [Bootstrap 5.3 – Introducción](https://getbootstrap.com/docs/5.3/getting-started/introduction/)
- [CSS – MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/CSS)
- [Celery – Documentación oficial](https://docs.celeryq.dev/en/stable/)
- [Django – Documentación oficial](https://docs.djangoproject.com/en/stable/)
- [Django REST Framework – Documentación oficial](https://www.django-rest-framework.org/)
- [Mailpit – Documentación oficial](https://mailpit.axllent.org/docs/)


# Documentación

