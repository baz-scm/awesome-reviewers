---
title: AI Boundary Compatibility
description: 'When building AI/LLM-related tooling (tool-calls, background execution,
  inference/image generation), enforce compatibility at the boundaries:


  1) Use team-standard LLM-friendly IDs'
repository: agent0ai/agent-zero
label: AI
language: Python
comments_count: 2
repository_stars: 17612
---

When building AI/LLM-related tooling (tool-calls, background execution, inference/image generation), enforce compatibility at the boundaries:

1) Use team-standard LLM-friendly IDs
- Generate identifiers used in LLM-facing payloads with the shared `guids.py` helper and its default length (e.g., 8). Don’t invent new ID formats for tool-call correlation.

2) Make AI hardware initialization conservative + always fall back
- Hardware probing/installation for GPU/CUDA should be environment-aware and non-disruptive in minimal containers/users.
- If CUDA isn’t available, the system must reliably proceed on CPU.
- Add a smoke test using a regular minimal OS/user image (e.g., Debian slim) to ensure CUDA setup isn’t too aggressive.

Example (ID generation pattern):
```python
# pseudo-example: use the team helper rather than custom UUID strings
from python.helpers.guids import llm_guid  # assumed name from your guids.py

call_id = llm_guid(length=8)  # keep the default length consistent
```

Checklist to apply during review
- Are all LLM-facing identifiers produced via the team’s LLM-friendly GUID utility (no custom formats)?
- Does the AI runtime path (GPU/CUDA detection + setup) degrade safely to CPU when CUDA isn’t present?
- Is there at least one test/smoke run in a minimal Debian-slim style environment to validate behavior and prevent overly aggressive CUDA install/setup attempts?