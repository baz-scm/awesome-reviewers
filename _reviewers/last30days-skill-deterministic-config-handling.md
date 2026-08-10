---
title: Deterministic Config Handling
description: 'Treat configuration inputs as a deterministic contract: normalize/parsing
  should be robust and centralized, and config-file reading must use an explicit encoding
  matching the write path.'
repository: mvanhorn/last30days-skill
label: Configurations
language: Python
comments_count: 2
repository_stars: 57799
---

Treat configuration inputs as a deterministic contract: normalize/parsing should be robust and centralized, and config-file reading must use an explicit encoding matching the write path.

- For list/flag style settings (e.g., `INCLUDE_SOURCES`), parse with normalization and whitespace tolerance at one “single computation site”, then reuse the parsed result everywhere. This prevents subtle bugs where spaces or empty tokens change behavior.
- For `.env`/config file IO, read with an explicit encoding (typically `utf-8`) rather than relying on the runtime’s locale. If you later need to support legacy encodings, implement an explicit fallback + warning, not an implicit locale-dependent codec.

Example (list parsing + config gating):
```python
include_sources = (config.get("INCLUDE_SOURCES") or "").lower().split(",")
include_sources = [s.strip() for s in include_sources if s.strip()]

# Example gate: opt-in only
if "dripstack" in include_sources:
    enable_dripstack()
```

Example (explicit `.env` read contract):
```python
with open(path, "r", encoding="utf-8") as f:
    content = f.read()
```