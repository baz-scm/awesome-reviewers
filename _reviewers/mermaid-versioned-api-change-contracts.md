---
title: Versioned API Change Contracts
description: 'When changing a user-facing interface (API/config/grammar or externally
  consumed resources), treat it as a versioned contract:


  1) Classify change severity and reflect it in release artifacts'
repository: mermaid-js/mermaid
label: API
language: Markdown
comments_count: 3
repository_stars: 87952
---

When changing a user-facing interface (API/config/grammar or externally consumed resources), treat it as a versioned contract:

1) Classify change severity and reflect it in release artifacts
- For deprecations: include the “why” (what/which user scenarios are impacted) and what the supported alternative is.
- If you also ship compatibility work (e.g., supporting the new config “whenever possible”), add a separate fix/patch-level entry rather than burying it in the deprecation note.

2) Isolate breaking changes from releases you can’t roll back
- If behavior/grammar is breaking, do not ship additional new syntax in the same release unless you have an explicit, reversible plan.
- Prefer shipping only the currently agreed compatibility surface, and track additional syntax separately.

3) Explicitly version external interface/resource URLs
- For CDN/external loaders used by clients, include a major version (or equivalent) in the URL so updates don’t silently change runtime behavior.

Example patterns:
- Changeset structure (deprecation + patch/fix):
```md
---
'my-feature': patch
---
fix: Support the `htmlLabels` config value whenever possible

---
'my-feature': minor
---
feat: Deprecate `flowchart.htmlLabels` in favor of root-level `htmlLabels`
```
- Staged syntax release (don’t mix breaking syntax):
```text
Release N: ship only `@{ ... }` syntax (no additional simplified grammar)
Release N+1: add simplified syntax under separate ticket/version
```
- Versioned CDN URL:
```js
// Prefer an URL that includes a major version segment
fetch('https://cdn.example.com/mermaid@3/icons/icons.json')
```

Apply this standard to ensure clients get predictable behavior, deprecations are actionable (not vague), and breakage risk is contained through semantic change classification and explicit versioning.