# Challenge Brief

## Objetivo Del Reto

Construir o mejorar un sistema de agentes de IA usando tecnologias de Google Cloud y Gemini. La entrega debe demostrar valor de negocio, implementacion tecnica, creatividad y una demo clara.

## Track Principal

Track 3: Refactor for Google Cloud Marketplace & Gemini Enterprise.

Elegimos este track porque Stormsboys Libros IA ya tiene una base funcional: analisis de libros, conversaciones con personajes, RAG, memoria, voz, dashboard, roles de lector/publisher/admin y flujos de lectura. La oportunidad competitiva esta en refactorizar esa base hacia un producto cloud-native, B2B y preparado para Google Cloud Marketplace/Gemini Enterprise.

## Evidencia Secundaria Track 2

Track 2 sigue siendo una pieza de soporte. Lo usaremos para demostrar que la plataforma trata la calidad de agentes como disciplina de ingenieria:

- Evaluacion baseline vs optimizada.
- Guardrails de canon.
- Stress tests de razonamiento multi-paso.
- Separacion de modo canon y modo ficcion.
- Trazas y metricas.

## Interpretacion Practica

Para este proyecto, "refactor for marketplace" significa:

- Formalizar la logica actual como agentes con responsabilidades separadas.
- Convertir el MVP en una plataforma B2B para editoriales y catalogos.
- Mejorar la arquitectura para Cloud Run, Cloud SQL/pgvector, Gemini y Secret Manager.
- Preparar ADK/A2A o documentar honestamente la capa compatible.
- Medir calidad, coherencia, latencia, coste y recuperacion de contexto.
- Crear trazas y evaluaciones reproducibles.
- Mostrar una demo funcional de producto real.

## Tecnologias Objetivo

- Gemini API.
- Google Cloud Run.
- Cloud SQL for PostgreSQL con pgvector, o alternativa compatible.
- ADK o capa de agentes compatible con el ecosistema Google.
- Observabilidad con logs estructurados y trazas por paso.
- RAG con embeddings y grounding documentado.

## Entregables

- Codigo.
- Repositorio de codigo publico.
- Descripcion en ingles con arquitectura.
- Diagrama de arquitectura incluido.
- Video demo de 1-2 minutos en ingles.
- Demo funcional accesible para los jueces.
- Documentacion tecnica y de negocio.

## Criterios Que Debemos Cubrir

- Technical Implementation: 30%. Arquitectura real, agentes, RAG, despliegue, observabilidad.
- Business Case: 30%. Valor para lectores, autores y publishers.
- Innovation & Creativity: 20%. Personajes vivos, modo canon, modo ficcion, escenas conversacionales, memoria narrativa.
- Demo & Presentation: 20%. Demo clara, emocional y tecnicamente creible.

## Elegibilidad Y Restricciones

- Espana es elegible.
- El proyecto debe crearse durante el periodo del concurso.
- El repositorio publico no debe incluir secretos, datos privados ni codigo arrastrado sin revisar.
- La demo debe estar accesible para los jueces con instrucciones simples.

## Decision

No vamos a presentar el proyecto como una app generica de libros. Lo vamos a presentar como una plataforma de inteligencia literaria multi-agente.
