# Especificacion De Observabilidad

## Objetivo

Cada interaccion importante debe poder explicarse despues: que agente actuo, que contexto uso, cuanto tardo, que modelo llamo y si paso validacion.

## Evento Base

```json
{
  "traceId": "trace_123",
  "spanId": "span_456",
  "agent": "CharacterAgent",
  "operation": "generate_reply",
  "bookId": "don-quijote",
  "conversationId": "conv_123",
  "model": "gemini",
  "status": "success",
  "latencyMs": 1234,
  "inputTokens": 1200,
  "outputTokens": 300,
  "retrievedSections": 4,
  "validation": {
    "schema": "passed",
    "canonConsistency": "passed"
  }
}
```

## Spans Minimos

- `book.ingest`.
- `book.analyze`.
- `embedding.generate`.
- `retrieval.search`.
- `retrieval.rerank`.
- `character.generate_reply`.
- `scene.orchestrate`.
- `consistency.check`.
- `memory.update`.
- `voice.generate`.

## Reglas

- Usar `traceId` comun por accion del usuario.
- No loguear claves.
- No loguear libro completo.
- Permitir modo demo con detalles ampliados.
- Permitir modo privado con redaccion de texto sensible.

## Visualizacion Para Demo

La demo debe mostrar una vista simple:

- Agente ejecutado.
- Paso actual.
- Tiempo.
- Contexto recuperado.
- Resultado de validacion.

No hace falta crear un sistema de observabilidad complejo para la primera version; una tabla de trazas por conversacion es suficiente si es clara.
