---
title: Robust LLM Integration
description: 'When integrating LLMs/embeddings into production code, treat the model
  as unreliable: enforce a stable IO contract (especially JSON), validate and safely
  recover from format mismatches, and route model calls through the project’s unified
  abstractions with configurable parameters.'
repository: eosphoros-ai/DB-GPT
label: AI
language: Python
comments_count: 6
repository_stars: 18703
---

When integrating LLMs/embeddings into production code, treat the model as unreliable: enforce a stable IO contract (especially JSON), validate and safely recover from format mismatches, and route model calls through the project’s unified abstractions with configurable parameters.

Apply this checklist:
1) Make LLM outputs contract-safe
- Assume responses may not contain the expected ```json block or may include extra text.
- Parse defensively (try strict code-fence JSON first, then fall back to the first JSON object), validate required fields, and on failure return a safe default (e.g., empty dict) rather than throwing.

Example (defensive JSON parsing):
```python
import json, re
from typing import Optional, Dict

def parse_llm_json(text: str) -> Dict:
    # 1) Prefer ```json ... ```
    code_block = re.search(r"```json\s*(.*?)\s*```", text, re.S|re.I)
    candidate = code_block.group(1) if code_block else None

    # 2) Fallback: first JSON object
    if not candidate:
        obj = re.search(r"\{.*?\}", text, re.S)
        candidate = obj.group(0) if obj else ""

    if not candidate:
        return {}

    try:
        data = json.loads(candidate)
    except json.JSONDecodeError:
        return {}

    # 3) Validate minimum contract
    if not isinstance(data, dict):
        return {}
    return data
```

2) Never call provider SDKs directly in core business logic
- Use the project’s LLM abstraction layer (e.g., the same path as LLMExtractor/LLMTranslator) to centralize auth, retries, routing, and message handling.
- Avoid global mutable history variables; rely on framework-managed conversation state.

3) Keep embeddings/models configurable and extensible
- Don’t hardcode embedding dimension or provider model details.
- Accept/configure `embedding_fn` (or an equivalent abstraction) so switching embedding providers/models doesn’t require code changes.

4) Keep message/history handling consistent
- If a proxy backend can’t handle multi-turn directly, convert messages only; let the framework manage multi-turn formatting.

5) Add fallback behavior for empty/failed vector sub-results
- If vector-based graph/entity expansion returns empty, fall back to keyword-based search (or another deterministic strategy) so retrieval doesn’t silently degrade.

This standard prevents production breakage from minor LLM formatting drift, improves portability across LLM providers, and makes embedding/model changes safe and configuration-driven.