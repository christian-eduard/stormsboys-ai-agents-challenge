# Handoff Para Continuar El Proyecto

Este archivo es el punto de entrada para cualquier agente nuevo. Si solo tienes tiempo para leer una cosa, lee esto.

## Contexto

Estamos creando un proyecto nuevo, aislado y autocontenido para el Google for Startups AI Agents Challenge.

- Track principal: Track 3 - Refactor for Google Cloud Marketplace & Gemini Enterprise.
- Track secundario/evidencia: Track 2 - Optimize Existing Agents.
- Entrega: repositorio publico, descripcion en ingles, arquitectura con diagrama, video demo de 1-2 minutos en ingles y demo funcional para jueces.
- Regla critica: no usar codigo, configuracion, datos, rutas, IDs ni recursos de otros proyectos.
- Nueva conclusion de producto: no estamos construyendo solo una demo de Don Quijote. Estamos reconstruyendo de forma limpia la plataforma real de libros interactivos: upload, analisis Gemini, personajes con psicologia, modo canon, modo ficcion, lector, escena/grupo, voz, publisher y superadmin.
- Don Quijote es el caso demo principal por ser reconocible y de dominio publico.
- Idioma: ingles es el idioma primario de submission/jueces; espanol es secundario pero debe ser una opcion funcional en la experiencia.

## Lectura Obligatoria Para Otro Agente

1. `AGENTS.md`
2. `docs/product/04-original-product-model.md`
3. `docs/track3/01-track3-marketplace-strategy.md`
4. `docs/agents/04-platform-agent-operating-model.md`
5. `docs/adr/0004-track-3-platform-refactor.md`
6. `docs/09-real-platform-implementation-plan.md`
7. `docs/08-original-app-track3-analysis.md`

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
- `ConversationMode` con `CANON` y `FICTION` en API/UI.
- `ConversationLanguage` con `en` y `es` en API/UI.
- Perfiles de personaje con psicologia estructurada: estilo de habla, OCEAN, deseo,
  miedo, relaciones, baseline emocional y politica de memoria.
- Memoria conversacional persistente en Cloud SQL cuando `DATABASE_URL` esta configurado,
  separada por `session_id`, personaje y modo: canon no altera hechos del libro,
  ficcion guarda rama alternativa separada. En local cae a memoria de proceso.
- Endpoint y panel web de historial de memoria: `/api/v1/demo/chat/memory`
  muestra eventos persistidos, proveedor de memoria, preguntas, respuestas y preferencias.
- `FictionBranchAgent` minimo: crea ramas alternativas separadas de canon en la respuesta API.
- Agent card Track 3 publicada en `/.well-known/agent-card.json` y `/a2a/agent-card.json`.
- Dockerfile.
- Scripts de smoke test y revision publica.
- Documentacion de producto, agentes, cloud, evaluacion, demo, seguridad y submission.
- Documentacion nueva de producto real, Track 3 y modelo operativo de agentes.
- Cloud SQL PostgreSQL 16 con pgvector inicializado.
- RetrievalAgent usa pgvector real cuando `DATABASE_URL` esta configurado y vuelve a memoria si falla.
- Libro demo Don Quijote sembrado en Cloud SQL con 5 secciones y embeddings `gemini-embedding-001` via Vertex AI.
- Panel web `Runtime proof` con estado Gemini, Cloud SQL/pgvector, seed y ultima traza de retrieval.
- Pantalla web `Testing access` con cuentas demo por rol y entrada dedicada `Judge Access`.
- Panel web `Role dashboard` con acciones y navegacion filtradas para reader, author, publisher, superadmin y judge.
- Vista `Author` con flujo protegido `/api/v1/demo/author-workflow`, checklist de aprobacion y agentes generados.
- Consola web `Marketplace Admin` con roles, permisos, tenant editorial, catalogo, readiness y salud operativa.
- Bloque `Superadmin operations` con endpoint protegido `/api/v1/admin/operations`.
- Endpoints publisher/admin protegidos por `Authorization: Bearer demo-token:*`.
- Endpoints auth/admin: `/api/v1/auth/demo-users`, `/api/v1/auth/demo-login`, `/api/v1/admin/roles` y `/api/v1/admin/marketplace`.

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

