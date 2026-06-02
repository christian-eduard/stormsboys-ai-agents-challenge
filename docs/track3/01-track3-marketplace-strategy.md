# Estrategia Track 3

## Decision

El proyecto debe presentarse principalmente como Track 3: Refactor for Google Cloud Marketplace & Gemini Enterprise.

Track 2 sigue siendo util como evidencia secundaria de calidad porque podemos demostrar evaluacion before/after, RAG, guardrails y mejoras de fiabilidad. Pero la historia principal del producto es Track 3: una aplicacion existente de agentes literarios se refactoriza hacia una arquitectura cloud-native, escalable y vendible.

## Por Que Track 3

La app original ya contiene un producto funcional:

- Upload y analisis de libros.
- Personajes generados por IA.
- Conversaciones con personajes.
- RAG con embeddings.
- Chat de escenas, lugares y grupos.
- Voz/narracion.
- Roles de lector, publisher y admin.
- Analitica editorial.

Eso no es un agente net-new. Tampoco es solo optimizacion de prompts. Es un MVP que puede convertirse en producto B2B para editoriales, educacion y plataformas de lectura.

## Producto B2B

La oferta para Marketplace/Gemini Enterprise:

Stormsboys Literary Agent Platform convierte catalogos editoriales en experiencias interactivas con agentes de personajes, lectura asistida, narracion y analitica de engagement.

Clientes objetivo:

- Editoriales.
- Plataformas educativas.
- Bibliotecas digitales.
- Autores con catalogo propio.
- Clubes de lectura y formacion.

## Requisitos Track 3 Mapeados

### B2B Focus

El producto resuelve un problema empresarial: aumentar engagement, monetizar catalogos y obtener analitica narrativa sobre libros digitales.

### Cloud-Native Runtime

Arquitectura objetivo:

- Cloud Run para API/web.
- Cloud SQL PostgreSQL + pgvector.
- Secret Manager.
- Cloud Logging.
- Artifact Registry.
- Service account dedicada.

### Vertex-Powered Intelligence

Modelo objetivo:

- Gemini 2.5 Flash para analisis, chat y evaluacion.
- `gemini-embedding-001` para embeddings.
- Vertex AI como runtime gestionado cuando aplique.

### A2A Interoperability

Objetivo minimo:

- Publicar agent card.
- Exponer capacidades de ingestion, character chat, canon guardrail, fiction branch y publisher insights.
- Preparar puente A2A con ADK cuando el tiempo lo permita.

### Marketplace Readiness

El proyecto debe documentar:

- Caso de negocio.
- Arquitectura.
- Seguridad.
- Roles y permisos de operacion.
- Tenant editorial y catalogo gestionable.
- Cost control.
- Testing access.
- Operacion.
- Public repo.
- Demo accesible.

Estado demo implementado:

- `/api/v1/auth/demo-users`: cuentas de prueba para `reader`, `author`, `publisher_admin`, `super_admin` y `judge_access`.
- `/api/v1/auth/demo-login`: login demo y token local para jueces.
- `/api/v1/admin/roles`: matriz de roles `reader`, `author`, `publisher_admin`, `super_admin`, `judge_access`.
- `/api/v1/admin/marketplace`: tenant demo, catalogo, readiness Marketplace y metricas de operacion; requiere token demo con `manage_catalog` o `manage_tenants`.
- `/api/v1/demo/publisher`: insights publisher protegidos por token demo.
- UI `Testing access`: pantalla inicial con cuentas demo y entrada dedicada `Judge Access`.
- UI `Role dashboard`: cada cuenta ve acciones y navegacion filtradas por su rol.
- UI `Marketplace Admin`: consola visible para jueces con roles, permisos y catalogo editorial
  bloqueado/activado segun rol.
- Produccion objetivo: Cloud Identity / Identity Platform con RBAC por tenant.

## Demo De 1-2 Minutos

La demo debe contar esto:

1. Una editorial o autor sube Don Quijote o selecciona el libro demo.
2. Gemini analiza la obra y genera personajes con perfil psicologico.
3. El lector abre el libro.
4. Habla con Don Quijote en modo canon.
5. Cambia a modo ficcion y crea una variante narrativa.
6. Entra Sancho o una escena grupal.
7. Se prepara voz/narracion.
8. El publisher ve engagement, calidad y catalogo.
9. El superadmin ve roles, permisos, tenant, readiness y salud operativa.
10. Se muestra arquitectura Google Cloud.

## Evidencia Tecnica

Para puntuar fuerte:

- Endpoint funcional publico.
- Cloud Run real.
- Cloud SQL/pgvector real.
- Gemini/Vertex real.
- Evaluacion reproducible.
- Trazas por agente.
- Separacion canon/ficcion.
- Documentacion clara en ingles para Devpost.

## Riesgos

- No prometer A2A completo si solo hay agent card.
- No vender como ADK real si solo existe una capa compatible.
- No arrastrar deuda de la app original.
- No mezclar credenciales antiguas.
- No presentar Don Quijote como producto unico.

## Frase Para Submission

Stormsboys refactors an existing AI-powered reading platform into a Google Cloud-native literary agent system for publishers, where every book becomes a governed multi-agent experience with canon-safe conversations, fiction branches, voice narration, and engagement analytics powered by Gemini.
