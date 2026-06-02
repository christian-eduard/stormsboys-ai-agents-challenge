# Contratos De Agentes

## Principio

Cada agente debe tener contrato de entrada/salida. Las respuestas libres de Gemini se validan con schemas antes de llegar al usuario.

## Tipos Base

```ts
type AgentTrace = {
  traceId: string;
  userId?: string;
  bookId: string;
  agentName: string;
  startedAt: string;
  finishedAt?: string;
  model: string;
  inputTokens?: number;
  outputTokens?: number;
  latencyMs?: number;
  status: "success" | "retry" | "failed";
};
```

```ts
type RetrievedContext = {
  sectionId: string;
  bookId: string;
  text: string;
  score: number;
  source: "book_section" | "scene" | "character_profile" | "publisher_note";
};
```

```ts
type CharacterReply = {
  characterId: string;
  characterName: string;
  thought?: string;
  response: string;
  emotionalState?: string;
  citations: string[];
  confidence: number;
};
```

## Reglas

- Ningun agente debe devolver datos al usuario sin validacion.
- Ningun agente debe acceder a secretos.
- Toda respuesta de personaje debe indicar contexto utilizado internamente.
- Las trazas no deben guardar texto sensible completo si el usuario marca el libro como privado.

## Pendiente

- Definir schemas finales en codigo.
- Decidir libreria de validacion.
- Decidir formato de trazas para observabilidad.
