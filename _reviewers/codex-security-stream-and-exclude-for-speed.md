---
title: Stream and Exclude for Speed
description: 'Optimize scan/diff/hash pipelines by (1) preventing large in-memory
  buffering and (2) shrinking the input set early.


  Apply these rules:

  - Measure first: when changing digest/patch handling, record memory/size deltas
  on realistic fixtures (e.g., large binary diffs) and use deterministic comparisons
  (streaming output must match buffered output).'
repository: openai/codex-security
label: Performance Optimization
language: Python
comments_count: 2
repository_stars: 9394
---

Optimize scan/diff/hash pipelines by (1) preventing large in-memory buffering and (2) shrinking the input set early.

Apply these rules:
- Measure first: when changing digest/patch handling, record memory/size deltas on realistic fixtures (e.g., large binary diffs) and use deterministic comparisons (streaming output must match buffered output).
- Prefer streaming + chunked hashing: route subprocess stdout through a mechanism that avoids holding the entire patch in RAM. If protocol framing requires knowing total length up front, spool to a temp file, use fstat to get the size, then hash in fixed chunks.
- Preserve determinism: if revalidation compares digests, ensure the digest framing is stable across implementations.
- Exclude known “noise” inputs by default: skip `.venv`, `vendor`, and large binary assets unless explicitly requested, to avoid dominating review cost and hitting file-count caps.

Example pattern (chunked digest with spooling when length is part of the hashed framing):
```python
import hashlib, os, tempfile

def digest_stream_with_length(cmd_stdout_pipe, value_length_prefix_bytes=8):
    with tempfile.NamedTemporaryFile() as f:
        # write Git stdout to temp to avoid buffering full patch in memory
        while True:
            chunk = cmd_stdout_pipe.read(1024 * 1024)
            if not chunk:
                break
            f.write(chunk)
        f.flush()

        size = os.fstat(f.fileno()).st_size
        h = hashlib.sha256()
        h.update(size.to_bytes(value_length_prefix_bytes, 'big'))
        f.seek(0)
        while True:
            chunk = f.read(1024 * 1024)
            if not chunk:
                break
            h.update(chunk)
        return h.hexdigest()
```

Outcome: less peak memory, less wasted work, and consistent, verifiable results under revalidation.