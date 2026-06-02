# Arquitectura De Agentes

## Objetivo

Convertir la logica actual en agentes explicitos, observables y evaluables. No queremos un unico prompt gigante. Queremos una capa modular donde cada agente tenga responsabilidad, entrada, salida, herramientas y metricas.

## Agentes Propuestos

### Book Ingestion Agent

Responsabilidad:

- Recibir libro.
- Normalizar texto.
- Dividir contenido en secciones.
- Preparar metadatos iniciales.

Salida:

- Texto limpio.
- Estructura base.
- Chunks listos para embeddings.

### Literary Analysis Agent

Responsabilidad:

- Extraer sinopsis.
- Detectar personajes.
- Detectar lugares.
- Detectar capitulos o escenas.
- Crear resumen narrativo.

Salida:

- `BookAnalysis`.
- `CharacterProfile[]`.
- `PlaceProfile[]`.
- `SceneProfile[]`.

### Embedding And Retrieval Agent

Responsabilidad:

- Generar embeddings.
- Indexar secciones.
- Recuperar contexto relevante.
- Reordenar resultados.

Salida:

- Contexto RAG citado y limitado.

### Character Agent

Responsabilidad:

- Responder como un personaje concreto.
- Mantener voz, memoria y coherencia.
- Evitar spoilers si aplica.

Entrada:

- Mensaje del lector.
- Perfil del personaje.
- Contexto RAG.
- Estado emocional.
- Memoria relacional.

### Scene Orchestrator Agent

Responsabilidad:

- Coordinar varios personajes.
- Decidir quien responde.
- Mantener coherencia de escena.
- Evitar contradicciones entre agentes.

### Narrative Consistency Agent

Responsabilidad:

- Detectar contradicciones.
- Evaluar canon vs invencion.
- Pedir regeneracion si la respuesta falla.

### Voice/Narration Agent

Responsabilidad:

- Convertir respuesta o escena en audio.
- Seleccionar voz segun personaje.
- Mantener proveedor bien identificado.

### Publisher Insights Agent

Responsabilidad:

- Resumir actividad.
- Detectar personajes mas consultados.
- Generar insights de engagement.

## Orquestacion

La version del challenge debe exponer un flujo observable:

1. User action.
2. Agent selected.
3. Tools called.
4. Context retrieved.
5. Gemini response.
6. Validation.
7. Final response.
8. Metrics emitted.

## Decision ADK

La direccion preferida es incluir una capa ADK minima para formalizar agentes y herramientas. Si ADK introduce riesgo de tiempo, se documentara una capa compatible con contratos claros y se priorizara Cloud Run + Gemini + evaluacion.
