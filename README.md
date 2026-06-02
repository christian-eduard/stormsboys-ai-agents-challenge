# Stormsboys AI Agents Challenge

Proyecto nuevo para preparar la entrega de Stormsboys Libros IA al Google for Startups AI Agents Challenge. Este workspace es autocontenido y no mezcla codigo, configuracion ni recursos de otros proyectos.

## Decision principal

- Track elegido: Track 2 - Optimize Existing Agents.
- Producto objetivo: plataforma multi-agente que convierte libros en experiencias conversacionales con Gemini, RAG, memoria narrativa, voz y herramientas para lectores/publishers.
- Entrega objetivo: demo de 1-2 minutos en ingles, arquitectura Cloud Run + Gemini + Cloud SQL/pgvector + capa ADK/Agent layer, evaluacion de calidad y documentacion tecnica clara.

## Reglas de separacion

- No copiar codigo de otros proyectos.
- No traer deuda tecnica conocida: secretos, credenciales demo, nombres legacy, wrappers confusos o configuraciones inconsistentes.
- No usar rutas, IDs, servicios, cuentas o datos de otros proyectos.
- Toda decision importante debe quedar documentada en `docs/adr`.

## Estructura

- `docs/product`: vision, alcance, usuario, demo y narrativa de negocio.
- `docs/agents`: diseno de agentes, herramientas, contratos y memoria.
- `docs/cloud`: arquitectura Google Cloud, despliegue y servicios.
- `docs/evaluation`: metricas, simulaciones, tests y observabilidad.
- `docs/demo`: guion, assets y checklist de submission.
- `docs/security`: seguridad, secretos, privacidad y politicas.
- `docs/adr`: decisiones tecnicas versionadas.
- `src`: codigo nuevo de API, agentes, schemas, evaluacion y demo web.
- `tests`: pruebas automatizadas del API y demo.

## Arquitectura

Diagrama para Devpost:

- `docs/submission/architecture-diagram.mmd`

Resumen:

```mermaid
flowchart LR
  J["Judges"] --> WEB["Cloud Run Web/API"]
  WEB --> AG["ADK-first Agent Layer"]
  AG --> GM["Gemini 2.5 Flash"]
  AG --> DB["Cloud SQL + pgvector"]
  AG --> EMB["gemini-embedding-001"]
  AG --> OBS["Agent Traces"]
```

## Primeros documentos

1. Leer `AGENTS.md`.
2. Leer `HANDOFF.md`.
3. Leer `docs/00-challenge-brief.md`.
4. Leer `docs/product/01-product-vision.md`.
5. Leer `docs/agents/01-agent-architecture.md`.
6. Leer `docs/cloud/01-target-architecture.md`.
7. Leer `docs/evaluation/01-evaluation-plan.md`.
8. Leer `docs/08-original-app-track3-analysis.md` para entender como conectar la app real de libros y Don Quijote.

## Estado actual

Demo publica desplegada en Google Cloud Run:

```txt
https://stormsboys-agents-api-5mpmuf566a-uc.a.run.app
```

Repositorio publico:

```txt
https://github.com/christian-eduard/stormsboys-ai-agents-challenge
```

Ya existe una API FastAPI con demo web para jueces, agente raiz ADK-first, agentes
especializados, Cloud SQL PostgreSQL con pgvector, embeddings `gemini-embedding-001`
via Vertex AI, Character Agent con `gemini-2.5-flash`, trazas por agente y
evaluacion before/after para Track 2.

La demo cubre:

- Lector con libro demo.
- Analisis literario.
- Chat con personaje.
- Escena multi-personaje.
- Plan de voz/narracion.
- Vista publisher/admin.
- Evaluacion baseline vs optimized.
- Panel runtime con Gemini, Cloud SQL/pgvector, seed y retrieval path.

## Ejecutar Local

```bash
make setup
make test
make lint
make dev
```

En otra terminal:

```bash
BASE_URL=http://127.0.0.1:8080 make smoke
```

## Endpoints Demo

- `GET /health`
- `GET /`
- `GET /api/v1/challenge/readiness`
- `GET /api/v1/challenge/capabilities`
- `GET /api/v1/demo/book`
- `POST /api/v1/demo/chat/character`
- `POST /api/v1/demo/chat/scene`
- `POST /api/v1/demo/narration`
- `GET /api/v1/demo/publisher`
- `GET /api/v1/demo/evaluation`

## Validacion

```bash
make test
make lint
make public-ready
BASE_URL=https://stormsboys-agents-api-5mpmuf566a-uc.a.run.app make smoke
```

Ultima validacion conocida:

- Tests Docker/Python 3.11: 20 passed.
- Lint: passed.
- Public-ready scan: passed.
- Public smoke test: passed.

## Estado De Implementacion

- API local y publica: implementada.
- ADK root agent: implementado.
- Agentes especializados demo: implementados.
- Evaluacion before/after: implementada con 12 casos.
- Dockerfile para Cloud Run: creado.
- Frontend demo servido por FastAPI: implementado.
- Gemini adapter central: implementado con fallback demo.
- Gemini real: activo via Vertex AI con identidad gestionada.
- Cloud Run real: desplegado.
- Cloud SQL/pgvector: activo.
- Tests: 20 tests pasan en Python 3.11.
