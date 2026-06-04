# Handoff Para Continuar El Proyecto

Este archivo es el punto de entrada para cualquier agente nuevo. Si solo tienes tiempo para leer una cosa, lee esto.

## Contexto

Estamos creando un proyecto nuevo, aislado y autocontenido para el Google for Startups AI Agents Challenge.

- Estrategia de entrega: demostrar los tres tracks del challenge en un producto unico.
- Track 1 - Build: nueva capa agentica ADK-first y flujo real de upload/analisis.
- Track 2 - Optimize: evaluacion before/after, grounding, guardrails, memoria y trazas.
- Track 3 - Refactor: Cloud Run, Gemini/Vertex, Cloud SQL pgvector, roles B2B, A2A card y Marketplace readiness.
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
- Ramas ficcionales persistentes en Cloud SQL cuando `DATABASE_URL` esta configurado:
  tabla `fiction_branches`, endpoint `/api/v1/demo/fiction/branches`, endpoint de detalle
  `/api/v1/demo/fiction/branches/{branch_id}` y panel web `Fiction timeline` con ramas
  expandibles. En local cae a memoria de proceso.
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
- Upload real de libros desde vista `Author` y API `POST /api/v1/books/upload`.
- Analisis de libros subidos es Gemini-first cuando Vertex/Gemini esta configurado:
  `LiteraryAnalysisAgent` pide JSON estricto, valida personajes/psicologia y cae a
  heuristica local si el modelo no esta disponible o devuelve JSON invalido.
- Catalogo real `GET /api/v1/books/catalog` que combina Don Quijote demo y libros subidos por tenant/usuario.
- Detalle de libro subido `GET /api/v1/books/{book_id}` con analisis, personajes, escenas y lugares.
- Chat de personaje acepta `book_id`, por lo que puede conversar contra Don Quijote o contra un libro subido.
- Vista `Reader` con catalogo navegable, libro activo, secciones/paginas de lectura,
  anotaciones/favoritos, progreso de lectura, persistencia backend via `reader_events`
  con fallback local y CTA directo a agentes.
- El chat web envia `book_id: state.currentBookId`; al subir o seleccionar un libro,
  los personajes y la conversacion se anclan al libro activo.
- Consola web `Marketplace Admin` con roles, permisos, tenant editorial, catalogo, readiness y salud operativa.
- Bloque `Superadmin operations` con endpoint protegido `/api/v1/admin/operations`.
- Endpoints publisher/admin protegidos por `Authorization: Bearer demo-token:*`.
- Endpoints auth/admin: `/api/v1/auth/demo-users`, `/api/v1/auth/demo-login`, `/api/v1/admin/roles` y `/api/v1/admin/marketplace`.
- Endpoint superadmin para limpiar solo memoria/rama de una sesion demo:
  `DELETE /api/v1/admin/demo-sessions/{session_id}`.
- Endpoint publisher/admin para export CSV:
  `GET /api/v1/admin/marketplace/export.csv`.
- Contrato honesto de interoperabilidad agentica:
  `docs/track3/02-agent-interoperability-contract.md`.
- Diagrama visual listo para adjuntar en Devpost:
  `docs/submission/architecture-diagram.svg`.

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

- Tests en contenedor Python 3.11: pasan, 57 tests.
- Ruff en contenedor Python 3.11: pasa.
- `node --check src/storms_agents/web/static/app.js`: pasa.
- `make public-ready`: pasa.
- Verificacion local Browser contra `http://127.0.0.1:8090`: login `Judge Access`,
  vista Reader muestra catalogo, progreso y Don Quijote; CTA `Talk now` abre `Agents`
  con personajes cargados.
- Verificacion local Browser contra `http://127.0.0.1:8091`: Reader muestra
  `Section 1 / 4`, permite avanzar a `Section 2 / 4`, actualiza progreso a `50%`
  y guarda una nota local visible en `readerNoteList`.
