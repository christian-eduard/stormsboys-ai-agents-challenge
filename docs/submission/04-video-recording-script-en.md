# 1-2 Minute Demo Video Script

## Goal

Record a clear English demo that proves the product, the agent architecture, the Google Cloud runtime, and the Track 2 before/after improvement.

Target length: 90 seconds.

## Pre-Recording Setup

- Open: `https://stormsboys-agents-api-5mpmuf566a-uc.a.run.app`.
- Zoom browser to 100%.
- Keep DevTools closed.
- Use the default prompts already loaded in the UI.
- Run through the flow once before recording.

## Script

### 0:00-0:10 Opening

"Stormsboys turns books into interactive multi-agent worlds. Instead of a passive ebook, readers can talk to characters, explore scenes, and publishers can measure narrative engagement."

Show the reader panel with Don Quijote de la Mancha.

### 0:10-0:25 Book Analysis

"The demo starts from a processed book. The system extracts characters, places, scenes, and a grounded retrieval layer."

Point at characters, places, and scenes counters.

### 0:25-0:45 Character Agent

Click `Ask character` with:

```txt
Why do you attack the windmills?
```

Say:

"This is not a generic chatbot. The Character Agent answers as Don Quijote, while the Retrieval Agent grounds the response in the book and the consistency agent checks narrative faithfulness."

Point at the trace list.

### 0:45-1:00 Out-Of-Canon Guardrail

Click `Out-of-canon test`.

Say:

"For Track 2, we optimized reliability. When the question asks for unsupported future canon, the system should acknowledge missing evidence instead of inventing."

### 1:00-1:15 Scene Orchestrator

Click `Run scene`.

Say:

"The Scene Orchestrator coordinates multiple character agents, so the book behaves like a multi-agent environment rather than a single assistant."

### 1:15-1:25 Voice And Publisher

Click `Prepare` in Voice / Narration Agent, then `Analyze` in Publisher Insights Agent.

Say:

"The same agent layer can prepare narration handoff for TTS and produce publisher insights such as engagement, quality, and recommendations."

### 1:25-1:40 Track 2 Evaluation

Click `Run` in evaluation if needed.

Say:

"The evaluation panel shows baseline versus optimized behavior across twelve cases, including grounding, voice, missing evidence, multilingual prompts, and multi-step reasoning."

### 1:40-1:55 Runtime Proof

Scroll to Runtime.

Say:

"The public demo is deployed on Cloud Run, uses Gemini through Vertex AI, Gemini embeddings, Cloud SQL PostgreSQL with pgvector, Secret Manager, and visible agent traces."

### 1:55-2:00 Close

"Stormsboys is a production-oriented multi-agent literary intelligence platform for readers, authors, publishers, and education."

## Do Not Say

- Do not claim arbitrary book upload is fully supported in the deployed demo.
- Do not claim real audio playback unless Google TTS is added.
- Do not mention unrelated local projects.
- Do not mention private billing details.

## Backup If Gemini Is Slow

Use the already-rendered response from the first dry run and focus the narration on traces, evaluation, runtime proof, and publisher value.
