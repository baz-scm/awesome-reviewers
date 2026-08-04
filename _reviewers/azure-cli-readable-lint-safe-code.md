---
title: Readable Lint-Safe Code
description: 'When changing code, prioritize readable structure that also passes linters
  with minimal formatting churn:


  - Keep formatting linter-safe: avoid re-indenting/alignment that triggers flake8
  (e.g., E127). Apply the smallest reformat needed to satisfy style rules.'
repository: Azure/azure-cli
label: Code Style
language: Python
comments_count: 7
repository_stars: 4592
---

When changing code, prioritize readable structure that also passes linters with minimal formatting churn:

- Keep formatting linter-safe: avoid re-indenting/alignment that triggers flake8 (e.g., E127). Apply the smallest reformat needed to satisfy style rules.
- Prefer clear boolean expressions: if a condition is hard to parse, extract named variables (e.g., `has_gateway`, normalized `auth`) so the final `if` is simple.
- Use correct path/OS-safe composition: when iterating directories, join paths using the current directory being walked (e.g., `os.path.join(_dirpath, file)`), not the root.
- Don’t create awkward helper nesting: don’t define a helper inside another function unless it has a clear closure need; otherwise inline it or make it a top-level/helper function.
- Reduce duplication via factoring: when multiple command argument blocks share the same prefix params, define a parent `argument_context(...)` and only specify unique parameters in child contexts.
- Remove unnecessary branching: if two branches differ only by a parameter, consolidate into a single call.

Example (condition simplification):

```python
_normalize_shared_key_fields(namespace)

has_gateway = any([namespace.local_gateway2, namespace.vnet_gateway2])
auth = (getattr(namespace, 'auth_type', '') or '').strip().lower()

if has_gateway and not (namespace.shared_key or auth == 'certificate'):
    ...
```

Example (minimal, linter-safe line formatting):

```python
response_body = _check_runtimestatus_with_deploymentstatusapi(
    cmd, resource_group_name, name, slot,
    deployment_status_url, is_async=True,
    timeout=timeout,
)
```

Example (directory walk correctness):

```python
for _dirpath, _dirnames, files in os.walk(src_path):
    for file in files:
        if fnmatch.fnmatch(file, "*.html"):
            static_html_file = os.path.join(_dirpath, file)
            break
```