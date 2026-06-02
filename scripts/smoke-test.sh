#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-http://127.0.0.1:8088}"

curl --fail --silent "${BASE_URL}/" | grep -q "Multi-agent literary intelligence"
curl --fail --silent "${BASE_URL}/static/app.js" | grep -q "runEvaluation"
curl --fail --silent "${BASE_URL}/health" >/dev/null
curl --fail --silent "${BASE_URL}/api/v1/challenge/readiness" >/dev/null
curl --fail --silent "${BASE_URL}/api/v1/challenge/capabilities" >/dev/null
curl --fail --silent "${BASE_URL}/api/v1/challenge/storage" >/dev/null
curl --fail --silent "${BASE_URL}/api/v1/challenge/storage/demo-seed" >/dev/null
curl --fail --silent "${BASE_URL}/api/v1/demo/evaluation" >/dev/null
curl --fail --silent "${BASE_URL}/api/v1/demo/publisher" >/dev/null
curl --fail --silent \
  -X POST "${BASE_URL}/api/v1/demo/chat/character" \
  -H "content-type: application/json" \
  -d '{"character_id":"don_quijote","question":"Why do you attack the windmills?"}' \
  >/dev/null
curl --fail --silent \
  -X POST "${BASE_URL}/api/v1/demo/narration" \
  -H "content-type: application/json" \
  -d '{"scene_text":"Don Quijote charges at the windmills while Sancho warns him."}' \
  >/dev/null

echo "Smoke test passed for ${BASE_URL}"
