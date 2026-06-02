# Critical Path

## Objetivo

Llegar a una submission completa con el menor riesgo posible.

## Ahora Mismo

Tenemos una demo funcional desplegada en Cloud Run. La submission tecnica esta muy cerca; el mayor riesgo restante es presentacion: repo publico, video en ingles y Devpost final.

Avance ya completado:

- API funcional.
- Demo web funcional.
- Docker build y contenedor local funcionales.
- Gemini adapter central con fallback.
- Character Agent usa Gemini/Vertex real y conserva guardrail determinista.
- Evaluacion Track 2 de 12 casos.
- Voice/Narration Agent implementado.
- Publisher Insights Agent implementado.
- Proyecto GCP nuevo creado y enlazado a billing Pronexus.
- Budget guardrail de 50 EUR creado.
- Cloud Run desplegado con service account nueva y sin claves JSON de usuario.
- Cloud SQL PostgreSQL + pgvector activo.
- Embeddings `gemini-embedding-001` via Vertex AI activos.
- Smoke test publico de Cloud Run funcional.

## Orden Recomendado

### 1. Submission

- Completar `docs/submission/01-devpost-description-en.md`.
- Completar `docs/submission/02-testing-access-en.md`.
- Crear README publico final.
- Grabar video 1-2 minutos.

### 2. Repo Publico

- Elegir licencia.
- Confirmar que no hay secretos.
- Crear repo publico.
- Subir solo este proyecto nuevo.

### 3. Demo Final

- Probar URL desde navegador limpio.
- Ejecutar smoke publico.
- Grabar video con prompts prevalidos.
- Pegar URL demo y repo en Devpost.

### 4. Mejoras Opcionales

- Conectar Gemini al LiteraryAnalysisAgent.
- Generar audio real con Google Cloud Text-to-Speech.
- Anadir upload controlado de libro.

## Cosas Que No Hacer Todavia

- No complicar con GKE.
- No meter autenticacion compleja.
- No portar codigo externo.
- No hacer features que no puntuen en los cuatro criterios.
