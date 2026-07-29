---
title: Boundary Hardening Rules
description: 'Treat every transition from “untrusted / scoped data” into a sensitive
  sink (shell execution, subprocess credentials, HTTP fetch, filesystem writes, and
  API-triggered work) as a security seam. Enforce fail-closed policy at that seam: '
repository: nousresearch/hermes-agent
label: Security
language: Python
comments_count: 15
repository_stars: 221948
---

Treat every transition from “untrusted / scoped data” into a sensitive sink (shell execution, subprocess credentials, HTTP fetch, filesystem writes, and API-triggered work) as a security seam. Enforce fail-closed policy at that seam: 

- **Authenticate/authorize first**: Require `self._check_auth(request)` (or the equivalent gateway dashboard auth middleware) *before* parsing bodies or triggering work; avoid any endpoint that starts actions without the existing auth boundary.
- **Keep secret scope intact**: Never recover from `UnscopedSecretError` by falling back to `os.environ`. Avoid process-global credential aliasing (e.g., setting env vars to influence client construction) unless the subprocess/sanitizer inheritance is explicitly rechecked.
- **Never build shells from user/gateway input**: If you must run a command, prefer list-mode `subprocess.run([...], shell=False, ...)`. If a string command is unavoidable, quote/escape with platform-appropriate shell quoting before any concatenation and add regression tests that include metacharacters like `;` and `|`.
- **Validate SSRF/TOCTOU under redirects**: Preflight URL safety is insufficient when redirects are followed. Re-validate every redirect target/final URL before consuming the response, and ensure the hostname/peer validated is the same one used at connect time.
- **Redact/sanitize outputs**: Don’t publish raw tool results, provider titles/errors, or system-role snippets in API responses/SSE events; apply the existing sanitizer/redaction helpers and add tests.

Example pattern (auth + safe command execution):
```python
async def handler(self, request):
    auth_err = self._check_auth(request)
    if auth_err:
        return auth_err

    body = await request.json()
    user_supplied = str(body.get("command_args", ""))

    # Prefer argv list-mode
    argv = ["some-binary", "--arg", user_supplied]  # no shell
    # subprocess.run(argv, shell=False, check=True, ...)

    return web.json_response({"ok": True})
```

Adopting this “seam-first, fail-closed” standard prevents common regressions: injected shell tokens, secret-scope bypasses, unguarded public triggers, and redirect-based SSRF/TOCTOU.