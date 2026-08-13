---
title: Deterministic script error handling
description: Treat IO and parse failures as first-class outcomes, with behavior that
  is (a) deterministic, (b) contract-respecting, and (c) strict about “malformed but
  present” config.
repository: bmad-code-org/bmad-method
label: Error Handling
language: Python
comments_count: 3
repository_stars: 51859
---

Treat IO and parse failures as first-class outcomes, with behavior that is (a) deterministic, (b) contract-respecting, and (c) strict about “malformed but present” config.

**Coding standard**
1. **Define the contract first**: For each script, document/encode whether failures must return **exit code 0** (with an error payload), or use **non-zero** exit codes, and whether the caller expects **stdout JSON** vs **stderr text**.
2. **Wrap risky operations**: Always `try/except` around file reads and decoding/parsing (e.g., `read_text`, `json.loads`, `tomllib.load`) and do **not** let tracebacks leak to users/CI.
3. **Emit a single-line error**: On failure, print `error: ...` to `stderr` and either:
   - return a **non-zero exit code** (typical for “cannot render/compute”), or
   - return **exit 0 but output error JSON** if that is the script’s stated contract.
4. **Differentiate missing vs malformed**:
   - **Missing optional files** may degrade gracefully (empty config).
   - If a file **exists but is invalid** (bad JSON/TOML/encoding), treat it as a **hard failure or loudly block execution**—especially when it affects org/user guardrails or other safety constraints.
5. **Test representative failures**: Add tests for missing files, malformed content, and bad encodings.

**Example pattern**
```python
from pathlib import Path
import json, sys

def load_required_json(path: Path) -> dict:
    try:
        data = path.read_text(encoding="utf-8")
        return json.loads(data)
    except FileNotFoundError:
        sys.stderr.write(f"error: findings file not found: {path}
")
        raise SystemExit(1)
    except json.JSONDecodeError:
        sys.stderr.write(f"error: findings file is not valid JSON: {path}
")
        raise SystemExit(1)

# Optional vs required distinction
def load_optional_toml(path: Path) -> dict:
    if not path.exists():
        return {}  # missing is OK
    try:
        # parse toml here
        ...
    except Exception:
        sys.stderr.write(f"error: customization exists but failed to parse: {path}
")
        raise SystemExit(1)  # malformed-but-present is not silently ignored
```

Applying this consistently prevents hidden misconfigurations, keeps tooling predictable, and matches each script’s stated integration contract.