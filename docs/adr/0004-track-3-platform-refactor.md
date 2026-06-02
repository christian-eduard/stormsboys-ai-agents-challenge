# ADR 0004: Track 3 Como Direccion Principal

## Estado

Aceptado.

## Fecha

2026-06-02.

## Contexto

El proyecto empezo orientado a Track 2 con una demo sintetica. Tras analizar la aplicacion original de libros, queda claro que el producto real es mas amplio: una plataforma donde usuarios y editoriales suben libros, Gemini analiza la obra, se crean agentes de personajes, se habilitan modos canon/ficcion, lectura, voz, escenas, grupos, publisher analytics y superadmin.

El challenge ofrece Track 3 para refactorizar agentes existentes hacia Google Cloud Marketplace y Gemini Enterprise. Este encaje es mas fuerte que presentar una demo de un libro aislado.

## Decision

El proyecto se orienta principalmente a Track 3:

- Refactorizar una plataforma existente de lectura agentica.
- Crear una arquitectura cloud-native sobre Google Cloud.
- Usar Gemini/Vertex, Cloud Run y Cloud SQL/pgvector.
- Preparar capa ADK/A2A o documentar honestamente el nivel implementado.
- Mantener evaluacion Track 2 como evidencia secundaria de calidad.

## Consecuencias

- Don Quijote sera libro demo, no el producto completo.
- La documentacion debe hablar de plataforma, roles y catalogos.
- El codigo nuevo debe separar canon y ficcion.
- La UI debe mostrar lector, personajes, modo canon, modo ficcion, escena/grupo, voz y publisher/admin.
- El backend debe prepararse para roles: lector, publisher y superadmin.
- No se copiara deuda tecnica de la app original.

## No Objetivos

- No migrar todo el repo original literalmente.
- No prometer marketplace publicado.
- No prometer A2A completo si no esta implementado.
- No reutilizar credenciales antiguas.

## Validacion

La decision se considera correcta si la submission puede explicar claramente:

- Caso B2B para editoriales.
- Arquitectura Google Cloud.
- Gemini como inteligencia central.
- Agentes diferenciados.
- Demo funcional.
- Evaluacion de calidad.
