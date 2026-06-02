# Plan De Despliegue

## Estado

Despliegue real completado en `stormsboys-agents-20260602`, region `us-central1`.

## Recursos Activos

- Cloud Run: `stormsboys-agents-api`.
- Artifact Registry: `stormsboys`.
- Cloud SQL PostgreSQL 16: `stormsboys-pgvector`.
- Secret Manager: `stormsboys-database-url`.
- Vertex AI / Gemini: `gemini-2.5-flash`.
- Vertex AI Embeddings: `gemini-embedding-001`.

## Despliegue

Scripts disponibles:

- `infra/cloud-run/plan.sh`: muestra comandos sin crear recursos.
- `infra/cloud-run/deploy.sh`: ejecuta despliegue solo con `CONFIRM_DEPLOY=true`.

Ejemplo:

```bash
GCP_PROJECT_ID=stormsboys-agents-20260602 ./infra/cloud-run/plan.sh
CONFIRM_DEPLOY=true GCP_PROJECT_ID=stormsboys-agents-20260602 ./infra/cloud-run/deploy.sh
```

## Verificacion

```bash
BASE_URL=https://stormsboys-agents-api-5mpmuf566a-uc.a.run.app make smoke
./scripts/check-public-ready.sh
```

Tambien verificar:

- `/api/v1/challenge/storage`
- `/api/v1/challenge/storage/demo-seed`
- `/api/v1/demo/chat/character`
- `/api/v1/demo/narration`
- `/api/v1/demo/publisher`

## Rollback

```bash
gcloud run services update-traffic stormsboys-agents-api \
  --region us-central1 \
  --project stormsboys-agents-20260602 \
  --to-revisions PREVIOUS_REVISION=100
```

## Politica

No se ejecutara ningun comando nuevo de creacion en Google Cloud sin documentar antes:

- Servicio afectado.
- Coste esperado.
- Comando.
- Plan de rollback.
