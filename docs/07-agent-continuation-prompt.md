# Prompt Para Otro Agente

Usa este prompt si quieres lanzar otro agente en paralelo o continuar el proyecto en otra sesion.

```txt
Trabaja solo dentro de:
stormsboys-ai-agents-challenge

Primero lee:
- AGENTS.md
- HANDOFF.md
- docs/06-next-critical-path.md
- docs/04-judging-scorecard.md

Reglas:
- No uses ni mezcles codigo, configuracion, rutas, IDs, datos ni recursos de otros proyectos.
- No leas .env ni secretos.
- No crees recursos en Google Cloud sin plan previo, coste esperado y rollback.
- Mantén Track 3 como historia principal y usa Track 1/2 como evidencia:
  build de capa nueva, evaluacion, guardrails y trazas.
- Todo cambio debe pasar make test, make lint y make public-ready.

Estado actual:
- API FastAPI funcional y desplegada en Cloud Run.
- Demo web publica en /.
- Agente raiz ADK-first.
- Agentes especializados: ingestion, analysis, retrieval, character, scene, consistency, narration y publisher insights.
- Evaluacion before/after con 12 casos.
- Cloud SQL PostgreSQL + pgvector activo.
- Gemini `gemini-2.5-flash` y embeddings `gemini-embedding-001` activos via Vertex AI.
- Dockerfile e infra Cloud Run creados.
- Tests Docker/Python 3.11: 46.
- Revision Cloud Run actual: revisar `HANDOFF.md`.

Tarea sugerida:
[ESCRIBIR AQUI UNA TAREA CONCRETA Y ACOTADA]

Al terminar, reporta:
- Archivos cambiados.
- Comandos ejecutados.
- Resultado de validacion.
- Riesgos pendientes.
```
