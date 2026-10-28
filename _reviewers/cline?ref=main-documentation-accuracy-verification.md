---
title: Documentation accuracy verification
description: 'Documentation must reflect the actual, verified behavior of the product
  — not aspirational, deprecated, or broken behavior. Before publishing or updating
  docs: (1) test every code example and CLI command to confirm it works as written
  (e.g., verify flag ordering like `cline connect telegram --restart -k <TOKEN>` actually
  behaves as documented); (2) if a...'
repository: cline/cline?ref=main
label: Documentation
language: Other
comments_count: 4
repository_stars: 70980
---

Documentation must reflect the actual, verified behavior of the product — not aspirational, deprecated, or broken behavior. Before publishing or updating docs: (1) test every code example and CLI command to confirm it works as written (e.g., verify flag ordering like `cline connect telegram --restart -k <TOKEN>` actually behaves as documented); (2) if a documented feature or config option is broken or has no effect (e.g., an env var that "has no effect in this release"), either fix the underlying product or remove the documentation entirely rather than leaving a stale reference — documenting something that silently does nothing is misleading and erodes trust; (3) when a feature is fully deprecated/unsupported (e.g., `.clineignore` no longer being applied anywhere), delete its documentation rather than keeping a "deprecated soon" notice indefinitely; (4) avoid claiming a reference table or list is exhaustive unless it truly is — instead instruct readers/scripts to gracefully ignore unrecognized values, since new types will be added over time. Only keep a documented caveat for broken functionality when the fix is large, cross-cutting work that can't block the doc update — and in that case, link to the tracking issue and make clear the caveat is temporary.