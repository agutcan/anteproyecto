# Despliegue del soporte IA en AWS

Este documento resume como se publico el bot de soporte de ArenaGG en AWS.

## 1. Entorno

Se uso una instancia EC2 para ejecutar el microservicio `subirEC2`.

El objetivo era mantener la API interna en localhost y exponerla por un dominio publico con HTTPS.

## 2. Componentes de AWS

- **EC2**: maquina donde corre el servicio.
- **Elastic IP o IP publica**: direccion accesible desde Internet.
- **Security Group**: reglas de red de la instancia.
- **Dominio DNS**: apunta al servidor.
- **TLS**: certificado HTTPS generado con Let’s Encrypt.

## 3. Diseno de red

La API se ejecuto en `127.0.0.1:8081` para que no quede abierta directamente al exterior.

El trafico publico entra por un reverse proxy y luego se reenvia a la API local.

## 4. Flujo de peticiones

```text
Usuario -> Dominio publico -> Nginx/Proxy -> 127.0.0.1:8081 -> FastAPI
```

## 5. Puertos

Los puertos mas importantes son:

- `80`: redireccion HTTP.
- `443`: HTTPS.
- `8081`: puerto interno de la API.

## 6. Servicio persistente

Para que la API siga funcionando tras reinicios, se puede usar `systemd`.

La idea es arrancar Uvicorn automaticamente con el entorno virtual ya preparado.

## 7. Reverse proxy

Se prefirio un proxy inverso porque:

- permite TLS centralizado,
- deja la API privada,
- simplifica la publicacion con dominio,
- evita exponer el puerto de FastAPI directamente.

## 8. Seguridad

Buenas practicas aplicadas:

- no exponer el servicio en todas las interfaces,
- mantener las credenciales en `.env`,
- usar un token para `/reindex`,
- separar la capa publica del servicio interno,
- abrir solo lo necesario en el Security Group.

## 9. Requisitos de la instancia

La documentacion del proyecto indica que la instancia debe tener recursos moderados, porque el bot usa embeddings y FAISS.

Para funcionar bien necesita:

- disco suficiente para el indice,
- permisos de escritura en `data`,
- red estable para hablar con el proveedor LLM,
- memoria suficiente para cargar el modelo de embeddings.

## 10. Integracion con el dominio

La URL publica usada para el bot fue del estilo:

```text
https://api.arenagg.tech
```

Desde Django se consume el endpoint `.../chat`.

## 11. Operacion normal

Cuando se actualiza la documentacion:

1. Se copian o editan los archivos Markdown.
2. Se ejecuta el reindexado.
3. Se reinicia el servicio si es necesario.
4. Django sigue consumiendo la misma URL.

## 12. Resultado final

El usuario final accede a un soporte automatico que responde dudas de la aplicacion, mientras la infraestructura real queda oculta en AWS y protegida por proxy, TLS y reglas de red.
