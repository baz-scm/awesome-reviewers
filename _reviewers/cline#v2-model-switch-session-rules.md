---
title: Model Switch Session Rules
description: When an AI model is changed during an active conversation (or for the
  next turn), code must treat model-dependent inference settings (e.g., context window
  / provider settings) as part of the session state.
repository: cline/cline#v2
label: AI
language: TSX
comments_count: 2
repository_stars: 70861
---

When an AI model is changed during an active conversation (or for the next turn), code must treat model-dependent inference settings (e.g., context window / provider settings) as part of the session state.

Apply this standard:
1) Recompute model-derived settings on every model change
- Derive inference parameters from the new model (e.g., cap `contextWindow` to the model’s `contextLength`) and apply them to the active provider/session configuration.
- Prefer fixing this at the shared SDK/service layer so all clients (desktop/web/cloud) behave consistently.

2) Enforce correct sequencing: update first, then send
- Any time you change the session/model configuration, ensure the system performs:
  - `session.update_connection` (or equivalent) BEFORE `session.send_input`.
- Add/extend tests to lock this ordering in.

3) Respect explicit user selection between turns
- If the product requires explicit user choice (e.g., they selected a particular model between turns), do not “helpfully” auto-correct/rewrite the attached session’s model.

Example (ordering + explicit selection intent):
```ts
// Pseudocode: enforce update-then-send when model changes
async function sendTurn({ session, chosenModel, autoCorrectModel }: {
  session: any;
  chosenModel: string;
  autoCorrectModel: boolean;
}) {
  // If explicit selection is required, don’t override it implicitly
  if (!autoCorrectModel) {
    await session.update_connection({ model: chosenModel, /* recompute contextWindow here */ });
  }

  // Always send only after the update completes
  return session.send_input({ /* user input */ });
}
```

Outcome: prevents stale context-window/provider settings from breaking inference quality (or causing runtime-specific issues) and makes model switching deterministic and testable.