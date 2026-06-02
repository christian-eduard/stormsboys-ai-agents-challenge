# Plan Before / After Para Track 2

## Objetivo

La guia recomienda que Track 2 muestre claramente como el agente optimizado resuelve escenarios que antes fallaban o se atascaban.

## Baseline

Sistema simple:

- Prompt directo.
- Sin retrieval fuerte.
- Sin validador de contradicciones.
- Sin trazas visibles.
- Sin memoria estructurada.

## Optimized

Sistema optimizado:

- Retrieval Agent.
- Character Agent.
- Narrative Consistency Agent.
- Scene Orchestrator.
- Memoria.
- Observabilidad.
- Evaluacion.

## Caso 1: Pregunta Fuera De Canon

Pregunta:

"Cuéntame que ocurre con este personaje diez anos despues del final."

Baseline probable:

- Inventa continuacion.

Optimized:

- Reconoce limite del canon.
- Puede responder especulativamente solo si lo etiqueta como imaginacion.

## Caso 2: Personaje No Deberia Saber Algo

Pregunta:

"Por que traicionaste al protagonista si todavia no lo sabes en este capitulo?"

Baseline probable:

- Responde con informacion futura.

Optimized:

- Usa contexto de escena.
- Evita conocimiento fuera de momento narrativo.

## Caso 3: Grupo Con Conflicto

Pregunta:

"Discutid quien tiene la culpa."

Baseline probable:

- Respuesta homogenea, todos suenan igual.

Optimized:

- Voces diferenciadas.
- Turnos coordinados.
- Emociones distintas.

## Caso 4: Pregunta Sin Evidencia

Pregunta:

"Que dice el libro sobre un lugar que no aparece?"

Baseline probable:

- Alucinacion.

Optimized:

- Dice que no hay evidencia en el texto recuperado.

## Uso En Video

Mostrar solo uno o dos casos para no saturar. El resto queda en documentacion y evaluacion.
