# Public Repository Readiness

## Must Be True Before Publishing

- No `.env` files.
- No API keys.
- No service account JSON files.
- No private books.
- No private conversations.
- No unrelated project references.
- No hardcoded cloud project IDs.
- No hardcoded demo passwords.
- License selected.
- README setup verified from a fresh clone.

## Checks

```bash
rg -n "AIza[0-9A-Za-z_-]{20,}|BEGIN (RSA )?PRIVATE KEY|private_key|client_secret|service_account|/Users/" .
git status --short
```

## Public README Must Include

- Project summary.
- Track.
- Architecture diagram.
- Google Cloud services used.
- Local setup.
- Demo instructions.
- Evaluation approach.
- Security notes.
