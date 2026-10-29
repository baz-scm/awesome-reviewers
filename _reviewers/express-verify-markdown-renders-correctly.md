---
title: Verify markdown renders correctly
description: 'When writing or editing markdown documentation (README, History, CONTRIBUTING,
  guides), verify that links, anchors, and references will actually resolve and render
  as intended on GitHub rather than assuming raw text works. Specifically: (1) GitHub
  does not auto-link bare commit hashes or issue/PR numbers, so wrap them in explicit
  markdown links, e.g. ``...'
repository: expressjs/Express
label: Documentation
language: Markdown
comments_count: 4
repository_stars: 69579
---

When writing or editing markdown documentation (README, History, CONTRIBUTING, guides), verify that links, anchors, and references will actually resolve and render as intended on GitHub rather than assuming raw text works. Specifically: (1) GitHub does not auto-link bare commit hashes or issue/PR numbers, so wrap them in explicit markdown links, e.g. `` [`8d09bfe6`](https://github.com/org/repo/commit/8d09bfe6...) ``; (2) GitHub strips special characters like `&` when generating heading anchors, so table-of-contents links must match the generated anchor exactly, e.g. a heading "Docs & Community" produces the anchor `#docs--community`, not `#Docs-&-Community`; (3) wrap GitHub usernames in inline code (backticks) when referencing them in non-link contexts (e.g. `` `@username` ``) to avoid unintentionally pinging/mentioning that person; (4) prefer relative links for in-repo documents (e.g. `Code-Of-Conduct.md`) and ensure links to shared resources (like a Code of Conduct) point to the canonical upstream location rather than a personal fork, updating them if the target file is later relocated. Before merging documentation changes, preview the rendered markdown on GitHub to confirm all links and anchors work as expected.