- Tests en contenedor Python 3.11: pasan, 43 tests.
- Ruff en contenedor Python 3.11: pasa.
- `node --check src/storms_agents/web/static/app.js`: pasa.
- `make public-ready`: pasa.
- `BASE_URL=http://127.0.0.1:8088 make smoke`: pasa.
- Docker daemon: disponible tras abrir Docker Desktop.
- Docker build local: pasa.
- Smoke test contra contenedor local: pasa.
- Smoke local confirma respuesta espanola de Don Quijote con psicologia, memoria,
  citas separadas y consistencia `passed=true` para "Por que atacas los molinos?".
- Smoke test publico de Cloud Run: pasa.
- El contenedor arranca con `APP_ENV=demo` y sin reloader.
- Proyecto GCP del challenge creado: `stormsboys-agents-20260602`.
- Billing Pronexus enlazado.
- Budget guardrail de 50 EUR creado.
- Cloud Run desplegado: `https://stormsboys-agents-api-5mpmuf566a-uc.a.run.app`.
- Revision Cloud Run activa: `stormsboys-agents-api-00027-tsp`.
- Cloud Run usa service account nueva: `stormsboys-agents-runtime@stormsboys-agents-20260602.iam.gserviceaccount.com`.
- No hay claves JSON de usuario ni credenciales antiguas en el runtime.
- Cloud SQL instance: `stormsboys-pgvector`.
- Cloud SQL database: `stormsbooks`.
- Cloud SQL user: `storms_agent`.
- Secret: `stormsboys-database-url`.
- Cloud Run Job de schema: `stormsboys-storage-init`.
- `/api/v1/challenge/storage`: `configured=true`, `pgvector_ready=true`.
- `/api/v1/challenge/storage/demo-seed`: `seeded=true`, `bookId=don-quijote`, `sections=5`.
- Embeddings publicos confirmados: `mode=gemini-embedding`, `model=gemini-embedding-001`, `vertexai=true`.
- Traza publica confirmada: `RetrievalAgent` usa `retrieval.pgvector_search`.
- Chat publico confirmado: `CharacterAgent` usa `gemini-2.5-flash` y `NarrativeConsistencyAgent` pasa.
- Narration publico confirmado: `VoiceNarrationAgent`, SSML y `ready_for_tts=true`.
- Publisher publico confirmado: `PublisherInsightsAgent`, engagement y quality `100%`.
- Admin publico confirmado: login demo, tokens demo, roles `reader`, `author`, `publisher_admin`, `super_admin`, `judge_access`, tenant demo, catalogo y readiness Marketplace.
- Smoke test publico confirmado el 2026-06-03 contra revision `stormsboys-agents-api-00027-tsp`.
- Chat publico confirmado: Don Quijote responde en espanol con psicologia visible,
  memoria de sesion, consistencia `passed=true` y citas separadas sin IDs inline.
- Memoria publica confirmada: `/api/v1/demo/chat/memory` devuelve historial desde
  `provider=cloud-sql-postgresql` con eventos persistidos en `conversation_memory_events`.
- Guardrail canonico corregido: preguntas ancladas dentro de una escena, como
  "after the windmills", ya no se tratan como futuro fuera de canon; preguntas como
  "ten years after the ending" siguen bloqueadas en modo `CANON`.
- Modos publicos confirmados: `CANON` rechaza futuro como canon y `FICTION` crea `fictionBranch`.
- Idioma publico confirmado: English por defecto, Espanol seleccionable, API devuelve `language` y Don Quijote responde en espanol cuando `language=es`.
- Nota local: `.venv` usa Python 3.14 en este Mac y `pytest` puede quedarse colgado al arrancar importaciones de dependencias Google. Para validacion fiable usa Docker/Python 3.11, que coincide con Cloud Run.

## Mapa De Codigo

