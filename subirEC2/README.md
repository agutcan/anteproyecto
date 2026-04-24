# subirEC2 - Guia de pasos pendientes

Este modulo ya esta creado y conectado con la vista de soporte de Django.
Aqui tienes solo lo que falta por hacer y como hacerlo.

## Estado actual

- RAG local listo (embeddings + FAISS + retrieval).
- API de chat lista en app/main.py.
- Proveedores LLM listos (openai, mistral, together, bedrock).
- Django ya apunta al endpoint /chat del servicio subirEC2.

## Checklist de pendientes

1. Configurar proveedor LLM y credenciales.
2. Cargar documentos reales de soporte.
3. Generar el indice vectorial.
4. Levantar el servicio de subirEC2.
5. Probar chat desde API y desde la vista de soporte.
6. (EC2) Dejar servicio persistente con systemd.

## 1) Configurar proveedor LLM y credenciales

Desde esta carpeta:

PowerShell:

```powershell
copy .env.example .env
```

Bash:

```bash
cp .env.example .env
```

Edita .env y configura lo minimo:

- LLM_PROVIDER=openai | mistral | together | bedrock
- LLM_API_KEY=<tu_clave> (solo para openai/mistral/together)
- LLM_MODEL=<modelo_valido_del_proveedor>
- ADMIN_TOKEN=<token_largo_y_privado>

Si usas Bedrock:

- LLM_PROVIDER=bedrock
- BEDROCK_MODEL_ID=<modelo>
- AWS_REGION=<region>
- Credenciales AWS por variables o IAM role en EC2.

## 2) Instalar dependencias

PowerShell:

```powershell
python -m venv .venv
. .venv/Scripts/Activate.ps1
pip install -r requirements.txt
```

Bash:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 3) Cargar documentos reales

Pon tus .md y .txt en documents/.

Ejemplos ya incluidos:

- documents/support_faq.md
- documents/politicas.md

Recomendacion:

- Una politica o FAQ por archivo.
- Texto claro y corto.
- Evitar duplicados.

## 4) Generar indice vectorial

```bash
python -m app.ingest
```

Resultado esperado:

- data/index.faiss
- data/metadata.json

## 5) Levantar la API de subirEC2

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8081
```

Comprobacion rapida:

```bash
curl http://127.0.0.1:8081/health
```

## 6) Probar endpoints

Chat:

```bash
curl -X POST http://127.0.0.1:8081/chat \
  -H "Content-Type: application/json" \
  -d '{"question":"Como recupero mi cuenta?"}'
```

Reindex:

```bash
curl -X POST http://127.0.0.1:8081/reindex \
  -H "X-Admin-Token: TU_ADMIN_TOKEN"
```

## 7) Verificar integracion con Django

En el .env principal del proyecto (raiz):

- SUPPORT_AI_API_URL=http://127.0.0.1:8081/chat
- SUPPORT_AI_TIMEOUT=20

Luego:

1. Arranca subirEC2 (uvicorn).
2. Arranca Django.
3. Abre la pagina soporte y envia una pregunta.

Si falla, revisa:

- URL y puerto del servicio.
- Que exista index.faiss.
- Que LLM_API_KEY sea valida.

## 8) Pasos para EC2 (produccion minima)

1. Subir codigo a la instancia.
2. Crear entorno virtual e instalar requirements.
3. Configurar .env con claves reales.
4. Ejecutar python -m app.ingest.
5. Levantar uvicorn en 127.0.0.1:8081.
6. Configurar Django para consumir esa URL.

## 9) Crear servicio systemd en EC2 (recomendado)

Archivo: /etc/systemd/system/subirec2.service

```ini
[Unit]
Description=subirEC2 FastAPI service
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/anteproyecto/subirEC2
Environment="PATH=/home/ubuntu/anteproyecto/subirEC2/.venv/bin"
ExecStart=/home/ubuntu/anteproyecto/subirEC2/.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8081
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Activacion:

```bash
sudo systemctl daemon-reload
sudo systemctl enable subirec2
sudo systemctl start subirec2
sudo systemctl status subirec2
```

## 10) Recomendaciones para t3.small

- TOP_K entre 4 y 6.
- Embedding ligero (multilingual-e5-small).
- Reindexar solo cuando cambien documentos.
- Mantener docs limpios para reducir latencia.
