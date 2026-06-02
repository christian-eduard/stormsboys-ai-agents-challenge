# Seguridad

## Reglas

- No guardar `.env`.
- No guardar claves de API.
- No guardar keystores.
- No imprimir claves en logs.
- No usar credenciales demo obvias en repositorios publicos.
- No subir libros privados a entornos publicos sin permiso.
- No enviar texto completo de libros privados a logs.

## Secretos

Los secretos deben vivir en:

- Secret Manager en Google Cloud.
- Variables locales ignoradas por Git durante desarrollo.

## Datos De Demo

El libro demo debe ser:

- Propio.
- Publico.
- Con permiso explicito.
- O generado para la demo.

## Logs

Logs permitidos:

- `traceId`.
- agente.
- latencia.
- estado.
- tamanos/token counts.
- ids internos.

Logs no permitidos:

- claves.
- tokens.
- passwords.
- texto completo de libros privados.
- conversaciones privadas completas.

## Checklist Antes De Publicar

- Buscar claves con detectores.
- Revisar `.gitignore`.
- Revisar logs.
- Revisar credenciales demo.
- Revisar variables publicas de frontend.
