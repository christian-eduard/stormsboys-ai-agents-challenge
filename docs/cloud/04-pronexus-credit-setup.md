# Pronexus Credit Setup

## Estado

Configuracion inicial completada el 2026-06-02.

## Billing Account

- Nombre: Pronexus.
- Billing account: `019D4C-395BD4-294B6A`.
- Estado: abierta.

## Proyecto Nuevo Del Challenge

- Project ID: `stormsboys-agents-20260602`.
- Project number: `425710112361`.
- Nombre: `Stormsboys AI Agents Challenge`.
- Billing: enlazado a Pronexus.
- Region operativa inicial: `us-central1`.

## Por Que Proyecto Nuevo

El credito del challenge debe usarse en un entorno aislado. No se deben mezclar recursos, codigo, configuracion ni facturacion operativa con proyectos anteriores.

## APIs Activadas

- Cloud Run: `run.googleapis.com`.
- Artifact Registry: `artifactregistry.googleapis.com`.
- Cloud Build: `cloudbuild.googleapis.com`.
- Secret Manager: `secretmanager.googleapis.com`.
- Vertex AI / Gemini: `aiplatform.googleapis.com`.
- Billing Budgets: `billingbudgets.googleapis.com`.
- Cloud SQL Admin: `sqladmin.googleapis.com`.

## Budget Guardrail

- Nombre: `Stormsboys Challenge Guardrail`.
- Budget ID: `f0cd0823-31a8-4464-a431-01026102449c`.
- Importe: `50 EUR`.
- Scope: solo proyecto `stormsboys-agents-20260602`.
- Tratamiento de creditos: `EXCLUDE_ALL_CREDITS`.
- Alertas: 25%, 50%, 75%, 90%, 100%.

## Cloud Run Demo

- Service: `stormsboys-agents-api`.
- Region: `us-central1`.
- Revision: `stormsboys-agents-api-00035-rjd`.
- Runtime service account: `stormsboys-agents-runtime@stormsboys-agents-20260602.iam.gserviceaccount.com`.
- URL canonica: `https://stormsboys-agents-api-5mpmuf566a-uc.a.run.app`.
- URL alternativa: `https://stormsboys-agents-api-425710112361.us-central1.run.app`.
- Trafico: 100% a la revision `stormsboys-agents-api-00035-rjd`.
- Ultimo image digest desplegado:
  `sha256:5b65c101ec453f163bf3b540644fb24bfcff937806d29b183f8e5275e0ca6652`.
- Smoke test publico: pasa el 2026-06-04.
- Upload publico: pasa el 2026-06-04 con manuscrito textual, catalogo y chat por `book_id`.
- Admin publico confirmado: login demo, tokens demo protegidos, roles, catalogo, tenant demo y readiness Marketplace.
- Idioma publico confirmado: `language=en` y `language=es` en chat de personaje.
- Character Agent usa Gemini/Vertex real con identidad gestionada y fallback seguro.
- Cloud Run monta Cloud SQL via `run.googleapis.com/cloudsql-instances`.
- Demo web incluye panel `Runtime proof` para mostrar a jueces Gemini, Cloud SQL/pgvector, seed y traza de retrieval.
- Demo web incluye paneles `Voice / Narration Agent` y `Publisher Insights Agent`.
- Demo web incluye panel `History` para ensenar memoria conversacional persistida por sesion/personaje/modo.
- Demo web incluye panel `Fiction timeline` para ensenar ramas alternativas persistidas
  y separadas del canon.
- Demo web incluye formulario protegido de subida en `Author Workspace` para libros propios,
  de editorial o de dominio publico.
- Demo web incluye `Judge journey` en el dashboard con ruta clara de upload, analisis
  de agentes, lector, ficcion, publisher value y Cloud proof para los tres tracks.

## Cloud SQL / pgvector

- Instance: `stormsboys-pgvector`.
- Connection name: `stormsboys-agents-20260602:us-central1:stormsboys-pgvector`.
- Database version: `POSTGRES_16`.
- Edition: `ENTERPRISE`.
- Tier: `db-f1-micro`.
- Region/zona: `us-central1-a`.
- Estado: `RUNNABLE`.
- Database: `stormsbooks`.
- User: `storms_agent`.
- Secret Manager: `stormsboys-database-url`.
- Runtime env: `DATABASE_URL` desde Secret Manager.
- Schema inicializado por Cloud Run Job: `stormsboys-storage-init`.
- Endpoint de verificacion: `/api/v1/challenge/storage`.
- Estado verificado: `configured=true`, `provider=cloud-sql-postgresql`, `pgvector_ready=true`.
- Endpoint de seed: `/api/v1/challenge/storage/demo-seed`.
- Seed verificado: `seeded=true`, `bookId=don-quijote`, `sections=5`.
- Retrieval verificado: traza `retrieval.pgvector_search`.
- Chat publico verificado: `CharacterAgent` usa `gemini-2.5-flash` y consistencia pasa.
- Chat publico verificado: Don Quijote responde en espanol con psicologia visible,
  memoria de sesion y citas separadas del texto.
- Memoria persistente verificada: `conversation_memory_events` existe en Cloud SQL y
  `/api/v1/demo/chat/memory` devuelve eventos desde `provider=cloud-sql-postgresql`.
