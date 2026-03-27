# 🤖 Bot de Soporte con AWS Bedrock (ArenaGG)

## 📋 Objetivo

Este documento define lo necesario para integrar un bot de soporte con AWS Bedrock en ArenaGG, reutilizando la página de soporte existente y la FAQ actual.

El objetivo es que el bot:

- Responda dudas frecuentes de usuarios en lenguaje natural.
- Use una base de conocimiento (RAG) para responder con contexto real del proyecto.
- Escale a soporte humano cuando no tenga certeza o cuando el caso sea sensible.

---

## 🧱 Estado actual de ArenaGG (implementado)

Ya existe y esta operativo en el proyecto:

- Página de soporte con formulario (`SupportView`) y chat de IA embebido.
- Endpoint de chat autenticado (`POST /api/support/chat/`).
- Cliente Bedrock con retrieval sobre Knowledge Base y respuesta generativa.
- Correo de soporte configurado (`SUPPORT_EMAIL`) y escalado humano.
- Reglas de escalado por casos sensibles + baja confianza.

Estado AWS confirmado:

- Región: `us-east-1`
- Knowledge Base ID: `C5B2GIAZKP`
- Vector store: S3 Vectors
- Modelo por defecto: Amazon Nova Lite
- Fallback de modelos: Nova -> Anthropic (si disponible en cuenta)

---

## ☁️ Setup AWS paso a paso (IAM + S3 + KB)

### 1) Crear usuario/perfil IAM para Bedrock

Objetivo: evitar usar cuenta root y aislar permisos del bot.

Pasos:

1. AWS Console -> IAM -> Users -> Create user.
2. Nombre sugerido: `arenagg-bedrock-bot`.
3. Activar `Programmatic access` (Access key).
4. Adjuntar política (MVP):
	- `AmazonBedrockFullAccess`
	- `AmazonS3FullAccess` (o política limitada al bucket del proyecto)
5. Crear usuario y guardar:
	- `AWS_ACCESS_KEY_ID`
	- `AWS_SECRET_ACCESS_KEY`

Recomendación producción:

- Reemplazar permisos amplios por permisos mínimos (least privilege) sobre:
  - Bedrock runtime + agent runtime
  - bucket S3 específico

### 2) Crear bucket S3 para conocimiento

Objetivo: almacenar documentos fuente de la base de conocimiento.

Pasos:

1. AWS Console -> S3 -> Create bucket.
2. Región: `us-east-1` (misma región que Bedrock en este proyecto).
3. Nombre sugerido: `arenagg-kb-<env>-<account-id>`.
4. Mantener `Block all public access` activado.
5. Cargar los documentos seed (FAQ, guías, políticas, soporte).

Estructura recomendada en S3:

- `kb/faq/*.md`
- `kb/guides/*.md`
- `kb/policies/*.md`
- `kb/support/*.md`

### 3) Crear Knowledge Base en Bedrock

Pasos:

1. AWS Console -> Amazon Bedrock -> Knowledge Bases -> Create.
2. Seleccionar fuente S3 (bucket anterior).
3. Configurar vector store (S3 Vectors para este MVP).
4. Completar creación y copiar `Knowledge Base ID`.
5. Ejecutar sincronización/indexado inicial.

Valor actual del proyecto:

- `BEDROCK_KB_ID=C5B2GIAZKP`

### 4) Configurar `.env` en Django

