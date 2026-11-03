---
title: Declare dependencies in pyproject
description: Any third-party package an integration needs to function must be declared
  in that integration's `pyproject.toml` (as a required dependency, or in an optional
  "extra" group for truly optional features like GPU acceleration or sparse-vector
  support), rather than relying on users to `pip install` it themselves after hitting
  an `ImportError`. Once a package is...
repository: run-llama/llama_index
label: Configurations
language: Python
comments_count: 8
repository_stars: 52785
---

Any third-party package an integration needs to function must be declared in that integration's `pyproject.toml` (as a required dependency, or in an optional "extra" group for truly optional features like GPU acceleration or sparse-vector support), rather than relying on users to `pip install` it themselves after hitting an `ImportError`. Once a package is a declared required dependency, do not wrap its import in `try/except ImportError` or lazy-import it inside functions/constructors "just in case" — import it normally at the top of the module. Lazy-import guards should only be used for packages that are genuinely optional (not listed as required deps), and in that case they should raise a clear, actionable error telling the user exactly what to install, e.g.:

```python
try:
    from transformers import BertTokenizerFast
except ImportError:
    raise ImportError(
        "To use this feature you need `transformers` installed. "
        "Run `pip install transformers`."
    )
```

Also, keep any version constraints consistent between code-level checks and the dependency declaration — if your code enforces `firecrawl-py>=2.0,<3.0`, the same bound must be reflected in `pyproject.toml`/`requirements.txt` (or the redundant file should be removed if unused), so the installed version always matches what the code assumes.