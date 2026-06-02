# Plan De Evaluacion

## Objetivo

Demostrar que el sistema de agentes mejora calidad, coherencia y utilidad frente a una conversacion directa sin orquestacion.

## Metricas Principales

- Coherencia canonica: la respuesta respeta el libro.
- Relevancia: responde a la pregunta del lector.
- Uso de contexto: utiliza fragmentos recuperados cuando corresponde.
- Personalidad: mantiene voz del personaje.
- Seguridad narrativa: evita inventar hechos incompatibles.
- Latencia: tiempo total y por agente.
- Coste estimado: tokens y llamadas por flujo.

## Casos De Evaluacion

### Individual Character Chat

- Pregunta factual sobre el libro.
- Pregunta emocional al personaje.
- Pregunta con riesgo de spoiler.
- Pregunta fuera del canon.

### Group Scene Chat

- Varios personajes con conflicto.
- Pregunta que requiere turnos coordinados.
- Escena donde un personaje no deberia saber cierta informacion.

### Retrieval

- Pregunta con contexto literal en una seccion.
- Pregunta con contexto distribuido en varias secciones.
- Pregunta sin respuesta en el libro.

## Comparacion

Baseline:

- Prompt unico sin RAG fuerte.
- Sin validador de contradicciones.
- Sin memoria estructurada.

Optimized:

- Retrieval Agent.
- Character Agent.
- Scene Orchestrator.
- Narrative Consistency Agent.
- Trazas y evaluacion.

## Resultado Esperado

La submission debe mostrar que el sistema optimizado:

- Responde con mas fidelidad.
- Reduce contradicciones.
- Mantiene mejor la voz de personaje.
- Explica mejor sus fuentes internas.
- Es observable y desplegable.

## Estado Implementado

La API ya expone `GET /api/v1/demo/evaluation` con:

- 12 casos de evaluacion.
- Summary baseline vs optimized.
- Riesgo por caso.
- Improvement rate.

Riesgos cubiertos:

- `hallucination`.
- `ungrounded_answer`.
- `wrong_voice`.
- `temporal_leak`.
- `missing_evidence`.
- `multi_step_reasoning`.

## Siguiente Mejora Opcional

Conectar Gemini real al evaluador automatico si queremos una evaluacion generativa adicional:

- Baseline: respuesta directa sin retrieval/consistency.
- Optimized: pipeline con Retrieval Agent, Character Agent y Narrative Consistency Agent.