- API local verificada contra `http://127.0.0.1:8092`: `POST /api/v1/reader/progress`,
  `POST /api/v1/reader/notes` y `GET /api/v1/reader/notes` funcionan con token demo.
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
- Revision Cloud Run activa: `stormsboys-agents-api-00044-dqc`.
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
- Smoke test publico confirmado el 2026-06-04 contra revision `stormsboys-agents-api-00036-6g9`.
- Smoke test publico confirmado el 2026-06-04 contra revision `stormsboys-agents-api-00037-vtk`.
- Smoke test publico confirmado el 2026-06-04 contra revision `stormsboys-agents-api-00038-2ps`.
- Smoke test publico confirmado el 2026-06-04 contra revision `stormsboys-agents-api-00039-r6d`.
- Smoke test publico confirmado el 2026-06-04 contra revision `stormsboys-agents-api-00040-pqp`.
- Smoke test publico confirmado el 2026-06-04 contra revision `stormsboys-agents-api-00041-rq9`.
- Smoke test publico confirmado el 2026-06-05 contra revision `stormsboys-agents-api-00042-m5h`.
- Smoke test publico confirmado el 2026-06-05 contra revision `stormsboys-agents-api-00044-dqc`.
- Compliance publico confirmado el 2026-06-04 contra revision `stormsboys-agents-api-00036-6g9`:
  `/api/v1/challenge/submission` muestra deadline extendido `2026-06-12 02:00 CEST`,
  evidencia A2A honesta como agent card/HTTP JSON, y login demo invalido devuelve
  `401 Invalid demo user`.
- UI publica confirmada el 2026-06-04: sidebar muestra Build, Optimize y Refactor;
  vista Reader tiene hero de producto, CTAs para chat/upload/publisher y carga
  Don Quijote correctamente.
- UI publica confirmada el 2026-06-04 contra revision `stormsboys-agents-api-00038-2ps`:
  Reader sirve catalogo navegable, progreso local, panel de lectura y CTA `Talk now`;
  el chat web envia el `book_id` del libro activo.
- UI/API publica confirmada el 2026-06-04 contra revision `stormsboys-agents-api-00039-r6d`:
  Reader sirve controles anterior/siguiente, notas/favoritos locales y
  `/api/v1/demo/book` devuelve `readingSections` desde Cloud SQL.
- API publica confirmada el 2026-06-04 contra revision `stormsboys-agents-api-00040-pqp`:
  `POST /api/v1/reader/progress`, `POST /api/v1/reader/notes` y
  `GET /api/v1/reader/notes` persisten en Cloud SQL; `/api/v1/admin/marketplace`
  devuelve `operations.readerEngagement` para `don-quijote`.
- UI/API publica confirmada el 2026-06-04 contra revision `stormsboys-agents-api-00041-rq9`:
  Admin muestra `ENGAGEMENT BOARD`, 4 titulos del catalogo, Don Quijote con
  `reader_signals` reales y accion editorial `Package as a premium discussion title`.
- API publica confirmada el 2026-06-05 contra revision `stormsboys-agents-api-00042-m5h`:
  `/api/v1/admin/marketplace` devuelve `section_signals` para `quijote-section-2`
  con progreso, notas y lectores agregados desde Cloud SQL.
- API publica confirmada el 2026-06-05 contra revision `stormsboys-agents-api-00044-dqc`:
  `/api/v1/admin/marketplace` devuelve `character_signals` para Don Quijote,
  agregados por `book_id`, `character_id` y modo desde `conversation_memory_events`.
- API/UI publica confirmada el 2026-06-05 contra revision `stormsboys-agents-api-00045-ll9`:
  `/api/v1/admin/marketplace/export` devuelve paquete JSON protegido para
  Publisher/Admin con readiness, catalogo, `reader_signals`, `section_signals`,
  `character_signals`, totales de exportacion y operaciones. La UI Admin incluye
  boton bilingue `Export insights` / `Exportar insights`.
- API/UI publica confirmada el 2026-06-05 contra revision `stormsboys-agents-api-00046-x72`:
  `/api/v1/admin/marketplace/export.csv` devuelve CSV protegido para
  Publisher/Admin, bloquea Reader con 403 y la UI Admin incluye boton
  `Download CSV` / `Descargar CSV`.
- UI publica confirmada el 2026-06-04 contra revision `stormsboys-agents-api-00035-rjd`:
  dashboard incluye `Judge journey`, 6 pasos de demo, 3 proof cards para Track 1/2/3,
  CTA de upload, sin claves i18n crudas y sin overflow horizontal.
- Upload publico confirmado el 2026-06-04: `POST /api/v1/books/upload` subio
  `The Orchard of Mirrors`, creo `book_id=upload-the-orchard-of-mirrors-46f285dceb`,
  lo guardo en `provider=cloud-sql-postgresql`, lo mostro en catalogo y permitio chat
  canonico con `character_id=elena`.