Variables necesarias:

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_REGION=us-east-1`
- `BEDROCK_KB_ID=<kb-id>`
- `BEDROCK_MODEL_ID=amazon.nova-lite-v1:0`

### 5) Verificar integración

1. Reiniciar servicio web (`docker compose up -d --build web`).
2. Abrir página de soporte y enviar una consulta de prueba.
3. Confirmar en logs que no hay errores de credenciales o acceso S3/Bedrock.

---

## 🏗️ Arquitectura recomendada (RAG)

1. Frontend (página de soporte)
- Chat UI en `web/support.html` (widget simple de mensajes).
- Botón alternativo para "Contactar humano".
- Mantener coherencia con acceso autenticado de soporte (fallback para usuarios sin sesion: FAQ publica + login).

2. Backend Django
- Endpoint API para chat (`POST /api/support/chat/`).
- Endpoint opcional para feedback (`POST /api/support/feedback/`).
- Registro de conversaciones (logs, métricas y auditoría).

3. AWS Bedrock
- Modelo fundacional para generación (con fallback de modelos).
- Knowledge Base para RAG con documentos de ArenaGG.
- Recuperación de fragmentos relevantes + respuesta final.

4. Escalado a humano
- Si baja confianza o caso sensible, redirigir a `SupportView` (email).
- Incluir resumen automático del chat en el ticket para soporte.
- Considerar que los adjuntos del formulario deben validarse en backend antes de prometer envio de evidencia.

---

## 📚 Base de conocimiento mínima

Para respuestas de calidad, la KB debe incluir como mínimo:

1. FAQ de usuario final
- Cuenta y acceso.
- Equipos y torneos.
- Resultados y discrepancias.
- Recompensas y premium.
- Errores comunes y pasos de resolución.

2. Guías de uso
- Crear equipo.
- Unirse a torneo.
- Reportar resultado.
- Contactar soporte.

3. Políticas
- Privacidad y términos.
- Criterios de soporte y tiempos de respuesta.
- Casos que requieren verificación humana.

4. Glosario
- MMR, renombre, VIP, canje, torneo upcoming/ongoing/completed.

---

## 🗂️ Formato recomendado para documentos (RAG-friendly)

Usar Markdown con estructura consistente:

- Título claro por tema.
- Preguntas y respuestas cortas.
- Pasos numerados.
- Sección "Cuándo escalar a humano".
- Metadatos al inicio (opcional): categoría, prioridad, idioma, versión.

Ejemplo de cabecera útil:

```md
---
category: soporte
topic: torneos
language: es
version: 1.0
last_updated: 2026-03-20
---
```

---

## 🛡️ Guardrails del bot

El bot debe cumplir estas reglas:

1. No inventar datos
- Si no encuentra respuesta en KB: decirlo y escalar.

2. Seguridad
- No revelar datos de otros usuarios.
- No modificar cuentas ni resultados desde chat.

3. Casos sensibles (escalar)
- Cobros/pagos.
- Reclamaciones de premios.
- Bloqueos de cuenta.
- Disputas de resultados entre equipos.

4. Transparencia
- Informar que es asistente virtual.
- Mostrar cuando la respuesta es orientativa.

---

## 🧠 Prompt de sistema recomendado

Usar un prompt base similar a este:

```text
Eres el asistente de soporte de ArenaGG. Responde siempre en espanol claro y breve.
Solo puedes responder usando la informacion recuperada de la base de conocimiento.
Si la informacion no es suficiente, indicalo y ofrece escalar a soporte humano.
Nunca inventes politicas, precios, estados de cuenta o resultados de torneos.
No solicites datos sensibles innecesarios.
Para casos sensibles (pagos, bloqueos, disputas, premios), deriva a soporte humano.
```

---

## ⚙️ Estado técnico real (backend y frontend)

Backend implementado:

- `web/bedrock_client.py`
	- `retrieve_from_kb()` usa `bedrock-agent-runtime.retrieve`.
	- `generate_response()` usa `bedrock-runtime.converse`.
	- Normalización de confianza para mostrar un valor más interpretable en UI.
	- Fallback automático de modelos en errores de:
		- throughput on-demand no soportado
		- modelo legacy/inactivo
		- modelo Anthropic sin formulario de use case aprobado
- `web/views.py`
	- API `support_chat_api` protegida con autenticación.
- `web/serializers.py`
	- Validación de entrada/salida para el chat.
- `web/urls.py`
	- Ruta de API activa: `api/support/chat/`.

Frontend implementado:

- `web/templates/web/support.html`
	- Formulario clásico de soporte + chat IA en la misma pantalla.
	- Estado de carga, mensajes de error, aviso de escalado y bloque de confianza.
	- Formateo de salida del asistente (saltos de línea, negritas y enlaces).
- `web/static/css/support.css`
	- Mejora de contraste del aviso de escalado.
	- Estilos de legibilidad para mensajes del asistente.
	- Indicador de confianza con mejor visibilidad.

---

## 🧩 Variables de entorno Bedrock (actuales)

Variables mínimas requeridas:

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_REGION=us-east-1`
- `BEDROCK_KB_ID=C5B2GIAZKP`
- `BEDROCK_MODEL_ID=amazon.nova-lite-v1:0`

