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

- Priorizar Track 2.
- Usar Cloud Run como camino rapido.
- Incluir ADK o una capa Agent-compatible claramente documentada.
- Preparar un dataset pequeno pero convincente.
- Evitar prometer Agent Runtime si no queda implementado.

## Riesgo Principal

Si solo presentamos "chat con personajes", puede parecer una app de consumo. Si presentamos "sistema multi-agente observable y evaluable para convertir libros en experiencias interactivas", encaja mucho mejor con el reto.
