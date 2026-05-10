---
title: Treat Jinja2 as Unsafe
description: Don’t trust “sandboxed” templating when any part of template text (or
  dangerous expressions) can be influenced by an untrusted party. For security-sensitive
  code, assume Jinja2 (and similar template engines) is dangerous with untrusted inputs
  and enforce strict trust boundaries.
repository: langchain-ai/langchain
label: Security
language: Markdown
comments_count: 1
repository_stars: 136312
---

Don’t trust “sandboxed” templating when any part of template text (or dangerous expressions) can be influenced by an untrusted party. For security-sensitive code, assume Jinja2 (and similar template engines) is dangerous with untrusted inputs and enforce strict trust boundaries.

Apply this rule:
- Only render templates that are fully controlled by your codebase (allowlisted template sources/IDs), not attacker-provided template strings or files.
- Treat user-supplied data used inside templates as untrusted: escape/quote it for the intended context, and avoid exposing template evaluation features (filters/functions/globals) to untrusted data.
- Don’t rely on “sandboxed” claims in docs/comments as a safety guarantee; instead, implement constraints that ensure untrusted parties cannot provide or influence executable template constructs.

Example (safe pattern: allowlisted templates; user data only as inert values):
```python
from jinja2 import Template

ALLOWED_TEMPLATES = {
    "welcome": "Hello {{ name }}!",
}

def render_welcome(template_id: str, user_name: str) -> str:
    # Block attacker-controlled templates
    if template_id not in ALLOWED_TEMPLATES:
        raise ValueError("Unknown template")

    tmpl = Template(ALLOWED_TEMPLATES[template_id])
    # Treat user_name as inert data; ensure it’s escaped for your output context
    return tmpl.render(name=user_name)
```
If your system needs to accept user-provided templates, require additional hardening and security review rather than assuming Jinja2 sandboxing is sufficient.