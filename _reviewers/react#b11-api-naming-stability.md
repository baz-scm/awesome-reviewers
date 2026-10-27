---
title: API naming stability
description: 'Be deliberate about identifier names—especially for anything exposed
  via exports, typings, devtools labels, or cross-component protocols.


  Standards:

  1) Classify naming scope'
repository: facebook/react#b11
label: Naming Conventions
language: JavaScript
comments_count: 6
repository_stars: 251894
---

Be deliberate about identifier names—especially for anything exposed via exports, typings, devtools labels, or cross-component protocols.

Standards:
1) Classify naming scope
- Public: exported entrypoints/symbols.
- Semi-public: Flow/typing-visible identifiers or names that others must reference.
- Internal: file-local/private helpers.

2) For public/semi-public names
- Follow existing project conventions (e.g. `${ucfirst(methodName)}Options`-style type names).
- Assume rename = breaking change. If you must change names, keep backward compatibility with aliases:

```js
// stable name
export {Activity} from './Activity';
// keep legacy name
export {Activity as unstable_Activity} from './Activity';
```

3) For semantic labels
- Use the most accurate name for the runtime value/role, and prefer the existing naming logic the codebase already uses (avoid inventing inconsistent labels like “fulfilled Thenable {…}” when “Promise” is what users most commonly observe).

4) Prevent naming drift in protocol conversions
- Centralize any naming normalization so the same meaning isn’t re-implemented in many places. Do it once at the source (e.g., normalize by removing a prefix like `top` during the initial mapping) and simplify downstream checks.

5) Match naming patterns to meaning
- Apply established suffix/prefix conventions only when the concept matches the convention (e.g., static-vs-render-specific flag naming should be consistent with how the codebase distinguishes those categories).