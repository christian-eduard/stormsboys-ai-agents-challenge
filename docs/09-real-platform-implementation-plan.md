# Plan De Implementacion De Plataforma Real

Este plan reemplaza la idea de seguir ampliando una demo sintetica. La direccion correcta es reconstruir, dentro del proyecto nuevo del challenge, una version limpia y demostrable de la app original.

## Objetivo

Tener una app funcional para jueces que demuestre:

- Upload o seleccion de libro.
- Analisis Gemini.
- Personajes con psicologia.
- Lector.
- Chat canon.
- Chat ficcion.
- Escena/grupo.
- Voz/narracion.
- Publisher dashboard.
- Superadmin/platform dashboard.
- Arquitectura Track 3 sobre Google Cloud.

## Principios De Implementacion

- No copiar el repo original.
- Reusar conocimiento, no deuda.
- Mantener contratos simples y testeables.
- Cada flujo debe verse en la demo.
- Don Quijote es el primer libro real.
- El modo canon y ficcion deben estar separados desde el modelo.

## Fase 1: Base Real De Libro

Meta: sustituir la identidad sintetica de la demo por una base real de producto.

Entregables:

- `DEMO_BOOK_ID=don-quijote`.
- Titulo y autor reales.
- Chunks representativos de Don Quijote.
- Personajes: Don Quijote, Sancho Panza, Dulcinea, narrador/ventero si aplica.
- Lugares: La Mancha, El Toboso, campo de molinos, venta.
- Escenas: lectura de libros de caballeria, salida, molinos, dialogo con Sancho.
- Evaluacion adaptada a Don Quijote.
- UI actualizada a producto de libros, no a cuento inventado.

Validacion:

- Tests pasan.
- Smoke local pasa.
- Smoke Cloud Run pasa tras deploy.

## Fase 2: Contrato Canon/Ficcion

Meta: implementar la diferencia central del producto.

Entregables:

- [x] Enum `ConversationMode`: `CANON`, `FICTION`.
- [x] Endpoint de chat acepta modo.
- [ ] Historial persistente separado por modo.
- [x] Respuesta canon usa retrieval y consistency.
- [x] Respuesta ficcion crea rama narrativa separada en la respuesta API.
- [x] UI tiene selector visible Canon/Ficcion.
- Evaluacion incluye casos de separacion.

Validacion:

- Una pregunta fuera de canon no contamina canon.
- Una escena alternativa se guarda como ficcion.
- El personaje mantiene personalidad en ambos modos.

Estado actual: la separacion existe en API/UI y tests, pero la memoria persistente de ramas
ficcionales todavia no esta guardada en base de datos.

## Fase 3: Modelo Publisher/Admin

Meta: reforzar Track 3 B2B.

Entregables:

- Dashboard publisher con catalogo.
- Metricas: lecturas, chats canon, chats ficcion, personajes mas activos, escenas mas activas.
- Vista superadmin con usuarios, libros, estado de agentes, salud y costes estimados.
- Documentar permisos.

Validacion:

- La demo puede mostrar valor para editorial.
- No se requieren secretos ni login complejo para jueces.

## Fase 4: ADK/A2A Readiness

Meta: demostrar refactor hacia ecosistema Google Cloud.

Entregables:

- Agent card o endpoint equivalente.
- Capabilities por agente.
- Documentacion de ADK real vs capa compatible.
- Si el tiempo permite, puente ADK/A2A minimo.

Validacion:

- El endpoint de capabilities expone Track 3.
- La documentacion no promete mas de lo implementado.

## Fase 5: Submission

Meta: preparar entrega.

Entregables:

- Descripcion en ingles.
- Diagrama de arquitectura actualizado.
- Repo publico limpio.
- Testing access.
- Video 1-2 minutos en ingles.

Validacion:

- `make test`
- `make lint`
- `make public-ready`
- smoke publico.

## Orden De Trabajo Para Agentes Paralelos

1. Agente Producto: actualizar narrativa, demo script y Devpost.
2. Agente Backend: implementar modelo canon/ficcion y libro Don Quijote.
3. Agente Frontend: adaptar UI a plataforma real y selector de modo.
4. Agente Evaluation: adaptar dataset y pruebas a Don Quijote/canon/ficcion.
5. Agente Track 3: agent card, A2A readiness y docs B2B.
6. Agente Cloud: deploy, smoke y coste.

## Criterio De Exito

La demo debe hacer evidente que:

- Es una plataforma, no un chatbot.
- Usa Google Cloud de verdad.
- Usa Gemini de verdad.
- Tiene negocio B2B para editoriales.
- Tiene innovacion en modos canon/ficcion.
- Puede explicarse en menos de 2 minutos.
