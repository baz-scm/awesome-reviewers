---
title: Google-style, concise docstrings
description: All public classes, methods, and functions must use Google-style docstrings
  (Args/Returns/Raises sections), since the API reference generator depends on this
  format. Docstrings should be concise and operational — describing what the code
  does and how to use it — rather than detailing internal design, architecture rationale,
  or marketing-style "Key Features"...
repository: run-llama/llama_index
label: Documentation
language: Python
comments_count: 8
repository_stars: 52785
---

All public classes, methods, and functions must use Google-style docstrings (Args/Returns/Raises sections), since the API reference generator depends on this format. Docstrings should be concise and operational — describing what the code does and how to use it — rather than detailing internal design, architecture rationale, or marketing-style "Key Features" lists; that kind of content belongs in the project README or external docs, not inline. Every parameter, including dynamically accepted `**kwargs` (e.g. a `milvus_partition_names` kwarg forwarded through `**kwargs`), must be documented so callers can discover supported options. Document known limitations or edge cases explicitly (e.g. "only filters top-level dict keys; nested dicts are not recursed into") rather than leaving them implicit. Avoid duplicating lengthy usage examples/instructions in multiple places (module docstring, README, and standalone example files) — keep one canonical source (prefer the README or docs examples folder) and reference it instead of repeating it.

Example:
```python
def process(self, data: dict, **kwargs: Any) -> dict:
    """
    Process input data and apply optional filters.

    Args:
        data (dict): Input payload to process.
        **kwargs: Additional options.
            allowed_fields (Set[str], optional): If provided, only these
                top-level keys are kept in the output. Nested dicts are
                not recursed into.

    Returns:
        dict: The filtered data.

    Raises:
        ValueError: If both allowed_fields and excluded_fields are given.
    """
```
</description>
</invoke>
