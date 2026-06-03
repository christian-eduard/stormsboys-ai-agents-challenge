# Devpost Fields

## Project Name

Stormsboys AI Agents: Multi-Agent Literary Intelligence Platform

## Tagline

Books become interactive multi-agent worlds powered by Gemini, Cloud Run, and pgvector.

## Track

Track 3: Refactor for Google Cloud Marketplace & Gemini Enterprise

## Demo URL

https://stormsboys-agents-api-5mpmuf566a-uc.a.run.app

## Testing Credentials

No credentials required.

## Repository URL

https://github.com/christian-eduard/stormsboys-ai-agents-challenge

## Video URL

TODO: add public demo video URL after recording.

## Short Description

Stormsboys transforms books into interactive literary worlds. Authors and publishers can upload owned or public-domain manuscripts, Gemini prepares characters with psychology and canon constraints, readers can talk to grounded character agents, and publishers can review engagement and quality insights. The system targets Track 3 Marketplace readiness while also showing Track 2-style optimization through agent traces, consistency checks, and baseline-versus-optimized evaluation.

## Google Cloud Services

- Cloud Run
- Vertex AI / Gemini
- Vertex AI Embeddings
- Cloud SQL PostgreSQL
- pgvector
- Secret Manager
- Cloud Logging

## Key Technical Proof

- Public Cloud Run demo.
- Character generation with `gemini-2.5-flash`.
- Retrieval embeddings with `gemini-embedding-001`.
- Cloud SQL PostgreSQL with pgvector retrieval.
- Real manuscript upload, catalog insertion, uploaded-book retrieval, and chat by `book_id`.
- Agent traces for retrieval, character generation, consistency, narration, and publisher insights.
- Track 2 evaluation across 12 cases.

## Known Limitations

- The narration feature currently produces a TTS-ready SSML plan, not streamed audio playback.
- Upload currently accepts text-based `.txt`, `.md`, and text-extractable `.pdf` files; scanned-image PDFs would need OCR in a production Marketplace version.
