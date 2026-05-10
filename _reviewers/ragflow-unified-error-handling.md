---
title: Unified Error Handling
description: 'Adopt a single error-handling standard across LLM/provider layers:


  1) Retry only transient failures (including connection jitter) with bounded, classified
  backoff'
repository: infiniflow/ragflow
label: Error Handling
language: Python
comments_count: 8
repository_stars: 80174
---

Adopt a single error-handling standard across LLM/provider layers:

1) Retry only transient failures (including connection jitter) with bounded, classified backoff
- Centralize retry behavior in shared utilities (e.g., @retry / retry_or_fallback) using error classification.
- Treat connection/network/DNS and rate-limit/server errors as retryable.
- Ensure the last attempt returns/raises a clear max-retry outcome (so callers never “fall through” without an error).
- Don’t silently support unsupported patterns: fail fast for generator/streaming functions (retrying mid-stream is unsafe).

2) Keep return/output contracts stable between success and failure
- Never change output types on exception paths (e.g., if success returns tuple(text, token_count), failure must return the same shape or be normalized before setting outputs).

3) Standardize failure encoding and checking at boundaries
- If providers encode failure in return values (e.g., prefixed strings), require callers to use the shared prefix constant and an is_error_result-style helper instead of ad-hoc string checks.

Example (type-stable normalization before setting output):
```python
try:
    transcription = seq2txt_mdl.transcription(tmp_path)
    # success may be tuple(text, token_count)
    txt = transcription[0] if isinstance(transcription, tuple) else transcription
except Exception as e:
    logging.warning(f"Transcription failed: {e}")
    txt = ""

self.set_output("text", txt)
```

Example (standard retry rule for transient polling blips):
```python
@retry
def _describe_task_status(self, req):
    return self.client.DescribeTaskStatus(req)

while retries < max_retries:
    resp = self._describe_task_status(req)  # transient 429/5xx/DNS blips survive
```

Result: fewer hidden failure modes, consistent caller behavior, and reliable recovery for transient LLM/API issues.