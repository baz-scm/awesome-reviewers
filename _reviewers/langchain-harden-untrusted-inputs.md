---
title: Harden Untrusted Inputs
description: 'When code uses externally influenced data (URLs, hostnames, user-provided
  strings, identifiers) across trust boundaries, treat it as hostile and apply layered
  defenses:'
repository: langchain-ai/langchain
label: Security
language: Python
comments_count: 5
repository_stars: 136312
---

When code uses externally influenced data (URLs, hostnames, user-provided strings, identifiers) across trust boundaries, treat it as hostile and apply layered defenses:

- **Network/URL safety (SSRF + DoS):** use an SSRF-safe client/validator, set **timeouts**, enforce **maximum response sizes**, and **stream**/abort as soon as caps are exceeded (don’t fully buffer). Also reject obviously bad declared sizes (e.g., Content-Length over the cap).
- **Validation/allowlisting:** for hostnames/IPs and other security-relevant fields, validate against an explicit policy (blocked private ranges, cloud metadata IPs/hosts, etc.). Keep hostname coverage consistent with your environment (e.g., consider whether `host.docker.internal` should be blocked or allowed based on your threat model).
- **Sanitize for downstream syntax/rendering:** before using strings in templates/renderers (Mermaid nodes, formatted placeholders, etc.), constrain allowed characters or escape/sanitize safely; document the assumptions about allowed character sets.
- **Don’t silence security tooling weakly:** avoid `noqa`/suppression for insecure primitives (e.g., MD5) unless there’s a clearly justified reason and the rationale is documented.
- **Document limitations + add tests:** security middleware/controls are mitigations—document what they protect against and what they don’t (e.g., PII handling middleware helps avoid sending PII to an LLM, but doesn’t guarantee full compliance in your logging/checkpointing/infrastructure). Add tests for the security-relevant edge cases (oversized/lying headers, SSRF policy behavior, etc.).

Example (network cap + safe client pattern):
```python
import httpx

timeout = 5.0
max_size = 50 * 1024 * 1024  # 50MB

response = _get_ssrf_safe_client().get(image_source, timeout=timeout)
response.raise_for_status()

content_length = response.headers.get("content-length")
if content_length and int(content_length) > max_size:
    return None

buf = bytearray()
for chunk in response.iter_bytes():
    buf.extend(chunk)
    if len(buf) > max_size:
        return None
```

If you apply this standard consistently, you reduce SSRF and resource-exhaustion risk while also preventing unsafe rendering/templating behavior and avoiding “security bypass by suppression.”