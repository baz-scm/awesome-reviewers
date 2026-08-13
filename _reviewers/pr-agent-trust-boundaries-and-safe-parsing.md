---
title: Trust Boundaries And Safe Parsing
description: Treat any repo-controlled config, external webhook payload, or model-generated
  text as untrusted. Enforce trust boundaries and use safe parsing/validation to prevent
  SSRF/exfiltration, arbitrary file writes, and unsafe deserialization.
repository: the-pr-agent/pr-agent
label: Security
language: Python
comments_count: 8
repository_stars: 12523
---

Treat any repo-controlled config, external webhook payload, or model-generated text as untrusted. Enforce trust boundaries and use safe parsing/validation to prevent SSRF/exfiltration, arbitrary file writes, and unsafe deserialization.

Checklist
- Host/operator-only settings: If a setting controls outbound requests or file/network side effects, ensure repo configuration cannot enable/override it (e.g., gate with an operator-owned allowlist and ignore/deny repo overrides).
- Disable dynamic/unsafe config behavior: when loading configuration from files, disable features that can introduce unexpected loading/merging (e.g., dotenv loading and cross-source merges).
- Verify authenticity before processing: webhook signature verification must fail closed (return/raise on verification failure rather than continuing).
- Validate required request fields by action/type: don’t assume fields exist for all action variants.
- Safe parsing for untrusted text: never use `yaml.load` for untrusted input; use `yaml.safe_load` and sanitize code fences; provide a safe fallback when parsing fails.

Example (safe parsing + failure handling)
```python
import yaml
from yaml import safe_load

def parse_model_yaml(prediction: str) -> dict:
    # Strip common markdown fences
    text = prediction.strip()
    text = text.lstrip('```yaml').rstrip('`')

    try:
        data = yaml.safe_load(text)
    except Exception:
        # Fall back to a safe default / fixup strategy (still using safe_load)
        data = {}
    if not isinstance(data, dict):
        return {}
    return data
```

Apply the same “untrusted-by-default” mindset to repo settings and webhook data: deny/ignore repo overrides that affect side effects, verify before use, validate inputs, and parse with safe primitives.