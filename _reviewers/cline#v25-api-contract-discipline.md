---
title: API Contract Discipline
description: 'Adopt an “explicit contract + spec gating + scope continuity” standard
  for API integrations.


  Apply these rules:

  1) **Round-trip all request fields through every projection path**'
repository: cline/cline#v25
label: API
language: TypeScript
comments_count: 4
repository_stars: 70891
---

Adopt an “explicit contract + spec gating + scope continuity” standard for API integrations.

Apply these rules:
1) **Round-trip all request fields through every projection path**
   - If an API accepts a field (e.g., `displayPrompt`), it must be preserved when events are copied/translated between subsystems.
2) **Don’t silently change header/field semantics**
   - If you change what `X-Task-ID` represents, either keep the meaning or rename the header / send both values as separate fields. Never rely on the backend inferring a new meaning from the old name.
3) **Follow spec capability/visibility constraints unconditionally**
   - If the spec says a host MUST NOT list tools not visible to `