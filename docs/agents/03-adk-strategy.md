# Estrategia ADK / Agent Layer

## Objetivo

Cumplir el espiritu del challenge: agentes reales, no solo endpoints con prompts.

## Opcion Preferida

Crear una capa de agentes compatible con ADK y evaluar integracion minima con ADK si el tiempo lo permite.

## Por Que No Empezar Copiando Todo

Los proyectos previos pueden tener funciones utiles, pero no deben copiarse directamente. Si copiamos sin diseno, heredamos:

- Prompts grandes.
- Mezcla de responsabilidades.
- Nombres legacy.
- Validacion dispersa.
- Dificultad para observar cada paso.

## Capa Propuesta

```txt
src/agents
  book-ingestion
  literary-analysis
  retrieval
  character
  scene-orchestrator
  consistency
  voice
  publisher-insights

src/tools
  gemini
  vector-store
  book-storage
  memory-store
  voice-provider
  observability
```

## Criterio Para Usar ADK

Usaremos ADK si:

- Permite avanzar rapido.
- No bloquea la demo.
- Nos da estructura clara de agents/tools/sessions.
- Puede desplegarse o explicarse con Google Cloud de forma honesta.

## Fallback Aceptable

Si ADK retrasa demasiado, crearemos una capa propia `AgentRunner` con contratos equivalentes:

- `Agent`.
- `Tool`.
- `Session`.
- `Memory`.
- `Trace`.
- `Evaluation`.

Y documentaremos como se puede migrar a ADK/Agent Runtime tras la demo.

## Regla De Honestidad

No se dira que usamos ADK o Agent Runtime si no esta implementado. La submission puede decir "Agent-compatible layer on Cloud Run" si esa es la realidad final.
