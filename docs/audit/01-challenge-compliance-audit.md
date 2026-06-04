# Challenge Compliance Audit

Fecha: 2026-06-04.

## Resumen Ejecutivo

El proyecto esta en buen estado para demo tecnica: compila, pasa lint, pasa 50 tests en
Docker/Python 3.11, pasa `public-ready`, pasa smoke publico y esta desplegado en Cloud Run.

La base cumple una parte importante del challenge:

- Demo publica funcional en Cloud Run.
- Repositorio publico.
- Gemini/Vertex y Cloud SQL/pgvector documentados y verificados en runtime.
- Upload real de libros `.txt`, `.md` y PDF textual.
- Don Quijote como caso demo de dominio publico.
- Chat canon y ficcion separados.
- Memoria y ramas ficcionales persistentes cuando `DATABASE_URL` esta configurado.
- Roles demo: reader, author, publisher admin, super admin y judge access.
- Evaluacion Track 2 before/after con 12 casos.
- Agent card publica en `/.well-known/agent-card.json` y `/a2a/agent-card.json`.

La brecha principal no es que falte "todo", sino que hay una mezcla peligrosa entre:

1. Lo implementado de verdad.
2. Lo descrito como preparado o "ready".
3. Documentos antiguos que todavia hablan como si Track 2 fuese la estrategia principal.

Para competir mejor, hay que limpiar esa narrativa y reforzar tres cosas: ADK/A2A honestos,
demo de producto mas operable y fecha/video/submission.

## Validacion Ejecutada

```bash
make lint
make public-ready
docker run --rm --user root -v "$PWD:/app" -w /app stormsboys-agents-test \
  sh -c 'pip install --no-cache-dir -e ".[dev]" >/tmp/pip-dev.log && python -m pytest'
BASE_URL=https://stormsboys-agents-api-5mpmuf566a-uc.a.run.app make smoke
```

Resultado:

- Ruff: passed.
- Public-ready scan: passed.
- Tests Docker/Python 3.11: 50 passed.
- Public smoke: passed.

## Matriz Contra El Challenge

| Requisito | Estado | Evidencia | Riesgo |
| --- | --- | --- | --- |
| Code | Cumple | Repo publico y tests pasan | Bajo |
| Video 1-2 min en ingles | Pendiente | `docs/submission/05-devpost-fields-en.md` mantiene `TODO` para video | Alto |
| Architecture diagram | Cumple parcialmente | `docs/submission/architecture-diagram.mmd` existe | Medio si no se exporta/adjunta visualmente |
| Testing access | Cumple | Demo publica y `Judge Access` | Bajo |
| Technical Implementation 30% | Fuerte con matices | Cloud Run, Gemini, Cloud SQL, pgvector, agentes, trazas | Medio por ADK/A2A y evaluacion determinista |
| Business Case 30% | Fuerte | Publisher/admin, catalogo, B2B docs | Medio por metricas demo no basadas en uso real |
| Innovation 20% | Fuerte | Canon/ficcion, personaje con psicologia, escena, voz handoff | Medio por lector/voz todavia poco completos |
| Demo & Presentation 20% | Mejorando | Guided judge journey desplegado | Alto hasta grabar video y probar navegador limpio |
| Track 1 Build | Parcial | Capa nueva, upload, agentes | Medio si se presenta como track principal |
| Track 2 Optimize | Cumple demo | 12 casos before/after, guardrails, trazas | Medio porque la evaluacion fuerza fallback determinista |
| Track 3 Refactor | Cumple demo parcial | Cloud Run, Gemini, Cloud SQL, roles, agent card | Medio/alto si se afirma Marketplace/A2A listo |

## Hallazgos Prioritarios

### P0 - Falta El Video De Submission

El challenge exige video. `docs/submission/05-devpost-fields-en.md` todavia tiene
`TODO: add public demo video URL after recording`.

Impacto: sin video, la submission queda incompleta aunque la app funcione.

Accion:

