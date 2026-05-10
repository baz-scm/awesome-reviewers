---
title: Consistent, clear naming
description: 'Use naming that is unambiguous, consistent with the codebase, and semantically
  accurate.


  Apply:

  - Avoid shadowing: don’t reuse the same parameter name in a nested scope; either
  rename or move the nested function out.'
repository: colinhacks/zod
label: Naming Conventions
language: TypeScript
comments_count: 5
repository_stars: 42628
---

Use naming that is unambiguous, consistent with the codebase, and semantically accurate.

Apply:
- Avoid shadowing: don’t reuse the same parameter name in a nested scope; either rename or move the nested function out.
- Follow established terminology: if the repo uses `*Params*`, don’t introduce `*Opts*` for the same concept (and avoid `opts` vs `params` drift).
- Avoid misleading or shadowy identifiers: don’t use generic built-in-like names (e.g. `toString`) for domain helpers—prefer explicit names (e.g. `errToString`).
- Keep aliases/shortcuts truthful: if an alias suggests transformation but it only adds validation, rename it to reflect intent and/or align with existing API vocabulary.

Example (shadowing + rename):
```ts
function isValidCreditCard(cardNumber: string): boolean {
  const isLuhnAlgo = (sanitizedCardNumber: string): boolean => {
    // ...
    return true;
  };

  return isLuhnAlgo(cardNumber);
}
```

Example (terminology + semantics):
- Prefer `params.async` (not `opts.async`) if the repo’s standard is `Params`.
- Prefer `step` over a confusing alias like `mod` when it’s meant to align with “step” semantics from familiar APIs.