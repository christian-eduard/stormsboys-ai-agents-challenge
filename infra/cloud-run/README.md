# Cloud Run Deployment Notes

This folder documents the target deployment. It intentionally does not create resources automatically yet.

Use `plan.sh` first. `deploy.sh` refuses to run unless `CONFIRM_DEPLOY=true`.

## Target Services

- `stormsboys-agents-api`: FastAPI backend and agent layer.
- Future `stormsboys-agents-web`: judge-facing web demo.

## Required APIs

- Cloud Run.
- Artifact Registry.
- Cloud Build.
- Secret Manager.
- Vertex AI / Gemini API.
- Cloud SQL Admin if database is used.

## Backend Build

```bash
gcloud builds submit \
  --tag REGION-docker.pkg.dev/PROJECT_ID/stormsboys/stormsboys-agents-api:latest
```

## Backend Deploy

```bash
gcloud run deploy stormsboys-agents-api \
  --image REGION-docker.pkg.dev/PROJECT_ID/stormsboys/stormsboys-agents-api:latest \
  --region REGION \
  --allow-unauthenticated \
  --set-env-vars APP_ENV=demo,DEMO_MODE=true
```

## Policy

Before running these commands, document:

- Final project ID.
- Region.
- Expected cost.
- Rollback command.
- Public demo access strategy.

## Safer Flow

```bash
cd infra/cloud-run
cp env.example .env.local
# export values from .env.local in your shell
./plan.sh
```

Only after review:

```bash
CONFIRM_DEPLOY=true ./deploy.sh
```
