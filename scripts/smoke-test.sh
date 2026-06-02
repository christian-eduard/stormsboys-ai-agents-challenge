#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-http://127.0.0.1:8088}"
CURL=(curl --max-time 60 --fail --silent)

HOME_HTML="$("${CURL[@]}" "${BASE_URL}/")"
APP_JS="$("${CURL[@]}" "${BASE_URL}/static/app.js")"

grep -q "Multi-agent literary intelligence" <<<"${HOME_HTML}"
grep -q "Choose a demo account" <<<"${HOME_HTML}"
grep -q "Submission readiness" <<<"${HOME_HTML}"
grep -q 'data-view="dashboard"' <<<"${HOME_HTML}"
grep -q 'data-view="author"' <<<"${HOME_HTML}"
grep -q "runEvaluation" <<<"${APP_JS}"
grep -q "judge_access" <<<"${APP_JS}"
grep -q "runAuthorWorkflow" <<<"${APP_JS}"
"${CURL[@]}" "${BASE_URL}/health" >/dev/null
"${CURL[@]}" "${BASE_URL}/api/v1/challenge/readiness" >/dev/null
"${CURL[@]}" "${BASE_URL}/api/v1/challenge/capabilities" >/dev/null
"${CURL[@]}" "${BASE_URL}/api/v1/challenge/submission" >/dev/null
"${CURL[@]}" "${BASE_URL}/api/v1/challenge/storage" >/dev/null
"${CURL[@]}" "${BASE_URL}/api/v1/challenge/storage/demo-seed" >/dev/null
"${CURL[@]}" "${BASE_URL}/api/v1/auth/demo-users" >/dev/null
LOGIN_RESPONSE="$("${CURL[@]}" \
  -X POST "${BASE_URL}/api/v1/auth/demo-login" \
  -H "content-type: application/json" \
  -d '{"user_id":"superadmin-demo"}' \
)"
TOKEN="$(python3 -c 'import json,sys; print(json.load(sys.stdin)["token"])' <<<"${LOGIN_RESPONSE}")"
"${CURL[@]}" "${BASE_URL}/api/v1/admin/roles" >/dev/null
"${CURL[@]}" "${BASE_URL}/api/v1/admin/marketplace" \
  -H "authorization: Bearer ${TOKEN}" \
  >/dev/null
"${CURL[@]}" "${BASE_URL}/api/v1/admin/operations" \
  -H "authorization: Bearer ${TOKEN}" \
  >/dev/null
"${CURL[@]}" "${BASE_URL}/api/v1/demo/author-workflow" \
  -H "authorization: Bearer ${TOKEN}" \
  >/dev/null
"${CURL[@]}" "${BASE_URL}/api/v1/demo/evaluation" >/dev/null
"${CURL[@]}" "${BASE_URL}/api/v1/demo/publisher" \
  -H "authorization: Bearer ${TOKEN}" \
  >/dev/null
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
