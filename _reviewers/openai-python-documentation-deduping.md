---
title: Documentation Deduping
description: When updating technical docs, avoid duplicating environment-specific
  setup or repeated troubleshooting steps. Prefer linking to the canonical upstream
  documentation for shell/env configuration, and keep only minimal project-specific
  commands (e.g., where you truly provide “permanent activation” instructions). Also
  consolidate identical “fix-it” guidance...
repository: openai/openai-python
label: Documentation
language: Markdown
comments_count: 2
repository_stars: 30731
---

When updating technical docs, avoid duplicating environment-specific setup or repeated troubleshooting steps. Prefer linking to the canonical upstream documentation for shell/env configuration, and keep only minimal project-specific commands (e.g., where you truly provide “permanent activation” instructions). Also consolidate identical “fix-it” guidance into a single canonical section, using cross-links instead of repeating the same snippet.

Example (keep only required project-specific commands, link the rest):
```shell
# Minimal project-specific permanent activation
register-python-argcomplete openai >> ~/.bashrc
register-python-argcomplete openai >> ~/.zshrc

# For other shells or temporary activation, link to upstream docs
# (replace duplicated instruction blocks with the appropriate argcomplete docs link)
```
Example (deduplicate troubleshooting text):
- Instead of repeating an identical “If you see no matches found for … try …” block multiple times, include it once under a dedicated “Troubleshooting” section and link to it from the relevant install sections.