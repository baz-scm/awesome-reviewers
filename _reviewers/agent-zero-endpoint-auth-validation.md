---
title: Endpoint Auth Validation
description: 'For security-sensitive flows (WS/API, authenticated cloning, token/API-key
  auth), don’t rely on generic or heuristic validation.


  Apply these rules:

  1) Validate with explicit allow/deny semantics'
repository: agent0ai/agent-zero
label: Security
language: Python
comments_count: 3
repository_stars: 17612
---

For security-sensitive flows (WS/API, authenticated cloning, token/API-key auth), don’t rely on generic or heuristic validation.

Apply these rules:
1) Validate with explicit allow/deny semantics
- Example: URL validators should accept only well-formed, intended schemes/authorities and reject unsafe forms.

2) Decide authorization/authZ at the destination handler
- Don’t infer auth/CSRF requirements in generic middleware/global connection logic. Route/namespace the request to the specific handler, and have that handler enforce what it needs (similar to API endpoint classes).

3) Add regression tests for both positive and negative cases
- Include wrong credentials (e.g., wrong Bearer token / wrong X-API-KEY), missing auth, and unsafe inputs, ensuring tests cover rejections and (where used) constant-time comparisons.

Minimal pattern to follow:
- WS connect/middleware: perform only lightweight checks needed to accept/reject the connection (e.g., origin validation), then delegate authorization to the handler/namespace.
- Auth-protected actions: verify credentials and required headers/claims inside the endpoint, not earlier.
- Validators: implement allowlist regex/logic + parametrized tests for accepted/rejected inputs.

Example (illustrative):
```python
@socketio_server.event
async def connect(sid, environ, _auth):
    with webapp.request_context(environ):
        origin_ok, reason = validate_ws_origin(environ)
        if not origin_ok:
            return False
        return True  # authorization/CSRF requirements enforced by the target handler
```
```python
@pytest.mark.parametrize(
    "url,should_accept",
    [
        ("https://host/org/repo.git", True),
        ("git@host:org/repo.git", True),
        ("ssh://alice@host/org/repo.git", True),
        ("ssh://host/org/repo.git", False),
        ("javascript://host/org/repo.git", False),
    ],
)
def test_url_validation(url, should_accept):
    assert is_valid_clone_url(url) is should_accept
```