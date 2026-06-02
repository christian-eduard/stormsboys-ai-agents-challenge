# Dataset De Evaluacion

## Objetivo

Crear prompts repetibles para medir el sistema antes y despues de la optimizacion.

## Formato

```json
{
  "id": "character-factual-001",
  "bookId": "don-quijote",
  "agent": "CharacterAgent",
  "input": "Pregunta del usuario",
  "expectedBehavior": "Que debe ocurrir",
  "failureModes": ["hallucination", "spoiler", "wrong_voice"],
  "metrics": ["canon_consistency", "relevance", "persona"]
}
```

## Casos Implementados En Codigo

Archivo fuente: `src/storms_agents/evaluation.py`.

Casos actuales:

- `out-of-canon-001`: riesgo de alucinacion de futuro canonico.
- `grounding-001`: respuesta sin grounding.
- `persona-001`: perdida de voz/persona.
- `scene-knowledge-001`: filtracion temporal de informacion.
- `retrieval-failure-001`: pregunta sin evidencia en el libro.
- `multi-step-001`: razonamiento sobre conflicto entre motivaciones.
- `squire-voice-001`: voz practica de Sancho Panza.
- `forbidden-volume-001`: warning del volumen prohibido sin profecia extra.
- `unsupported-place-001`: pregunta sobre palacio no presente en el libro.
- `power-memory-001`: razonamiento sobre memoria y poder.
- `spanish-out-of-canon-001`: guardrail canonico en espanol.
- `scene-conflict-001`: conflicto de escena con motivos diferenciados.

## Resultado Actual

- Total: 12 casos.
- Baseline: 6/12.
- Optimized: 12/12.
- Improvement rate: 0.5.
- Endpoint: `/api/v1/demo/evaluation`.

## Casos Iniciales Documentados

### Factual

Pregunta:

"Que sabes sobre el lugar donde empezo todo?"

Esperado:

- Usar contexto del libro.
- Responder desde conocimiento del personaje.
- No inventar detalles externos.

### Emotional

Pregunta:

"Como te sentiste cuando ocurrio esa escena?"

Esperado:

- Mantener voz del personaje.
- Mostrar emocion coherente.
- No romper la cuarta pared.

### Out Of Canon

Pregunta:

"Dime algo que pasa despues del final."

Esperado:

- No inventar canon.
- Responder con cautela narrativa.

### Group Conflict

Pregunta:

"Discutid entre vosotros quien tomo la peor decision."

Esperado:

- Respuestas diferenciadas.
- Conflicto controlado.
- Coherencia de relaciones.

### Retrieval Failure

Pregunta:

"Que dice el libro sobre una ciudad que nunca aparece?"

Esperado:

- Reconocer falta de evidencia.
- No alucinar.

## Pendiente

- Crear evaluator con Gemini como judge opcional.
- Guardar resultados baseline vs optimized en Cloud SQL.
- Ampliar a 16-20 prompts si sobra tiempo.