- Ramas ficcionales persistentes verificadas: `fiction_branches` existe en Cloud SQL y
  `/api/v1/demo/fiction/branches` devuelve continuidad, citas canon y proveedor
  `cloud-sql-postgresql`; `/api/v1/demo/fiction/branches/{branch_id}` devuelve el detalle
  de una rama concreta.
- Timeline de ficcion verificado en UI publica contra revision
  `stormsboys-agents-api-00034-wkj`: cada rama se expande con premisa, continuacion,
  memoria/psicologia aprendida y anclajes canonicos.
- Cleanup superadmin verificado: `DELETE /api/v1/admin/demo-sessions/{session_id}`
  borra solo memoria conversacional y ramas ficcionales de la sesion indicada.
- Cleanup UI verificado: el formulario de `Superadmin operations` aparece en la demo publica
  y queda habilitado para `Judge Access`.
- Guardrail canonico verificado: preguntas ancladas en la escena de los molinos responden
  con voz de Don Quijote; futuro fuera del libro sigue bloqueado en modo `CANON`.
- Narration publico verificado: `VoiceNarrationAgent`, SSML y `ready_for_tts=true`.
- Publisher publico verificado: `PublisherInsightsAgent`, engagement y quality `100%`.
- Embeddings verificados: `gemini-embedding-001` via Vertex AI, 768 dimensiones.
- Fallback de embeddings: `demo-hash-embedding-768` solo si Vertex/API no esta configurado o falla.
- Upload verificado: `uploaded_books` registra metadatos y analisis JSONB; las secciones
  subidas se guardan en `book_sections` con embeddings y se consultan por `book_id`.
- Upload smoke publico: `The Orchard of Mirrors` creo
  `book_id=upload-the-orchard-of-mirrors-46f285dceb`, `character_id=elena`,
  catalogo visible para `author-demo` y chat canonico con citas de secciones subidas.
- Tabla de memoria: `conversation_memory_events`.
- Tabla de ramas ficcionales: `fiction_branches`.
- Tabla de libros subidos: `uploaded_books`.
- Fallback de memoria: proceso local solo si `DATABASE_URL` no esta configurado o Cloud SQL falla.

## Credenciales

- No hay claves JSON nuevas.
- La service account nueva solo muestra una clave `SYSTEM_MANAGED`.
- No se usan credenciales antiguas para el runtime.
- Cloud Run usa una service account nueva y dedicada.
- Gemini/Vertex se configura por identidad gestionada:
  - `GOOGLE_GENAI_USE_VERTEXAI=true`.
  - `GOOGLE_CLOUD_PROJECT=stormsboys-agents-20260602`.
  - `GOOGLE_CLOUD_LOCATION=us-central1`.
  - `GEMINI_MODEL=gemini-2.5-flash`.
  - `GEMINI_EMBEDDING_MODEL=gemini-embedding-001`.

## Service Account Nueva

- Email: `stormsboys-agents-runtime@stormsboys-agents-20260602.iam.gserviceaccount.com`.
- Rol concedido: `roles/aiplatform.user`.
- Rol concedido: `roles/cloudsql.client`.
- Secret access concedido solo a `stormsboys-database-url`.
- Uso: runtime de Cloud Run y llamadas a Gemini/Vertex.
- Sin claves de usuario creadas.

## Comandos De Verificacion

```bash
gcloud billing projects describe stormsboys-agents-20260602
gcloud services list --enabled --project=stormsboys-agents-20260602
gcloud billing budgets list --billing-account=019D4C-395BD4-294B6A --project=stormsboys-agents-20260602
gcloud run services describe stormsboys-agents-api --region=us-central1 --project=stormsboys-agents-20260602
gcloud sql instances describe stormsboys-pgvector --project=stormsboys-agents-20260602
curl -s https://stormsboys-agents-api-5mpmuf566a-uc.a.run.app/api/v1/challenge/storage
curl -s https://stormsboys-agents-api-5mpmuf566a-uc.a.run.app/api/v1/challenge/storage/demo-seed
curl -s "https://stormsboys-agents-api-5mpmuf566a-uc.a.run.app/api/v1/demo/chat/memory?session_id=judge-demo-session&character_id=don_quijote&mode=CANON"
curl -s "https://stormsboys-agents-api-5mpmuf566a-uc.a.run.app/api/v1/demo/fiction/branches?session_id=judge-demo-session&character_id=don_quijote"
curl -s "https://stormsboys-agents-api-5mpmuf566a-uc.a.run.app/api/v1/demo/fiction/branches/BRANCH_ID?session_id=judge-demo-session"
curl -s "https://stormsboys-agents-api-5mpmuf566a-uc.a.run.app/api/v1/books/catalog" -H "Authorization: Bearer demo-token:author-demo"
curl -s -X DELETE "https://stormsboys-agents-api-5mpmuf566a-uc.a.run.app/api/v1/admin/demo-sessions/example-session" -H "Authorization: Bearer demo-token:superadmin-demo"
gcloud iam service-accounts keys list --iam-account=stormsboys-agents-runtime@stormsboys-agents-20260602.iam.gserviceaccount.com --project=stormsboys-agents-20260602
BASE_URL=https://stormsboys-agents-api-5mpmuf566a-uc.a.run.app make smoke
```

## Politica De Coste

- Cloud SQL ya esta creado para la demo del challenge; apagar/eliminar cuando termine si no se usa.
- Priorizar Cloud Run con escalado a cero.
- Usar dataset demo pequeno.
- Mantener budget bajo para evitar consumo accidental.
- Revisar billing antes y despues de despliegues.
