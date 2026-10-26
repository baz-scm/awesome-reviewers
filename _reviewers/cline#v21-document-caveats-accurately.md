---
title: Document Caveats Accurately
description: 'When updating documentation, ensure every statement is either (a) correct
  and actionable, or (b) explicitly labeled as a caveat with clear, practical guidance.
  In practice:'
repository: cline/cline#v21
label: Documentation
language: Other
comments_count: 2
repository_stars: 70886
---

When updating documentation, ensure every statement is either (a) correct and actionable, or (b) explicitly labeled as a caveat with clear, practical guidance. In practice:

- **Never keep “no effect”/obsolete options unmarked.** If a documented setting currently does nothing, either remove the entry or clearly mark it as broken with scope and expected timeline (only if you’ll fix it soon).
- **If behavior varies by provider/platform or has important exceptions, use a consistent “Caveats” callout.** The caveat should answer the user’s practical question (e.g., “which providers run tool processing themselves?”) and point to what the user should expect.
- **Prefer deleting misleading documentation over adding footnotes** when the feature is non-functional and non-core.

Example (doc pattern):

```mdx
> **Caveats**
> - Some model providers run tool processing internally.
> - For those providers, hooks like `PreToolUse`/`PostToolUse` may not execute.
> - Check which provider you’re using and expect different hook behavior.
```

Apply this each time you touch docs: verify the feature actually works as described, and if it doesn’t or varies, label it and guide the user accordingly.