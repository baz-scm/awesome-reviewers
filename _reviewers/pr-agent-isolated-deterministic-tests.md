---
title: Isolated, Deterministic Tests
description: 'Tests should be deterministic and non-leaky: any test that depends on
  (or mutates) global state, environment variables, or import-time configuration must
  isolate that impact and restore it afterward.'
repository: the-pr-agent/pr-agent
label: Testing
language: Python
comments_count: 5
repository_stars: 12523
---

Tests should be deterministic and non-leaky: any test that depends on (or mutates) global state, environment variables, or import-time configuration must isolate that impact and restore it afterward.

Apply this as a team rule:
1) Snapshot/restore global SDK state with fixtures
- If your code reads/writes globals (e.g., `litellm.*`, `openai.*`), use an `autouse` fixture to snapshot before each test and restore in `finally`.
- If environment variables can trigger alternate code paths, snapshot them too and temporarily disable the triggering path.

```python
import os
import pytest
import litellm
import openai

@pytest.fixture(autouse=True)
def _restore_globals():
    saved = {
        "litellm_api_key": litellm.api_key,
        "litellm_openai_key": getattr(litellm, "openai_key", None),
        "openai_api_key": openai.api_key,
        "aws_use_imds": os.environ.get("AWS_USE_IMDS"),
        "aws_region": os.environ.get("AWS_REGION_NAME"),
    }
    try:
        # ensure code paths are not environment-dependent
        os.environ.pop("AWS_USE_IMDS", None)
        yield
    finally:
        litellm.api_key = saved["litellm_api_key"]
        litellm.openai_key = saved["litellm_openai_key"]
        openai.api_key = saved["openai_api_key"]
        if saved["aws_use_imds"] is None:
            os.environ.pop("AWS_USE_IMDS", None)
        else:
            os.environ["AWS_USE_IMDS"] = saved["aws_use_imds"]
```

2) Isolate import-time configuration
- For tests that verify “module imports without optional config sections”, do not rely on in-process config mutation + `reload()`; prefer running the import in a subprocess, or strictly set config before import and restore afterward.

3) Exercise real wiring under patched settings (avoid uncovered dead wiring)
- If you bypass constructors (e.g., using `__new__` to avoid network calls), ensure tests still cover the important wiring/derived attributes by setting them via the real resolver under patched configuration—don’t hardcode values that mask regressions.

Result: suites won’t pass or fail depending on execution order, developer machine env, or pre-existing global/config state, and they will correctly catch wiring regressions.