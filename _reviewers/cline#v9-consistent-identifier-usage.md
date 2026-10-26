---
title: Consistent Identifier Usage
description: 'Use canonical, shared identifiers across layers (strings, command names,
  and UI assets) so behavior and audits remain consistent.


  Apply this rule:

  1) Normalize naming strings to the downstream contract'
repository: cline/cline#v9
label: Naming Conventions
language: TSX
comments_count: 2
repository_stars: 70868
---

Use canonical, shared identifiers across layers (strings, command names, and UI assets) so behavior and audits remain consistent.

Apply this rule:
1) Normalize naming strings to the downstream contract
- If a runner/inspector normalizes inputs (e.g., trims whitespace), make your registration/menu-path values use the same canonical form.
- Don’t add extra validation/normalization in only one stage if the surrounding system doesn’t do it consistently.

```ts
// Ensure the menu path matches downstream normalization
const normalizedPath = menuPath.trim();
// register/emit using normalizedPath so inspection + execution agree
```

2) Use standardized imports for common UI identifiers
- Prefer the project’s canonical icon/component imports (e.g., from the same Lucide wrapper) instead of ad-hoc inline SVG equivalents, so reviewers can quickly verify icon consistency.

```tsx
// Prefer shared icon import so usage is auditable/consistent
import { X } from 'lucide-react';

<X className="h-4 w-4" aria-hidden="true" />
```

Outcome: consistent identifier usage improves compatibility across tooling boundaries and makes naming/icon choices easy to verify in code.