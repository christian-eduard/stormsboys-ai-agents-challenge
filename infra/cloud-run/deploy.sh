#!/usr/bin/env bash
set -euo pipefail

if [[ "${CONFIRM_DEPLOY:-}" != "true" ]]; then
  echo "Refusing to deploy. Set CONFIRM_DEPLOY=true after reviewing infra/cloud-run/plan.sh." >&2
  exit 1
fi

GCP_PROJECT_ID="${GCP_PROJECT_ID:?Set GCP_PROJECT_ID}"
GCP_REGION="${GCP_REGION:-us-central1}"
ARTIFACT_REPOSITORY="${ARTIFACT_REPOSITORY:-stormsboys}"
SERVICE_NAME="${SERVICE_NAME:-stormsboys-agents-api}"
IMAGE_NAME="${IMAGE_NAME:-stormsboys-agents-api}"
RUNTIME_SERVICE_ACCOUNT="${RUNTIME_SERVICE_ACCOUNT:-stormsboys-agents-runtime@${GCP_PROJECT_ID}.iam.gserviceaccount.com}"
CLOUD_SQL_INSTANCE="${CLOUD_SQL_INSTANCE:-${GCP_PROJECT_ID}:${GCP_REGION}:stormsboys-pgvector}"
DATABASE_SECRET="${DATABASE_SECRET:-stormsboys-database-url}"
GEMINI_MODEL="${GEMINI_MODEL:-gemini-2.5-flash}"
GEMINI_EMBEDDING_MODEL="${GEMINI_EMBEDDING_MODEL:-gemini-embedding-001}"
IMAGE_URI="${GCP_REGION}-docker.pkg.dev/${GCP_PROJECT_ID}/${ARTIFACT_REPOSITORY}/${IMAGE_NAME}:latest"

gcloud services enable \
  run.googleapis.com \
  artifactregistry.googleapis.com \
  cloudbuild.googleapis.com \
  secretmanager.googleapis.com \
  aiplatform.googleapis.com \
  --project "${GCP_PROJECT_ID}"

gcloud artifacts repositories describe "${ARTIFACT_REPOSITORY}" \
  --location "${GCP_REGION}" \
  --project "${GCP_PROJECT_ID}" >/dev/null 2>&1 \
  || gcloud artifacts repositories create "${ARTIFACT_REPOSITORY}" \
    --repository-format docker \
    --location "${GCP_REGION}" \
    --project "${GCP_PROJECT_ID}"

gcloud builds submit \
  --tag "${IMAGE_URI}" \
  --project "${GCP_PROJECT_ID}"

gcloud run deploy "${SERVICE_NAME}" \
  --image "${IMAGE_URI}" \
  --region "${GCP_REGION}" \
  --project "${GCP_PROJECT_ID}" \
  --service-account "${RUNTIME_SERVICE_ACCOUNT}" \
  --allow-unauthenticated \
  --add-cloudsql-instances "${CLOUD_SQL_INSTANCE}" \
  --set-secrets "DATABASE_URL=${DATABASE_SECRET}:latest" \
  --set-env-vars APP_ENV=demo,DEMO_MODE=true,GOOGLE_GENAI_USE_VERTEXAI=true,GOOGLE_CLOUD_PROJECT="${GCP_PROJECT_ID}",GOOGLE_CLOUD_LOCATION="${GCP_REGION}",GEMINI_MODEL="${GEMINI_MODEL}",GEMINI_EMBEDDING_MODEL="${GEMINI_EMBEDDING_MODEL}"
