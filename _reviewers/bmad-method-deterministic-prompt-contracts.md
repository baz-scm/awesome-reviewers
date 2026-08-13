---
title: Deterministic Prompt Contracts
description: 'Write AI prompt/workflow steps as deterministic contracts: remove ambiguity,
  force required lookups, gate behavior by mode, and make unattended/automation outputs
  schema-correct.'
repository: bmad-code-org/bmad-method
label: AI
language: Markdown
comments_count: 8
repository_stars: 51859
---

Write AI prompt/workflow steps as deterministic contracts: remove ambiguity, force required lookups, gate behavior by mode, and make unattended/automation outputs schema-correct.

Apply these rules:
- **Directive reference loading**: If the step depends on reference files (contracts/guides), explicitly instruct the agent to load them *in order* before deciding anything; don’t rely on the model to “figure out” which files are needed.
- **Mode gating**: Any conversational/side-effect output must be conditional on `{mode}` (e.g., skip greeting in autonomous mode) so the first emitted content is always the artifact or next action.
- **Schema mapping in automation**: When running unattended, explicitly map each schema field to the observable source of truth (files/statuses) rather than “write per schema.”
- **Bounded subagent roles**: Subagents should have constrained responsibilities (e.g., “report findings only”), with the orchestrator doing deduplication, classification, and scoring to avoid inconsistent severity/formatting.
- **Avoid brittle heuristics**: If routing depends on content, instruct semantic reasoning the model can perform (or provide an explicit matching rule); don’t depend on fragile numeric thresholds or placeholder-based routing.

Example pattern:
```md
## Output Contract
- If `{mode}` == `autonomous`, do **not** output conversational text.
- Always load reference docs in this order before step 1:
  1) `references/guide-contract.md`
  2) `references/evidence.md`

## Automation Mode (unattended)
After applying patches:
- Write `$AUTO_DIR/tasks/$TASK_ID/result.json` with:
  - `workflow`: "code-review"
  - `patched`: true iff patch-items were applied on disk
  - `deferred`: list iff deferred-work file append occurred
  - `dismissed`: count set aside to review ledger
  - `clean`: true iff status on disk is `done` and no escalations
```
If you follow the contract rules above, you prevent the common production failures: skipped lookups, wrong behavior in autonomous runs, schema ambiguity, and inconsistent classification across subagents.