- Upload publico Gemini-first confirmado el 2026-06-04 contra revision
  `stormsboys-agents-api-00037-vtk`: `The Glass Observatory` creo
  `book_id=upload-the-glass-observatory-c0e5a3d03f`, `LiteraryAnalysisAgent`
  uso `model=gemini-2.5-flash`, genero personajes `liora`, `mateo` y
  `liora_s_mother`, guardo en `provider=cloud-sql-postgresql` y permitio chat
  canonico con `liora` usando `retrieval.pgvector_search`.
- Chat publico confirmado: Don Quijote responde en espanol con psicologia visible,
  memoria de sesion, consistencia `passed=true` y citas separadas sin IDs inline.
- Memoria publica confirmada: `/api/v1/demo/chat/memory` devuelve historial desde
  `provider=cloud-sql-postgresql` con eventos persistidos en `conversation_memory_events`.
- Ramas ficcionales publicas confirmadas: una llamada `FICTION` crea `fictionBranch`,
  `/api/v1/demo/fiction/branches` devuelve `provider=cloud-sql-postgresql`, continuidad,
  citas canon separadas y `consistency.passed=true`.
- UI publica verificada: `Fiction timeline` abre cada rama con `<details>` nativo y muestra
  premisa, continuacion, memoria/psicologia aprendida y anclajes canonicos sin depender de
  JavaScript asincrono.
- Cleanup publico confirmado: `DELETE /api/v1/admin/demo-sessions/{session_id}` con
  `superadmin-demo` borra solo `conversation_memory_events` y `fiction_branches` para una
  sesion temporal; despues historial y ramas devuelven listas vacias.
- UI publica confirmada: el panel Admin expone un formulario protegido para ejecutar cleanup
  por `session_id`; Judge Access lo ve habilitado.
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
- `src/storms_agents/agents/literary_analysis.py`: analisis literario demo y analisis
  Gemini-first de manuscritos subidos con fallback heuristico.
- `src/storms_agents/agents/retrieval.py`: retrieval demo.
- `src/storms_agents/agents/character.py`: respuesta de personaje.
- `src/storms_agents/agents/fiction_branch.py`: rama ficcional alternativa, separada del canon.
- `src/storms_agents/fiction_history.py`: store de ramas ficcionales con Cloud SQL y fallback local.
- `src/storms_agents/agents/scene_orchestrator.py`: escena multi-personaje.
- `src/storms_agents/agents/consistency.py`: validacion narrativa.
- `src/storms_agents/agents/narration.py`: plan de voz/narracion para TTS.
- `src/storms_agents/agents/publisher_insights.py`: informe publisher/admin.
- `src/storms_agents/api/main.py`: tambien expone contratos demo de roles y Marketplace admin.
- `src/storms_agents/evaluation.py`: before/after Track 2.
- `src/storms_agents/storage/repository.py`: contrato Cloud SQL/pgvector, schema,
  retrieval, memoria persistente y tabla `uploaded_books`.
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
- `POST /api/v1/books/upload`
- `GET /api/v1/books/catalog`
- `GET /api/v1/books/{book_id}`
- `POST /api/v1/reader/progress`
- `GET /api/v1/reader/progress`
- `POST /api/v1/reader/notes`
- `GET /api/v1/reader/notes`
- `GET /api/v1/demo/book`
- `POST /api/v1/demo/chat/character`
- `GET /api/v1/demo/chat/memory`
- `GET /api/v1/demo/fiction/branches`
- `GET /api/v1/demo/fiction/branches/{branch_id}`
- `DELETE /api/v1/admin/demo-sessions/{session_id}`
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

Estado UI publica 2026-06-05 01:23 CEST:

- Redisenio premium desplegado en Cloud Run revision `stormsboys-agents-api-00047-6vk`.
- Imagen desplegada: `sha256:29162aa1498f9e65a9befc94f219559d9bdf5ea66c780eb71d461e349d0dd011`.
- Smoke publico pasado contra `https://stormsboys-agents-api-5mpmuf566a-uc.a.run.app`.
- QA visual publica con `Judge Access`: portada de producto, lector, selector ingles/espanol,
  Don Quijote y Sancho visibles, sin overflow horizontal en desktop.

## Prioridades Siguientes

1. Preparar datos demo con Don Quijote y al menos un libro subido desde la UI antes de grabar.
2. Convertir el timeline ficcional en una vista editable por usuario/publisher.
3. Pulir Publisher para visualizar mejor las senales `reader_events`.
4. Grabar video demo 1-2 minutos en ingles al final.
5. Verificar manualmente el estado de Devpost si se va a enviar desde una cuenta autenticada.

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
