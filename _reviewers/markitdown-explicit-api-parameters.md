---
title: explicit API parameters
description: Make API parameters explicit and named rather than hiding them in **kwargs.
  This improves clarity, enables better validation, and provides clearer interfaces
  for callers.
repository: microsoft/markitdown
label: API
language: Python
comments_count: 4
repository_stars: 76602
---

Make API parameters explicit and named rather than hiding them in **kwargs. This improves clarity, enables better validation, and provides clearer interfaces for callers.

When designing APIs, avoid burying important parameters in generic **kwargs dictionaries. Instead, define them as explicit named parameters with proper types, defaults, and validation. This makes the API more discoverable, self-documenting, and less prone to errors.

For example, instead of:
```python
def convert(self, local_path, **kwargs):
    pdf_engine = kwargs.get("pdf_engine", "pdfminer")
    # Hidden parameter, no validation
```

Use explicit parameters with validation:
```python
def convert(self, local_path, pdf_engine: Literal['pdfminer', 'pymupdf4llm'] = 'pdfminer', **kwargs):
    _engines = {"pdfminer": pdfminer, "pymupdf4llm": pymupdf4llm}
    if pdf_engine not in _engines:
        raise ValueError(f"Invalid pdf_engine. Choose from {list(_engines.keys())}")
```

This approach also supports instance-based configuration where converters can be configured with parameters like API keys, while still maintaining clear method signatures. Avoid hardcoding assumptions (like content types) and instead derive them dynamically from the actual data when possible.