Variables opcionales recomendadas:

- `BEDROCK_MODEL_CANDIDATES=amazon.nova-lite-v1:0,amazon.nova-micro-v1:0,us.anthropic.claude-3-5-haiku-20241022-v1:0`

---

## 🧯 Incidencias AWS resueltas durante integración

1. Error de payload en `converse`
- Causa: uso de campos no válidos (`systemPrompt`) y formato incorrecto de `messages[].content`.
- Solución: usar `system` y `content` como lista de bloques de texto.

2. Modelo Anthropic on-demand no soportado
- Causa: model ID de tipo on-demand sin inference profile.
- Solución: fallback por IDs compatibles y cambio de modelo por defecto.

3. Modelo marcado como legacy/inactivo
- Causa: cuenta sin uso reciente del modelo concreto.
- Solución: fallback automático al siguiente candidato.

4. Formulario de use case Anthropic no aprobado
- Causa: cuenta sin formulario de proveedor completado o propagado.
- Solución: priorizar Amazon Nova y mantener Anthropic como fallback opcional.

---

## 🔁 Flujo de conversación recomendado

1. Usuario pregunta.
2. Backend consulta KB (recupera fragmentos relevantes).
3. Bedrock genera respuesta con contexto.
4. Se calcula criterio de confianza (simple o heurístico).
5. Si confianza baja o caso sensible:
- Respuesta de transición.
- Botón o enlace para soporte humano.
- Resumen del chat para ticket.

---

## 📏 Métricas de calidad

Mínimo a medir:

- Tasa de resolución sin humano.
- Tasa de escalado.
- Tasa de "no sé".
- Satisfacción del usuario (thumbs up/down).
- Tiempo medio de respuesta.

Objetivo inicial recomendado:

- Resolución automática >= 60% en preguntas frecuentes.
- Alucinaciones críticas = 0.

---

## 🧪 Plan de pruebas antes de producción

1. Crear set de 100 preguntas reales o probables.
2. Clasificarlas por categoría.
3. Definir respuesta esperada y criterio de aprobado.
4. Probar:
- Con respuesta correcta.
- Sin contexto suficiente.
- Casos sensibles con escalado.
5. Revisar semanalmente logs y actualizar KB.

---

## 🚀 Roadmap sugerido

### Fase 1 (MVP)

- Chat en página de soporte.
- 50-100 FAQs bien redactadas.
- Escalado a humano por email.
- Logging básico.

### Fase 2

- Feedback del usuario por respuesta.
- Panel interno de métricas.
- Mejoras de prompt y recuperación.

### Fase 3

- Personalización por perfil (jugador premium/no premium).
- Respuestas proactivas según contexto de la cuenta.

---

## ✅ Checklist de "listo para producción"

- [x] KB creada con cobertura funcional de soporte.
- [x] Prompt y guardrails validados.
- [x] Casos sensibles definidos y probados.
- [ ] Métricas activas y observabilidad mínima (pendiente panel/reporting).
- [x] Flujo de fallback humano operativo.
- [ ] Revisión legal (privacidad y términos).

---

## 🔄 Navegación

- [README principal](../README.md)
- [Vistas](VIEWS.md)
- [Formularios](FORMS.md)
- [Tests](TESTS.md)
- [Tareas programadas](TASKS.md)