- Grabar video final de 1-2 minutos en ingles.
- Usar el nuevo dashboard `Judge journey` como inicio.
- Actualizar `docs/submission/05-devpost-fields-en.md` con URL final.

### P0 - Fecha Limite Contradictoria En Demo Y PDF - Corregido En Codigo

El PDF descargado muestra arriba `Deadline: Jun 12, 2026 at 02:00am CEST`, pero el cuerpo
del PDF tambien dice `Projects are due by 5:00 PM PT on June 5th, 2026` y anuncia
`Submission Deadline Extended`.

El endpoint publico `/api/v1/challenge/submission` fue actualizado para devolver:

```json
"deadline": "2026-06-12 02:00 CEST (extended; verify in Devpost before final submit)"
```

Codigo: `src/storms_agents/api/main.py`, campo `deadline` en `challenge_submission`.

Impacto: un juez o agente puede ver una fecha antigua dentro de la demo.

Accion restante:

- Verificar la fecha final real en Devpost justo antes de enviar.

### P1 - Root ADK Agent Todavia Dice Track 2 - Corregido

`src/storms_agents/agents/root_agent.py` devuelve:

```python
"track": "Track 2 - Optimize Existing Agents"
```

Pero el proyecto actual declara Track 3 principal y una demo integrada Track 1/2/3.

Corregido: `describe_submission_scope()` ahora declara Track 3 como track principal
y Track 1/2 como evidencia de soporte. Hay test de regresion.

### P1 - Documentacion Antigua Sigue Diciendo "Priorizar Track 2" - Corregido

Ejemplos:

- `docs/03-official-guide-mapping.md`: "Priorizar Track 2".
- `docs/07-agent-continuation-prompt.md`: "Mantén la entrega alineada con Track 2".
- `docs/cloud/01-target-architecture.md`: "alineada con Track 2".
- `docs/adr/0001-track-2.md`: ADR aceptada sin nota de superacion por ADR 0004.

Corregido: ADR 0001 queda superada por ADR 0004, y los documentos de continuidad,
mapping oficial y arquitectura cloud ya dicen Track 3 principal con Track 1/2 como
evidencia tecnica.

### P1 - A2A/MCP Se Promete Mas Fuerte De Lo Que Esta Implementado

Corregido parcialmente: el endpoint de submission ya no declara `MCP/A2A-ready contracts`;
ahora habla de agent card A2A-ready y contratos HTTP JSON. La realidad implementada sigue
siendo agent card publica y HTTP JSON; no hay protocolo A2A completo ni MCP tool server
funcional dentro del repo.

Impacto: riesgo de sobrepromesa en Track 1/3.

Accion:

- Cambiar copy a "A2A-ready agent card and HTTP JSON interface" cuando sea preciso.
- Documentar explicitamente "not full A2A runtime yet".
- Si queda tiempo: crear un endpoint interoperable minimo mas cercano a A2A real, o una
  seccion de docs con contrato de invocacion por agente.

### P1 - Login Demo Devuelve Reader Si El User ID Es Invalido - Corregido

`auth_demo_login` busca el usuario y si no existe cae a `_demo_users()[0]`.

Corregido: un `user_id` inexistente devuelve `401 Invalid demo user.` y hay test de
regresion.

### P1 - El Producto Es Operable, Pero No Todavia "App Real Completa"

Hay vistas y endpoints para roles, upload, admin, publisher y lector, pero varios elementos son
demo o readiness:

- No hay registro real de usuarios.
- No hay Identity Platform real.
- No hay gestion real de disponibilidad/publicacion mas alla de `ready_for_review`.
- No hay progreso de lectura/favoritos.
- Voz produce SSML, no audio reproducible.
- Publisher metrics son sinteticas/evaluacion, no agregadas de uso real.

Impacto: para Track 3, hay que venderlo como Marketplace-ready refactor demo, no como producto
Marketplace ya publicado.

Accion:

- Mantener honestidad en submission.
- Priorizar una pequena mejora de publisher/admin: evento de uso real o contador de chats por
  libro/sesion si hay tiempo.

