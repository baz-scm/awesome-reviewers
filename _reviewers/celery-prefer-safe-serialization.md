---
title: Prefer safe serialization
description: Avoid `pickle` unless you have a documented, justified need and you can
  guarantee the serialized data never comes from untrusted sources. Prefer safe, data-only
  formats (e.g., JSON) for serialization/deserialization in tests and production code.
repository: celery/celery
label: Security
language: Python
comments_count: 1
repository_stars: 28464
---

Avoid `pickle` unless you have a documented, justified need and you can guarantee the serialized data never comes from untrusted sources. Prefer safe, data-only formats (e.g., JSON) for serialization/deserialization in tests and production code.

Example (safer alternative pattern):
```python
import json

payload = {
    "app": "sentinel-app",
    "max_interval": "sentinel-max_interval",
    "schedule_filename": "sentinel-schedule_filename",
    "scheduler_cls": "sentinel-scheduler_cls",
}

# Round-trip the data representation (no code execution during parsing)
serialized = json.dumps(payload)
restored = json.loads(serialized)
```

If `pickle` is unavoidable, require a clear justification in code/comments and ensure it is only ever used with objects/data produced locally (no user input, no external storage, no network-delivered blobs).