---
title: Use absolute canonical links
description: Documentation (READMEs, guides, markdown pages) is rendered in many different
  contexts—PyPI package pages, the docs website, GitHub—so any link must be a full,
  absolute, and canonical URL rather than a relative path, a local filesystem path,
  or an outdated domain that merely happens to redirect today.
repository: run-llama/llama_index
label: Documentation
language: Markdown
comments_count: 5
repository_stars: 52785
---

Documentation (READMEs, guides, markdown pages) is rendered in many different contexts—PyPI package pages, the docs website, GitHub—so any link must be a full, absolute, and canonical URL rather than a relative path, a local filesystem path, or an outdated domain that merely happens to redirect today.

Before merging documentation changes, verify that:
- No links reference local machine paths (e.g. `/Users/username/Documents/...`); these leak personal file structure and are meaningless to readers. Replace with a real public URL or remove the reference entirely.
- Relative links to examples/notebooks (e.g. `[notebook](../../../docs/examples/...)` or `examples/foo.ipynb`) are converted to full `https://github.com/.../blob/main/...` links, since relative paths break when the README is rendered on PyPI or a website.
- Internal doc-to-doc links use the correct site base path/prefix (e.g. `/python/...` instead of a stale `/docs/...` prefix) and point to an actual existing page, not a directory lacking an index file.
- External/API reference links point to the current canonical domain rather than a legacy domain that only works because of a redirect—redirects can be dropped later and silently break the docs.

Example fix:
```md
<!-- Bad: breaks on PyPI/website, exposes local paths -->
- [Moss Agent Notebook](examples/moss_agent.ipynb)
- n8n implementation: `/Users/pritak/Documents/n8n-nodes-merge`

<!-- Good: absolute, durable, works everywhere -->
- [Moss Agent Notebook](https://github.com/run-llama/llama_index/tree/main/llama-index-integrations/tools/llama-index-tools-moss/examples/moss_agent.ipynb)
```

Treat broken or fragile links as a blocking issue in review, not a nit—confirm the convention against sibling docs and test that the link actually resolves on the live site before approving.</description>
