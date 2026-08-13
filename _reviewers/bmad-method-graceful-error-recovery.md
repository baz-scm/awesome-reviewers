---
title: Graceful Error Recovery
description: 'Design review/orchestration flows so failures, missing dependencies,
  and partial automation never corrupt state or silently drop work.


  Apply these standards:'
repository: bmad-code-org/bmad-method
label: Error Handling
language: Markdown
comments_count: 5
repository_stars: 51859
---

Design review/orchestration flows so failures, missing dependencies, and partial automation never corrupt state or silently drop work.

Apply these standards:
1) Validate any persisted or resumed state/config before acting.
- If `mode`/settings are invalid, fall back to a safe fresh scan instead of trusting state.
2) Define a structured output contract and validate it before downstream use.
- Persist findings to an artifact (e.g., `review-findings.json`) and require downstream steps to validate required fields/types.
3) Never silently discard “dismissed” or “undecidable” outcomes in auto paths.
- If an automated decision can’t be made unambiguously, set the finding aside with an explicit reason and ensure it is recorded in the ledger/artifact so later cycles don’t re-litigate it.
4) Implement explicit graceful degradation when subsystems are unavailable.
- Don’t stall: choose an inline/sequential fallback appropriate to `{auto_mode}` vs interactive mode.
5) Make side effects and exits precise.
- Only true terminal branches should trigger “exit/on_complete” behavior; non-terminal “display” paths must return control without firing hooks.

Example (state validation + schema contract):
```js
// Validate resume mode
const allowedModes = new Set(['interactive','auto','validate']);
if (!allowedModes.has(resumed.mode)) {
  // Safe recovery
  runFreshScan();
  return;
}

// Validate structured findings before use
const required = ['id','severity','type','summary','detail','file_line','proof'];
function validateFindingSchema(f){
  for (const k of required) if (!(k in f)) throw new Error(`Missing ${k}`);
  return true;
}

const findings = JSON.parse(fs.readFileSync('review-findings.json','utf8'));
findings.forEach(validateFindingSchema);
// proceed knowing the contract holds
```

Net effect: fewer corrupted/looping pipelines, no lost decisions, safer automation, and reliable recovery in the face of missing components or invalid persisted state.