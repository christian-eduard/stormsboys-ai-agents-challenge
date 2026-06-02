# Work Packages Para Agentes Paralelos

## Objetivo

Permitir que varios agentes trabajen en paralelo sin pisarse ni duplicar decisiones.

## Reglas Generales

- Cada agente debe tomar un paquete concreto.
- Cada agente debe leer `AGENTS.md`, `docs/00-challenge-brief.md` y el documento de su area.
- Cada agente debe dejar notas de decision si cambia arquitectura.
- Un agente no debe modificar areas fuera de su paquete salvo que lo documente.

## Paquete A: Product & Demo

Responsabilidad:

- Guion de demo.
- Narrativa Devpost.
- Testing access.
- Lista de assets.
- Capturas necesarias.

Archivos principales:

- `docs/product`
- `docs/demo`

Entregables:

- Guion final de video.
- Checklist de grabacion.
- Texto de submission.

## Paquete B: Agent Layer

Responsabilidad:

- Diseno e implementacion de agentes.
- Contratos de entrada/salida.
- Herramientas internas.
- Trazas de razonamiento operativo.

Archivos principales:

- `docs/agents`
- `src/agents`
- `src/tools`

Entregables:

- Agentes implementados.
- Schemas.
- Pruebas unitarias.

## Paquete C: Backend API

Responsabilidad:

- API limpia para demo.
- Auth demo.
- Books.
- Conversations.
- Publisher/admin.

Archivos principales:

- `src/api`
- `src/server`
- `tests/api`

Entregables:

- Health check.
- Endpoints de demo.
- OpenAPI actualizado.

## Paquete D: Frontend Demo

Responsabilidad:

- UI demo.
- Upload.
- Reader.
- Character chat.
- Group/scene chat.
- Dashboard publisher.

Archivos principales:

- `src/web`
- `tests/e2e`

Entregables:

- Demo estable.
- Estados de carga/error.
- Flujo listo para video.

## Paquete E: Cloud & Infra

Responsabilidad:

- Cloud Run.
- Cloud SQL.
- Secret Manager.
- Storage.
- Comandos reproducibles.

Archivos principales:

- `docs/cloud`
- `infra`
- `scripts`

Entregables:

- Plan de despliegue.
- Scripts seguros.
- Coste estimado.

## Paquete F: Evaluation

Responsabilidad:

- Dataset de prompts.
- Baseline.
- Sistema optimizado.
- Reporte comparativo.
- Metricas.

Archivos principales:

- `docs/evaluation`
- `tests/evaluation`

Entregables:

- Casos de evaluacion.
- Resultados reproducibles.
- Graficas o tabla para demo.

## Paquete G: Security & Release

Responsabilidad:

- Limpieza de secretos.
- `.gitignore`.
- Politicas de logging.
- Revision pre-publicacion.

Archivos principales:

- `docs/security`
- raiz del proyecto

Entregables:

- Checklist de seguridad.
- Revision de secretos.
- Release checklist.
