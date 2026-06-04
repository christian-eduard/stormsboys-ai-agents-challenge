# Agent Interoperability Contract

Fecha: 2026-06-05.

## Estado Implementado

Stormsboys publica una capa interoperable minima para Track 3:

- `/.well-known/agent-card.json`
- `/a2a/agent-card.json`
- API HTTP JSON versionada bajo `/api/v1`
- Endpoints protegidos por token demo para roles Publisher/Admin/Judge
- Export JSON y CSV para que otros agentes lean readiness de catalogo

Esto es **A2A-ready**, no un runtime A2A completo. La entrega no debe prometer
coordinacion A2A production-grade ni MCP tool server hasta que se implemente y se pruebe.

## Invocaciones Para Agentes Externos

### Descubrir Capacidades

```bash
curl https://stormsboys-agents-api-5mpmuf566a-uc.a.run.app/.well-known/agent-card.json
```

Uso: otro agente puede descubrir nombre, descripcion, protocolos y capacidades de la plataforma.

### Leer Estado De Submission

```bash
curl https://stormsboys-agents-api-5mpmuf566a-uc.a.run.app/api/v1/challenge/submission
```

Uso: verificar tracks, criterios, entregables y cuenta recomendada para jueces.

### Ejecutar Chat De Personaje

```bash
curl -X POST https://stormsboys-agents-api-5mpmuf566a-uc.a.run.app/api/v1/demo/chat/character \
  -H "Content-Type: application/json" \
  -d '{
    "book_id": "don-quijote",
    "character_id": "don_quijote",
    "mode": "CANON",
    "language": "en",
    "session_id": "external-agent-demo",
    "question": "Why do you attack the windmills?"
  }'
```

Uso: probar retrieval, personalidad, psicologia, citas, consistencia y separacion canon/ficcion.

### Leer Export Editorial JSON

```bash
curl https://stormsboys-agents-api-5mpmuf566a-uc.a.run.app/api/v1/admin/marketplace/export \
  -H "Authorization: Bearer demo-token:publisher-demo"
```

Uso: otro agente puede consumir catalogo, readiness, senales de lector, senales por seccion,
senales de personaje y totales de operacion.

### Descargar Export Editorial CSV

```bash
curl https://stormsboys-agents-api-5mpmuf566a-uc.a.run.app/api/v1/admin/marketplace/export.csv \
  -H "Authorization: Bearer demo-token:publisher-demo" \
  -o stormsboys-marketplace-insights.csv
```

Uso: preparar reporting, analisis externo o ingestion por agentes de ventas/editoriales.

## Lenguaje Seguro Para Devpost

Usar:

- "A2A-ready agent card and HTTP JSON interface."
- "Marketplace-oriented refactor deployed on Cloud Run."
- "Prepared for future ADK/A2A runtime integration."

No usar todavia:

- "Full A2A runtime."
- "Production MCP server."
- "Published Google Cloud Marketplace listing."

## Siguiente Paso Si Queda Tiempo

Implementar un endpoint especifico de tareas agenticas, por ejemplo:

```txt
POST /api/v1/agents/tasks
```

Con contrato:

- `task_type`: `character_chat`, `catalog_export`, `publisher_review`
- `input`: payload versionado
- `trace_id`: identificador de trazabilidad
- `result`: salida estructurada

Ese endpoint acercaria la demo a orquestacion agent-to-agent real sin sobreprometer runtime.
