---
title: Token and Prompt Fidelity
description: 'When implementing LLM/AI APIs (including streaming), treat three things
  as contract-critical: (1) compute token usage with a real tokenizer, (2) ensure
  the intended system/user context is actually passed through every planning/tool
  stage, and (3) emit only the events your client expects.'
repository: infiniflow/ragflow
label: AI
language: Python
comments_count: 4
repository_stars: 80174
---

When implementing LLM/AI APIs (including streaming), treat three things as contract-critical: (1) compute token usage with a real tokenizer, (2) ensure the intended system/user context is actually passed through every planning/tool stage, and (3) emit only the events your client expects.

**1) Token usage must use tokenizer-based counting**
Avoid `len(text)` for `prompt_tokens/total_tokens`; it’s character-based and will be wrong across languages/models. Use a tokenizer compatible with your target model.

```python
import tiktoken

tokenizer = tiktoken.get_encoding("cl100k_base")

context_token_used = sum(len(tokenizer.encode(m["content"])) for m in messages)
# use similar encoding for prompt_tokens/completion_tokens
```

**2) Prompt plumbing must be correct**
If an agent/planning function takes `prompt`/`sys_prompt`/history, pass the correct variables. Add a small assertion or unit test to ensure downstream components receive the system prompt intended for the run (not a different variable like history or an uninitialized prompt).

**3) Streaming/compatibility endpoints must filter noise**
If the upstream emits multiple event types (e.g., content vs reference chunks), only forward the subset your client UI consumes. Example logic:

```python
# keep only the LLM response and its related finalization/reference
if event not in ["message", "message_end"]:
    continue
```

**How to apply**
- For every LLM endpoint response, confirm token fields are derived from tokenizer counts.
- For every agent/tool/planning path, verify the system prompt and user history are the same objects used to build the actual prompt that reaches planning.
- For streaming, ensure you accumulate deltas consistently and only emit client-meaningful events.