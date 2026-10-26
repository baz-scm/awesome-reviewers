---
title: API Contract Clarity
description: 'When evolving API surfaces, make the contract unambiguous and end-to-end
  consistent.


  Apply these rules:

  - **Spec/gating rules must be applied directly.** If the spec says something must
  never be listed/sent unless it includes a capability (e.g., tool visibility includes
  `"model"`), don’t add exceptions based on unrelated “extension advertised” flags.'
repository: cline/cline#v20
label: API
language: TypeScript
comments_count: 5
repository_stars: 70886
---

When evolving API surfaces, make the contract unambiguous and end-to-end consistent.

Apply these rules:
- **Spec/gating rules must be applied directly.** If the spec says something must never be listed/sent unless it includes a capability (e.g., tool visibility includes `"model"`), don’t add exceptions based on unrelated “extension advertised” flags.
- **Never change the meaning behind an existing identifier without disambiguation.** If a header/field name implies one identifier (e.g., `X-Task-ID`), changing its value to a different identifier (e.g., ulid) is a silent contract break unless you also rename (e.g., `X-Task-ULID`) or send both explicitly.
- **Forward every request/event field through every transformation layer.** If a new field is accepted, ensure all projections/copies and handler conversions preserve it; otherwise it becomes “accepted but dropped”. Add coverage for omitted/empty/present variants.
- **Prefer options objects over boolean parameter packs.** Multi-flag APIs should use named properties so call sites remain self-documenting and flags can’t be swapped.

Example (options object pattern):
```ts
// Prefer:
load({ refresh: true, userInitiated: true })

// Over:
// load(true, true) // unclear at call site

function load(opts: { refresh?: boolean; userInitiated?: boolean } = {}) {
  const { refresh = false, userInitiated = false } = opts;
  // ...
}
```

Example (field forwarding check):
```ts
// If input has displayPrompt, ensure it’s preserved in BOTH event copies
pending_prompt_submitted: ({ input }) => ({
  ...otherFields,
  displayPrompt: input.displayPrompt,
});

// and HubRuntimeHost conversion back out:
function toCoreEvent(envelope) {
  return {
    ...coreEvent,
    displayPrompt: envelope.displayPrompt,
  };
}
```

Finally, ensure behavior stays consistent with the underlying payload contract (e.g., if a tool result is text-only today, don’t allow UI paths that silently queue/drop attachments—make the mismatch explicit).