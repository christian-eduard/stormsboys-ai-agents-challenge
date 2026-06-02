# Testing Access Instructions

## Demo URL

https://stormsboys-agents-api-5mpmuf566a-uc.a.run.app

## Credentials

No credentials required for the challenge demo.

## Recommended Judge Flow

1. Open the demo URL.
2. Review the preloaded demo book.
3. Ask Don Quijote: "Why do you attack the windmills?"
4. Confirm the trace shows `retrieval.pgvector_search`, `CharacterAgent`, and `NarrativeConsistencyAgent`.
5. Run the out-of-canon test.
6. Open the scene/group chat.
7. Prepare the narration plan.
8. Open the publisher/admin insights view.
9. Review the Track 2 before/after evaluation.
10. Review the runtime proof panel for Gemini and Cloud SQL pgvector.

## What To Look For

- The response is grounded in the book.
- The character keeps a distinct voice.
- Multi-character scenes show coordinated agents.
- The narration panel produces a TTS-ready plan.
- The publisher panel explains business value and quality signals.
- The trace view shows pgvector retrieval, Gemini generation, and consistency validation.
- The evaluation shows baseline versus optimized behavior across 12 cases.

## Known Limitations

- The deployed demo uses a controlled sample book rather than arbitrary public uploads.
- pgvector retrieval is real and backed by Cloud SQL. The deployed demo reports `gemini-embedding-001` through Vertex AI in the runtime proof panel.
- Character generation uses Gemini through Vertex AI.
