---
title: Defense-in-depth Security Guardrails
description: 'When handling security-sensitive interactions (authz/ownership, network
  callbacks, and untrusted execution), apply defense-in-depth at the boundaries: be
  precise about guarantees, bind authorization to explicit identities at creation
  time, validate inbound payloads before side effects, and isolate both execution
  and filesystem writes.'
repository: QwenLM/qwen-code
label: Security
language: Markdown
comments_count: 9
repository_stars: 26407
---

When handling security-sensitive interactions (authz/ownership, network callbacks, and untrusted execution), apply defense-in-depth at the boundaries: be precise about guarantees, bind authorization to explicit identities at creation time, validate inbound payloads before side effects, and isolate both execution and filesystem writes.

Practical rules:
1) Don’t overstate bypass behavior
- If a flag relaxes checks, document exactly which checks are skipped vs still enforced, and strongly recommend safe pairing with allowlists.

2) Bind authorization explicitly; require exact-match on callbacks
- At “create” time, store a typed owner key (normalized from the inbound envelope identity).
- At “dispatch” time, compare callback identity to the stored owner key; reject missing/foreign identities without mutating state.

3) Validate callback payload structure against stored state before calling responders
- If you accept indexed answer keys, verify each key maps to a valid index of the stored question array.
- Reject invalid payloads at ingress and do not invoke downstream settlement/responders.

4) Only allow interactive actions for eligible inbound-human turns
- If your “pending prompt” can be produced by unattended producers (loops/webhooks), exclude them from interactive-card eligibility unless you also design an alternate unattended-card contract.

5) Sandbox untrusted code with isolation parity; keep metadata out of the sandbox
- Never execute untrusted PR code in a normal local working copy with access to host credentials.
- Provide metadata as a mounted, read-only file; do not rely on in-sandbox `gh` calls or network calls that require credentials.

6) Never write trusted outputs through untrusted worktrees
- When worktrees can be tampered with (e.g., symlinks), write generated reports to absolute paths rooted in a trusted checkout.
- Restrict untrusted worktree usage to read-only probes.

7) Constrain PR-facing writes to a single authorized path
- Treat PR write capability as an allowlist: one command/path is permitted; everything else (other comment/review/issue edits) must be blocked or enforced by a structural backstop.

Example (callback ingress validation pattern):
```ts
// 1) Owner-only: storedKey was recorded at card creation time.
const ok = normalizeOwner(callback.user) === storedKey;
if (!ok) return failClosed();

// 2) Answer-key defense-in-depth: indices must match stored questions.
const keys = Object.keys(payload.answers ?? {});
const valid = keys.every(k => {
  const i = Number(k);
  return Number.isInteger(i) && i >= 0 && i < storedQuestions.length;
});
if (!valid) return failClosed();

// 3) Only now call the responder/settlement.
await responder({ answers: payload.answers, ...otherFields });
```

Checklist your team can apply to any “interactive callback / bypass flag / untrusted execution” change: (authz binding) + (payload validation) + (eligibility definition) + (sandbox/credential boundaries) + (safe output path policy) + (single allowed write path).