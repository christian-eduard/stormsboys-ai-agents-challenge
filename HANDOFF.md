# Handoff Para Continuar El Proyecto

Este archivo es el punto de entrada para cualquier agente nuevo. Si solo tienes tiempo para leer una cosa, lee esto.

## Contexto

Estamos creando un proyecto nuevo, aislado y autocontenido para el Google for Startups AI Agents Challenge.

- Track: Track 2 - Optimize Existing Agents.
- Entrega: repositorio publico, descripcion en ingles, arquitectura con diagrama, video demo de 1-2 minutos en ingles y demo funcional para jueces.
- Regla critica: no usar codigo, configuracion, datos, rutas, IDs ni recursos de otros proyectos.
- Nueva conclusion de producto: la demo debe pivotar hacia la app real `Stormsboys_libros/libros-ia-app` y Don Quijote sin copiar codigo a ciegas; ver `docs/08-original-app-track3-analysis.md`.

## Estado Actual

Ya existe:

- API FastAPI.
- Demo web servida en `/`.
- Endpoint de capabilities con criterios del challenge, entregables y runtime.
- Endpoint de storage con estado Cloud SQL/pgvector: `/api/v1/challenge/storage`.
- Endpoint de seed demo en Cloud SQL/pgvector: `/api/v1/challenge/storage/demo-seed`.
- Agente raiz ADK-first.
- Agentes deterministas de demo.
- Evaluacion before/after para Track 2 con 12 casos.
- Gemini adapter central con fallback demo.
- Character Agent conectado a Gemini/Vertex real cuando esta configurado.
- Guardrail de voz: la respuesta generada conserva el nombre/persona del personaje antes de pasar consistencia.
- Trazas basicas por agente.
- VoiceNarrationAgent para preparar narracion/SSML lista para TTS.
- PublisherInsightsAgent para vista admin con engagement, calidad y recomendaciones.
- Dockerfile.
- Scripts de smoke test y revision publica.
- Documentacion de producto, agentes, cloud, evaluacion, demo, seguridad y submission.
- Cloud SQL PostgreSQL 16 con pgvector inicializado.
- RetrievalAgent usa pgvector real cuando `DATABASE_URL` esta configurado y vuelve a memoria si falla.
- Libro demo sembrado en Cloud SQL con 4 secciones y embeddings `gemini-embedding-001` via Vertex AI.
- Panel web `Runtime proof` con estado Gemini, Cloud SQL/pgvector, seed y ultima traza de retrieval.

## Comandos Basicos

```bash
cd stormsboys-ai-agents-challenge
make test
make lint
make public-ready
make dev
```

En otra terminal:

```bash
BASE_URL=http://127.0.0.1:8080 make smoke
```

Demo local:

```txt
http://127.0.0.1:8080
```

## Validacion Conocida

Ultima validacion local conocida:

- Tests en contenedor Python 3.11: pasan, 20 tests.
- `make lint`: pasa.
- `make public-ready`: pasa.
- `BASE_URL=http://127.0.0.1:8088 make smoke`: pasa.
- Docker daemon: disponible tras abrir Docker Desktop.
- Docker build local: pasa.
- Smoke test contra contenedor local: pasa.
- Smoke test publico de Cloud Run: pasa.
- El contenedor arranca con `APP_ENV=demo` y sin reloader.
- Proyecto GCP del challenge creado: `stormsboys-agents-20260602`.
- Billing Pronexus enlazado.
- Budget guardrail de 50 EUR creado.
- Cloud Run desplegado: `https://stormsboys-agents-api-5mpmuf566a-uc.a.run.app`.
- Revision Cloud Run activa: `stormsboys-agents-api-00011-xds`.
- Cloud Run usa service account nueva: `stormsboys-agents-runtime@stormsboys-agents-20260602.iam.gserviceaccount.com`.
- No hay claves JSON de usuario ni credenciales antiguas en el runtime.
- Cloud SQL instance: `stormsboys-pgvector`.
- Cloud SQL database: `stormsbooks`.
- Cloud SQL user: `storms_agent`.
- Secret: `stormsboys-database-url`.
- Cloud Run Job de schema: `stormsboys-storage-init`.
- `/api/v1/challenge/storage`: `configured=true`, `pgvector_ready=true`.
- `/api/v1/challenge/storage/demo-seed`: `seeded=true`, `sections=4`.
- Embeddings publicos confirmados: `mode=gemini-embedding`, `model=gemini-embedding-001`, `vertexai=true`.
- Traza publica confirmada: `RetrievalAgent` usa `retrieval.pgvector_search`.
- Chat publico confirmado: `CharacterAgent` usa `gemini-2.5-flash` y `NarrativeConsistencyAgent` pasa.
- Narration publico confirmado: `VoiceNarrationAgent`, SSML y `ready_for_tts=true`.
- Publisher publico confirmado: `PublisherInsightsAgent`, engagement y quality `100%`.
- Smoke test publico confirmado el 2026-06-02 contra revision `stormsboys-agents-api-00011-xds`.
- Nota local: `.venv` usa Python 3.14 en este Mac y `pytest` puede quedarse colgado al arrancar importaciones de dependencias Google. Para validacion fiable usa Docker/Python 3.11, que coincide con Cloud Run.

