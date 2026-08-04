---
title: Executable Documentation Accuracy
description: All technical documentation in this repo (stage protocols, stage bodies,
  templates, plugin authoring docs, READMEs that describe operational steps) must
  be mechanically consistent with the actual engine/tools/sensors—and must state conditions
  as explicit, checkable constraints.
repository: awslabs/aidlc-workflows
label: Documentation
language: Markdown
comments_count: 6
repository_stars: 3849
---

All technical documentation in this repo (stage protocols, stage bodies, templates, plugin authoring docs, READMEs that describe operational steps) must be mechanically consistent with the actual engine/tools/sensors—and must state conditions as explicit, checkable constraints.

Apply this checklist before merging doc changes:
1) **Self-consistency vs templates/sensors**: If prose describes a structure (counts/sections/fields), it must match the enforced template/sensor expectations.
2) **No ambiguous placeholders**: Any computed display (e.g., “Progress: [N]/…”) must have a single unambiguous rule for every scope. If different graphs exist, document the selection rule (or the engine picks it) and ensure every example uses the correct denominator.
3) **No contract contradictions**: If a global rule forbids a tool call, stage docs must not instruct the forbidden behavior—unless the doc includes an explicit carve-out naming the stage(s)/step(s) and the exception rationale.
4) **Honor “declared vs evaluated” truth**: For fields that are parsed/validated but not executed (or machine-enforced claims that are not actually enforced), label them explicitly (e.g., “declared-not-evaluated”, “logged-not-enforced”, “unimplemented”) and describe current behavior.
5) **Paths/extensions must match the artifact resolver**: Sensor globs and produced/consumed artifact types must align with the repo’s actual directory shapes and resolver behavior (including .json vs .md or engine-resolved prose paths).
6) **Examples must be safe**: Research-only artifacts or optional steps must be labeled clearly (and if multi-step instructions are error-prone, provide a single script/one-command install flow).

Example (fixing ambiguous progress denominators):
```md
**For enterprise and feature scopes** (graph holds 36 stages; enterprise & feature execute all 32 delivery-path stages):
Progress: [N]/36 overall | [phase-N]/[phase-total] [Phase] stages complete. Next: [Next Stage Name]

[N] numerator rule: plan SKIP rows count in neither numerator nor total; runtime `[S]` skips count in both.
```

Result: a conductor/agent can follow docs literally without nondeterminism, and automated checks (sensors/templates/protocol gates) won’t silently disagree with the written contract.