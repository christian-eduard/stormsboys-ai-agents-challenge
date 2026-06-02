# Implementation Baseline

## Decision

El proyecto nuevo empieza con una capa Python-first para agentes porque ADK oficial soporta Python con `google-adk` y permite evolucionar hacia Agent Engine.

## Modulos Iniciales

- `src/storms_agents/api`: API FastAPI para demo y health checks.
- `src/storms_agents/agents`: agentes ADK.
- `src/storms_agents/tools`: adaptadores de herramientas.
- `src/storms_agents/schemas.py`: contratos Pydantic.
- `src/storms_agents/observability.py`: trazas internas.
- `tests`: pruebas nuevas.

## Regla De Aislamiento

La primera prueba funcional del proyecto expone:

- Track elegido.
- Modo demo.
- Regla de no mezclar proyectos.
- Capa agentic ADK-first.

## Comandos Locales

```bash
cd stormsboys-ai-agents-challenge
make setup
make test
make dev
```

## Estado Implementado

- Gemini real activo via Vertex AI para Character Agent.
- Embeddings reales `gemini-embedding-001` via Vertex AI.
- Agentes especializados implementados.
- Frontend demo implementado.
- Infra reproducible en `infra/cloud-run`.
- Cloud Run publico desplegado.
- Cloud SQL/pgvector activo.

## Validacion Actual

- Dependencias instaladas correctamente.
- `google-adk` resuelto a version `2.1.0`.
- `google-genai` resuelto a version `1.75.0`.
- Tests pasan.
- Lint pasa.
- API local verificada con `curl`.
- Demo web servida en `/`.
- Smoke test local pasa.
- Public-ready scan pasa.
- Dockerfile creado.
- Docker build local pasa.
- Contenedor local pasa smoke test.
- Contenedor arranca sin reloader en modo `demo`.
- Gemini adapter central creado con fallback demo.
- Endpoint `/api/v1/challenge/capabilities` creado.
- Evaluacion Track 2 ampliada a 12 casos con summary baseline vs optimized.
- Voice/Narration Agent implementado.
- Publisher Insights Agent implementado.
- Tests Docker/Python 3.11: 20.
- Smoke publico pasa.