### P2 - Evaluacion Track 2 Es Determinista, No Online Con Gemini

`run_demo_evaluation()` fuerza `GeminiTool(Settings(google_api_key=None, google_cloud_project=None))`
para usar fallback demo.

Impacto: es reproducible y estable, pero no demuestra directamente evaluacion live de Vertex/Gemini.

Accion:

- Documentar en UI/API que es deterministic evaluation harness.
- Opcional: agregar un endpoint/flag de evaluacion live para 2-3 casos, con coste controlado.

### P2 - Analisis De Libros Subidos Es Heuristico, No Gemini Real - Corregido

Corregido: `LiteraryAnalysisAgent` usa Gemini como primera via para analizar libros subidos
cuando Gemini/Vertex esta configurado. El agente pide JSON estricto, valida el contrato y cae a
heuristica local si Gemini no esta configurado, falla o devuelve JSON invalido.

Verificado en Cloud Run: `The Glass Observatory` genero personajes mediante
`LiteraryAnalysisAgent` con `model=gemini-2.5-flash`, guardo el libro en Cloud SQL y
permitio chat canonico con `liora` usando `retrieval.pgvector_search`.

### P2 - Reader No Es Todavia Un Lector Completo - Corregido Para Demo

Corregido para demo: la vista Reader ahora incluye catalogo navegable, Don Quijote como
titulo demo, libros subidos visibles cuando el usuario autenticado los tiene disponibles,
secciones/paginas de lectura desde `readingSections`, resumen/escenas/lugares, progreso
persistido via backend `reader_events` con fallback local, notas/favoritos por seccion y
CTA directo a chat. El chat web envia `book_id: state.currentBookId`, por lo que hablar con
personajes queda anclado al libro activo.

Corregido para demo: el panel Admin/Marketplace ya muestra un tablero editorial
`ENGAGEMENT BOARD` con `reader_signals`, `section_signals`, `character_signals`,
estado de readiness y siguiente accion de negocio por titulo. Don Quijote aparece
con senales reales persistidas en Cloud SQL y drill-down por seccion/personaje.
Tambien existe export JSON protegido `/api/v1/admin/marketplace/export` para
Publisher/Admin con catalogo, readiness, senales y totales.

Impacto: el producto se entiende, pero el usuario puede sentir que falta aplicacion lectora.

Accion:

- Probar el boton de export en navegador limpio antes de grabar el video.

### P2 - Idioma Espanol Existe En Chat/UI, Pero No En Todo El Producto

La UI principal tiene selector `English/Espanol` y chat respeta `language=en|es`. Sin embargo,
las respuestas de admin/publisher/evaluation vienen en ingles desde API y el upload no traduce
analisis ni resumen.

Impacto: cumple requisito demo bilingue basico, pero no producto bilingue integral.

Accion:

- Mantener ingles como primary para judges.
- Documentar "Spanish supported for reader/character experience".
- Si hay tiempo, traducir strings dinamicos clave de publisher/admin en frontend.

## Backlog Recomendado Antes De Enviar

1. Grabar video de 1-2 minutos en ingles.
2. Verificar deadline en Devpost en vivo antes de enviar.
3. Ajustar lenguaje A2A/MCP para no sobreprometer.
4. Exportar o adjuntar arquitectura como imagen si Devpost no acepta Mermaid.
5. Probar demo desde navegador limpio con `Judge Access`.
6. Opcional fuerte: agregar descarga CSV adicional si el video necesita mostrar archivo.
7. Opcional fuerte: agregar metrica real de interacciones por libro para Publisher.

## Veredicto

Estado actual: **demo publica tecnicamente solida, con P0/P1 narrativos principales corregidos
salvo video final y verificacion live del deadline**.

La submission puede ser competitiva si se corrigen los P0/P1. Sin esas correcciones, el riesgo no
es tecnico basico, sino de confianza: el proyecto dice "ADK/A2A/All tracks/Marketplace" en varios
sitios, pero algunos archivos todavia dicen Track 2 y algunas afirmaciones son readiness, no runtime
completo.
