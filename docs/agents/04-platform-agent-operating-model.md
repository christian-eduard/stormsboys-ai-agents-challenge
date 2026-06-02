# Modelo Operativo De Agentes

Este documento define los agentes que debe tener la nueva version del challenge. La app original contiene logica agentica, pero el proyecto nuevo debe expresarla con modulos limpios, trazables y preparados para ADK/A2A.

## Principio

Cada libro se convierte en un sistema de agentes. El usuario no habla con un chatbot generico: interactua con agentes literarios especializados que comparten memoria, recuperacion semantica y reglas de canon.

## Agentes Principales

### Book Ingestion Agent

Responsabilidad:

- Recibir libro.
- Extraer texto.
- Validar metadatos.
- Normalizar contenido.
- Crear tarea de analisis.

Entrada:

- Archivo PDF/TXT.
- Titulo.
- Autor.
- Genero.
- Owner.
- Derechos declarados.

Salida:

- `book_id`.
- Estado `PROCESSING`.
- Texto normalizado.

### Literary Analysis Agent

Responsabilidad:

- Analizar la obra.
- Extraer sinopsis.
- Extraer personajes.
- Extraer lugares.
- Extraer escenas/capitulos.
- Producir contexto literario.

Salida:

- `BookAnalysis`.
- `CharacterProfile[]`.
- `PlaceProfile[]`.
- `SceneProfile[]`.

### Character Forge Agent

Responsabilidad:

- Convertir personajes extraidos en agentes conversacionales.
- Crear personalidad operativa.
- Definir estilo de habla.
- Calcular rasgos OCEAN.
- Definir restricciones.
- Preparar voz.

Salida:

- `CharacterAgentProfile`.

### Retrieval Agent

Responsabilidad:

- Dividir libro en chunks.
- Generar embeddings.
- Consultar pgvector.
- Devolver fragmentos relevantes con puntuacion.

Regla:

- Ninguna respuesta canon debe generarse sin contexto recuperado o sin admitir falta de evidencia.

### Canon Conversation Agent

Responsabilidad:

- Responder como personaje dentro del canon.
- Usar RAG.
- Usar personalidad.
- Usar memoria de relacion.
- No inventar hechos contradictorios.

Salida:

- Respuesta.
- Pensamiento interno opcional para demo.
- Estado emocional.
- Citas o secciones usadas.
- Score de confianza.

### Fiction Branch Agent

Responsabilidad:

- Crear y continuar ramas narrativas alternativas.
- Mantener identidad del personaje.
- Separar ficcion de canon.
- Guardar evolucion narrativa.
- Producir material reutilizable.

Reglas:

- Debe declarar que opera en modo ficcion.
- Debe mantener trazabilidad con el libro base.
- No debe contaminar el estado canon.

### Scene Orchestrator Agent

Responsabilidad:

- Coordinar varios personajes en una escena.
- Decidir quien responde.
- Mantener voces diferenciadas.
- Usar contexto de escena/capitulo.

### Group Conversation Agent

Responsabilidad:

- Gestionar salas con varios personajes.
- Mantener memoria grupal.
- Actualizar estado emocional por participante.
- Preservar interacciones entre personajes.

### Voice/Narration Agent

Responsabilidad:

- Preparar texto para TTS.
- Seleccionar voz o estilo.
- Crear SSML/transcript cuando aplique.
- Integrarse con Gemini TTS o proveedor final documentado.

### Publisher Insights Agent

Responsabilidad:

- Resumir engagement.
- Identificar personajes/escenas mas activos.
- Informar calidad y riesgos.
- Recomendar acciones editoriales.

### Platform Admin Agent

Responsabilidad:

- Ayudar al superadmin a entender estado de usuarios, libros, agentes, costes y errores.
- No ejecutar acciones destructivas sin confirmacion.

## Modos

### CANON

Usa:

- Retrieval Agent.
- Canon Conversation Agent.
- Narrative Consistency Agent.

No permite:

- Cambiar hechos.
- Crear finales nuevos como canon.
- Responder sin evidencia cuando el usuario pregunta por hechos del libro.

### FICTION

Usa:

- Retrieval Agent.
- Fiction Branch Agent.
- Scene/Group agents si aplica.

Permite:

- Nuevos eventos.
- Nuevos escenarios.
- Continuaciones alternativas.

Obliga:

- Guardar rama.
- Separar memoria.
- Mantener personalidad.

## Estados De Conversacion

Toda conversacion debe guardar:

- `conversation_id`.
- `book_id`.
- `user_id`.
- `mode`.
- `character_id` o `scene_id`.
- Mensajes.
- Memoria de relacion.
- Estado emocional.
- Contexto evolucionado.
- Citas de retrieval.

## Evaluacion

Los tests deben cubrir:

- Respuesta canon con evidencia.
- Rechazo o redireccion ante preguntas sin evidencia.
- Cambio correcto a modo ficcion.
- Separacion de memoria canon/ficcion.
- Voz consistente de personaje.
- Escena multi-personaje con voces diferenciadas.
- Publisher insights con metricas reales o simuladas.

## Preparacion ADK/A2A

Cada agente debe poder describirse con:

- Nombre.
- Objetivo.
- Entradas.
- Salidas.
- Herramientas.
- Restricciones.
- Metricas.

Esto permite migrar a ADK real y publicar capacidades via A2A sin reescribir el producto.
