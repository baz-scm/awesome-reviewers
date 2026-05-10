---
title: High-signal Testing Practices
description: 'Write tests that are (a) high-signal and not fragile, and (b) structured
  with standard pytest mechanisms.


  Apply:

  - Use fixtures instead of module/global clients, so each test has clean, controllable
  dependencies.'
repository: anthropics/anthropic-sdk-python
label: Testing
language: Python
comments_count: 6
repository_stars: 3392
---

Write tests that are (a) high-signal and not fragile, and (b) structured with standard pytest mechanisms.

Apply:
- Use fixtures instead of module/global clients, so each test has clean, controllable dependencies.
- For new externally observable behavior, add a targeted test. If the output is complex, use a snapshot/recorded example.
- For internal “plumbing” where deep inspection isn’t possible, start with a smoke test (no exceptions) and optionally mock the dependency to assert that key arguments are passed.
- Use `pytest.MonkeyPatch.context()` (or equivalent) to ensure patches clean up at the right scope.
- Skip conditionally with `pytest.mark.skipif(...)` instead of early-return branches.
- Assert only the behavior that matters; avoid extra checks that are likely to be stripped/modified by proxies (e.g., don’t add confusing header assertions when you only need to verify `Authorization`).

Example (focused assertion + fixture-friendly structure):

```python
import re
import pytest
import respx
import httpx
from unittest.mock import Mock

@pytest.mark.respx()
def test_bearer_token_env_passes_authorization(monkeypatch: pytest.MonkeyPatch, respx_mock):
    respx_mock.post(re.compile(r"https://bedrock-runtime\.us-east-1\.amazonaws\.com/model/.*/invoke")).mock(
        return_value=httpx.Response(200, json={"ok": True})
    )

    monkeypatch.setenv("AWS_BEARER_TOKEN_BEDROCK", "test-bearer-token")

    # exercise code that triggers the request
    # sync_client.messages.create(...)

    calls = list(respx_mock.calls)
    assert len(calls) == 1
    assert calls[0].request.headers.get("Authorization") == "Bearer test-bearer-token"
```

This approach keeps tests reliable, maintainable, and valuable as the code evolves.