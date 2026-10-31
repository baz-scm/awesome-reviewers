---
title: Sanitize untrusted client input
description: Treat all client-supplied data—HTTP headers (e.g. `Host`), query/path
  parameters, form data—as untrusted, and enforce strict validation or escaping before
  using it in security-sensitive contexts such as generating URLs or rendering HTML.
  Mitigations must be mandatory, correctly scoped, and precisely described rather
  than presented as optional suggestions.
repository: pallets/flask
label: Security
language: Other
comments_count: 4
repository_stars: 75022
---

Treat all client-supplied data—HTTP headers (e.g. `Host`), query/path parameters, form data—as untrusted, and enforce strict validation or escaping before using it in security-sensitive contexts such as generating URLs or rendering HTML. Mitigations must be mandatory, correctly scoped, and precisely described rather than presented as optional suggestions.

For host-derived URLs, Flask always builds external URLs (`url_for(..., _external=True)`) from the request's `Host` header. Don't describe this as a "default" behavior—state clearly that it always happens. To protect against Host header injection, require the global `TRUSTED_HOSTS` configuration (not the per-request `Request.trusted_hosts` attribute, which only overrides the global setting for that request) and document it as something you *must* configure, not something to "consider":

```python
app.config["TRUSTED_HOSTS"] = ["example.com"]
```

For user-controlled values rendered in responses, always escape them to prevent XSS, and keep example code self-contained (including necessary imports):

```python
from markupsafe import escape

@app.route('/user/<username>')
def profile(username):
    return '{}\'s profile'.format(escape(username))
```

When writing security documentation or code, be explicit and directive: state exactly when input is untrusted, which configuration or escaping mechanism actually mitigates the risk, and require its use rather than merely recommending it.</description>