## Mapa De Codigo

- `src/storms_agents/api/main.py`: FastAPI, endpoints y montaje web.
- `src/storms_agents/agents/root_agent.py`: agente raiz ADK.
- `src/storms_agents/agents/book_ingestion.py`: ingestion demo.
- `src/storms_agents/agents/literary_analysis.py`: analisis literario demo.
- `src/storms_agents/agents/retrieval.py`: retrieval demo.
- `src/storms_agents/agents/character.py`: respuesta de personaje.
- `src/storms_agents/agents/scene_orchestrator.py`: escena multi-personaje.
- `src/storms_agents/agents/consistency.py`: validacion narrativa.
- `src/storms_agents/agents/narration.py`: plan de voz/narracion para TTS.
- `src/storms_agents/agents/publisher_insights.py`: informe publisher/admin.
- `src/storms_agents/evaluation.py`: before/after Track 2.
- `src/storms_agents/storage/repository.py`: contrato Cloud SQL/pgvector y health check.
- `src/storms_agents/storage/embedding.py`: proveedor de embeddings Vertex/Gemini con fallback determinista de 768 dimensiones.
- `src/storms_agents/tools/gemini.py`: adaptador Gemini con fallback demo.
- `src/storms_agents/web/index.html`: interfaz de jueces.
- `src/storms_agents/web/static/app.js`: logica frontend.
- `src/storms_agents/web/static/styles.css`: estilos.
- `infra/cloud-run/plan.sh`: imprime plan de despliegue sin crear recursos.
- `infra/cloud-run/deploy.sh`: despliegue protegido por `CONFIRM_DEPLOY=true`.
- `docs/cloud/04-pronexus-credit-setup.md`: estado de facturacion/credito.
- `docs/08-original-app-track3-analysis.md`: analisis de app original, Don Quijote, ADK y Track 3.
- `tests/test_api.py`: cobertura de endpoints.

## Endpoints

- `GET /`
- `GET /health`
- `GET /api/v1/challenge/readiness`
- `GET /api/v1/challenge/capabilities`
- `GET /api/v1/challenge/storage`
- `GET /api/v1/challenge/storage/demo-seed`
- `GET /api/v1/demo/book`
- `POST /api/v1/demo/chat/character`
- `POST /api/v1/demo/chat/scene`
- `POST /api/v1/demo/narration`
- `GET /api/v1/demo/publisher`
- `GET /api/v1/demo/evaluation`

## Demo Publica

```txt
https://stormsboys-agents-api-5mpmuf566a-uc.a.run.app
```

## Repositorio Publico

```txt
https://github.com/christian-eduard/stormsboys-ai-agents-challenge
```

Validacion:

```bash
BASE_URL=https://stormsboys-agents-api-5mpmuf566a-uc.a.run.app make smoke
```

## Prioridades Siguientes

1. Conectar Gemini tambien a LiteraryAnalysisAgent o SceneOrchestratorAgent con el mismo patron seguro.
2. Mejorar agentes para usar schemas estrictos y trazas mas utiles.
3. Crear repo publico y limpiar metadatos.
4. Grabar video demo 1-2 minutos en ingles.
5. Completar testing access para jueces.
6. Ampliar embeddings reales de Gemini a ingestion de libros subidos por usuario si se implementa upload completo.

## Trabajo Seguro Para Otro Agente

Un agente puede trabajar en una de estas areas sin pisar a los demas:

- Gemini integration: conectar agentes concretos a `src/storms_agents/tools/gemini.py`.
- Persistence demo: `src/storms_agents/storage` y tests nuevos.
- Cloud scripts: `infra/cloud-run` y `scripts`.
- Submission copy: `docs/submission`.
- UI polish: `src/storms_agents/web`.
- Evaluation dataset: `src/storms_agents/evaluation.py` y `docs/evaluation`.

## Reglas De No Mezcla

- No leer `.env`.
- No copiar codigo de otros proyectos.
- No usar project IDs existentes salvo que el usuario lo apruebe para despliegue.
- No crear recursos cloud sin plan, coste esperado y rollback.
- No meter secretos en repo.

## Definition Of Ready Para Deploy

Antes de Cloud Run real:

- Docker build local pasa.
- Contenedor responde `/health` y pasa `make smoke`.
- `make public-ready` pasa.
- Region y proyecto GCP confirmados: `us-central1`, `stormsboys-agents-20260602`.
- Runtime con service account dedicada, no default compute.
- Secretos definidos en Secret Manager, no en codigo, si se agregan en el futuro.
- Coste esperado documentado.

## Cloud Run Scripts

Los scripts existen, pero no deben ejecutarse contra una cuenta real sin aprobacion:

```bash
GCP_PROJECT_ID=example-project ./infra/cloud-run/plan.sh
```

Despliegue real solo tras revisar plan:

```bash
CONFIRM_DEPLOY=true GCP_PROJECT_ID=... ./infra/cloud-run/deploy.sh
```
