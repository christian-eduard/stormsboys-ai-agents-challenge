# Devpost Fields

## Project Name

Stormsboys AI Agents: Multi-Agent Literary Intelligence Platform

## Tagline

Books become interactive multi-agent worlds powered by Gemini, Cloud Run, and pgvector.

## Track

Track 2: Optimize Existing Agents

## Demo URL

https://stormsboys-agents-api-5mpmuf566a-uc.a.run.app

## Testing Credentials

No credentials required.

## Repository URL

https://github.com/christian-eduard/stormsboys-ai-agents-challenge

## Video URL

TODO: add public demo video URL after recording.

## Short Description

Stormsboys transforms books into interactive literary worlds. Readers can talk to grounded character agents, explore multi-character scenes, prepare narration handoffs, and publishers can review engagement and quality insights. The system demonstrates Track 2 optimization through agent traces, consistency checks, and baseline-versus-optimized evaluation.

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
- Agent traces for retrieval, character generation, consistency, narration, and publisher insights.
- Track 2 evaluation across 12 cases.

## Known Limitations

- The deployed judge demo uses a controlled sample book.
- The narration feature currently produces a TTS-ready SSML plan, not streamed audio playback.
- Uploading arbitrary public books is intentionally out of scope for this short challenge demo.
