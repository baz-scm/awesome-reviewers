---
title: Accurate AI Content
description: When writing AI/LLM-related documentation or roadmap material, ensure
  it (a) states model limitations precisely, (b) stays in the correct scope for the
  node/context, and (c) explains implementations in terms of the underlying pipeline
  (prefer pre-trained tools) rather than framework specifics.
repository: kamranahmedse/developer-roadmap
label: AI
language: Markdown
comments_count: 6
repository_stars: 354523
---

When writing AI/LLM-related documentation or roadmap material, ensure it (a) states model limitations precisely, (b) stays in the correct scope for the node/context, and (c) explains implementations in terms of the underlying pipeline (prefer pre-trained tools) rather than framework specifics.

Apply these rules:
- Don’t present LLM outputs/citations as guaranteed. If citations are mentioned, explicitly note hallucinated/incorrect citations and mitigation (improved retrieval, RAG, and human oversight).
- Distinguish error modes when relevant: faithfulness (output diverges from provided context/sources) vs factuality (unsupported/incorrect facts).
- Keep multimodal sections multimodal: describe how the model is used for vision/audio within multimodal AI, not generic “image/audio processing” theory.
- Prefer “use pre-trained models/tools” framing for roadmap content; avoid unnecessary CNN/RNN architecture detail unless the node is explicitly about that.
- For RAG/agent patterns, describe the end-to-end steps (chunking → embeddings → store in vector DB → embed the query → similarity search → provide retrieved context), without requiring a specific library.

Example (claiming citations safely):
- Instead of: “The model will cite sources correctly.”
- Use: “LLMs may generate inaccurate or fictitious citations; use retrieval (RAG) plus verification/human oversight when citations matter.”