- `src/storms_agents/api/main.py`: FastAPI, endpoints y montaje web.
- `src/storms_agents/api/main.py`: tambien contiene login demo, usuarios demo y contratos de acceso por rol.
- `src/storms_agents/agents/root_agent.py`: agente raiz ADK.
- `src/storms_agents/agents/book_ingestion.py`: ingestion demo.
- `src/storms_agents/agents/literary_analysis.py`: analisis literario demo.
- `src/storms_agents/agents/retrieval.py`: retrieval demo.
- `src/storms_agents/agents/character.py`: respuesta de personaje.
- `src/storms_agents/agents/fiction_branch.py`: rama ficcional alternativa, separada del canon.
- `src/storms_agents/agents/scene_orchestrator.py`: escena multi-personaje.
- `src/storms_agents/agents/consistency.py`: validacion narrativa.
- `src/storms_agents/agents/narration.py`: plan de voz/narracion para TTS.
- `src/storms_agents/agents/publisher_insights.py`: informe publisher/admin.
- `src/storms_agents/api/main.py`: tambien expone contratos demo de roles y Marketplace admin.
- `src/storms_agents/evaluation.py`: before/after Track 2.
- `src/storms_agents/storage/repository.py`: contrato Cloud SQL/pgvector, schema,
  retrieval y memoria persistente.
- `src/storms_agents/memory.py`: store de memoria con Cloud SQL y fallback local.
- `src/storms_agents/storage/embedding.py`: proveedor de embeddings Vertex/Gemini con fallback determinista de 768 dimensiones.
- `src/storms_agents/tools/gemini.py`: adaptador Gemini con fallback demo.
- `src/storms_agents/web/index.html`: interfaz de jueces.
- `src/storms_agents/web/static/app.js`: logica frontend.
- `src/storms_agents/web/static/styles.css`: estilos.
- `infra/cloud-run/plan.sh`: imprime plan de despliegue sin crear recursos.
- `infra/cloud-run/deploy.sh`: despliegue protegido por `CONFIRM_DEPLOY=true`.
- `docs/cloud/04-pronexus-credit-setup.md`: estado de facturacion/credito.
- `docs/08-original-app-track3-analysis.md`: analisis de app original, Don Quijote, ADK y Track 3.
- `docs/product/04-original-product-model.md`: definicion real del producto, roles y modos canon/ficcion.
- `docs/track3/01-track3-marketplace-strategy.md`: estrategia Track 3 Marketplace/Gemini Enterprise.
- `docs/agents/04-platform-agent-operating-model.md`: agentes objetivo para reconstruir la app.
- `docs/adr/0004-track-3-platform-refactor.md`: decision formal de Track 3 principal.
- `docs/09-real-platform-implementation-plan.md`: orden de implementacion desde demo sintetica hacia plataforma real.
- `tests/test_api.py`: cobertura de endpoints.

## Endpoints

- `GET /`
- `GET /health`
- `GET /api/v1/challenge/readiness`
- `GET /api/v1/challenge/capabilities`
- `GET /api/v1/challenge/storage`
- `GET /api/v1/challenge/storage/demo-seed`
- `GET /.well-known/agent-card.json`
- `GET /a2a/agent-card.json`
- `GET /api/v1/demo/book`
- `POST /api/v1/demo/chat/character`
- `GET /api/v1/demo/chat/memory`
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

1. Reorientar UI/API desde libro sintetico hacia plataforma real con Don Quijote como caso demo.
2. Crear endpoint admin para limpiar sesiones demo antiguas si se generan muchas pruebas.
3. Ampliar persistencia de ramas ficcionales para mostrar timeline editable por usuario/publisher.
4. Crear agentes nuevos o adaptar los existentes segun `docs/agents/04-platform-agent-operating-model.md`.
5. Implementar publisher/admin como vista B2B Track 3, no solo panel decorativo.
6. Conectar Gemini tambien a LiteraryAnalysisAgent o SceneOrchestratorAgent con schemas estrictos.
7. Ampliar embeddings reales de Gemini a ingestion de libros subidos por usuario si se implementa upload completo.
8. Grabar video demo 1-2 minutos en ingles al final.

## Trabajo Seguro Para Otro Agente

Un agente puede trabajar en una de estas areas sin pisar a los demas:

- Gemini integration: conectar agentes concretos a `src/storms_agents/tools/gemini.py`.
- Product platform: modos canon/ficcion y roles segun `docs/product/04-original-product-model.md`.
- Track 3: agent card/A2A readiness y B2B docs segun `docs/track3`.
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
