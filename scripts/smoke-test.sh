#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-http://127.0.0.1:8088}"
CURL=(curl --max-time 60 --fail --silent)

"${CURL[@]}" "${BASE_URL}/" | grep -q "Multi-agent literary intelligence"
"${CURL[@]}" "${BASE_URL}/static/app.js" | grep -q "runEvaluation"
"${CURL[@]}" "${BASE_URL}/health" >/dev/null
"${CURL[@]}" "${BASE_URL}/api/v1/challenge/readiness" >/dev/null
"${CURL[@]}" "${BASE_URL}/api/v1/challenge/capabilities" >/dev/null
"${CURL[@]}" "${BASE_URL}/api/v1/challenge/storage" >/dev/null
"${CURL[@]}" "${BASE_URL}/api/v1/challenge/storage/demo-seed" >/dev/null
"${CURL[@]}" "${BASE_URL}/api/v1/demo/evaluation" >/dev/null
"${CURL[@]}" "${BASE_URL}/api/v1/demo/publisher" >/dev/null
"${CURL[@]}" \
  -X POST "${BASE_URL}/api/v1/demo/chat/character" \
  -H "content-type: application/json" \
  -d '{"character_id":"don_quijote","mode":"CANON","language":"en","question":"Why do you attack the windmills?"}' \
  >/dev/null
"${CURL[@]}" \
  -X POST "${BASE_URL}/api/v1/demo/chat/character" \
  -H "content-type: application/json" \
  -d '{"character_id":"don_quijote","mode":"CANON","language":"es","question":"Por que atacas los molinos?"}' \
  >/dev/null
"${CURL[@]}" \
  -X POST "${BASE_URL}/api/v1/demo/chat/character" \
  -H "content-type: application/json" \
  -d '{"character_id":"don_quijote","mode":"FICTION","language":"en","question":"What if Sancho convinces you the giants are machines?"}' \
  >/dev/null
"${CURL[@]}" \
  -X POST "${BASE_URL}/api/v1/demo/narration" \
  -H "content-type: application/json" \
  -d '{"scene_text":"Don Quijote charges at the windmills while Sancho warns him."}' \
  >/dev/null

echo "Smoke test passed for ${BASE_URL}"
