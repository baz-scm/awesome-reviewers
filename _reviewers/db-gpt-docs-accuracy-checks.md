---
title: Docs accuracy checks
description: When writing documentation in code (comments, docstrings, example snippets),
  ensure every instruction and external link precisely matches the actual package
  extras and the implemented service/provider.
repository: eosphoros-ai/DB-GPT
label: Documentation
language: Python
comments_count: 2
repository_stars: 18703
---

When writing documentation in code (comments, docstrings, example snippets), ensure every instruction and external link precisely matches the actual package extras and the implemented service/provider.

Apply this checklist:
- Installation examples: use the correct `pip` syntax for editable installs and extras, and confirm the package name.
  - Prefer patterns like:
    - `pip install -e ".[openai]"`
    - `pip install "db-gpt[openai]"`
- External API links in comments/docstrings: only keep references that match the real backend/provider. If the code is for Google Gemini, don’t keep ZhiPu-specific API docs—update the link/title or remove it.

Example (corrected install snippet):
```bash
# Install extra support
pip install -e ".[openai]"
# or
pip install "db-gpt[openai]"
```

If you’re unsure which doc/link is correct, verify against the project’s packaging metadata (extras) and the exact provider SDK you’re calling.