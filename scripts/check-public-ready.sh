#!/usr/bin/env bash
set -euo pipefail

rg -n "AIza[0-9A-Za-z_-]{20,}|BEGIN (RSA )?PRIVATE KEY|private_key|client_secret|service_account|/Users/" . \
  --glob '!docs/submission/03-public-repo-readiness.md' \
  --glob '!scripts/check-public-ready.sh' \
  --glob '!.venv/**' \
  --glob '!__pycache__/**' \
  --glob '!*.pyc' \
  && {
    echo "Potential sensitive strings found. Review before publishing." >&2
    exit 1
  }

echo "No obvious sensitive strings found."
