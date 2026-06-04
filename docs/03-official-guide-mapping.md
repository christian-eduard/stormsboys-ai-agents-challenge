# Mapeo Contra La Guia Oficial

Fuente usada: `ai_agents_challenge_designed_guide.pdf` de Google for Startups.

## Track 2 Segun La Guia

La guia describe Track 2 como optimizacion de agentes existentes para pasar de prototipo funcional a fiabilidad real. Los focos principales son:

- Stress-testing de razonamiento multi-step.
- Debug de logica bloqueada o ambigua.
- Refinamiento de instrucciones de sistema.
- Agent Simulation.
- Agent Evaluation.
- Agent Observability.
- Gestion de estado con Sessions, Runtime y Memory Bank.
- Despliegue en Agent Runtime o infraestructura gestionada en Google Cloud.
- Grounding/Custom RAG.
- Demo con comparacion antes/despues.

## Traduccion A Nuestro Proyecto

| Requisito guia | Respuesta en Stormsboys |
| --- | --- |
| Existing agents | Personajes, escenas, analisis literario y RAG ya existen como comportamiento de referencia. |
| Multi-step reasoning | Upload -> analisis -> embeddings -> retrieval -> respuesta -> validacion -> memoria. |
| Stress testing | Dataset de prompts narrativos, factual, emocional, out-of-canon y multi-personaje. |
| Observability | Trazas por agente, latencia, tokens, contexto recuperado y estado final. |
| Evaluation | Baseline vs optimized con metricas de coherencia, relevancia, personalidad y grounding. |
| Managed runtime | Cloud Run primero; Agent Runtime se evaluara si encaja en tiempo y complejidad. |
| State and memory | Memoria de conversacion, afinidad, estado emocional y resumen relacional. |
| Grounding/RAG | pgvector/Cloud SQL y/o Agent Search Data Stores si se incorpora en fase Cloud. |
| Before/after demo | Mostrar fallo o debilidad baseline y luego sistema optimizado resolviendo el caso. |

## Implicaciones

- No basta con mostrar una app bonita.
- Hay que mostrar ingenieria de agentes.
- La demo debe ensenar evaluacion y observabilidad, aunque sea de forma compacta.
- La arquitectura debe explicar por que es production-ready.

## Decisiones Para La Entrega

- Presentar Track 3 como historia principal: refactor cloud-native, B2B, roles,
  Marketplace/Gemini Enterprise readiness y runtime Google Cloud.
- Usar Track 2 como evidencia de calidad: evaluacion before/after, grounding,
  guardrails, memoria separada y trazas.
- Usar Track 1 como evidencia secundaria de build: nueva capa agentica, upload,
  agentes literarios y contratos HTTP/agent card.
- Usar Cloud Run como camino rapido y honesto.
- Incluir ADK real donde exista y documentar con precision lo que sea
  "agent-compatible" o "A2A-ready", sin prometer Agent Runtime/A2A completo si
  no queda implementado.

## Riesgo Principal

Si solo presentamos "chat con personajes", puede parecer una app de consumo. Si presentamos "sistema multi-agente observable y evaluable para convertir libros en experiencias interactivas", encaja mucho mejor con el reto.
