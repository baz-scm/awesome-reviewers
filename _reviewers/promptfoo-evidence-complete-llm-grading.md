---
title: Evidence-complete LLM grading
description: Automated grading and evaluation logic for LLM outputs (redteam graders,
  eval scoring, result interchange) must base pass/fail decisions on all available
  evidence, not on a narrow signal that is convenient to check. Do not shortcut grading
  on an empty or trivial final response text when other signals (e.g. a trace summary
  showing an actual tool call, side...
repository: promptfoo/promptfoo
label: AI
language: TypeScript
comments_count: 6
repository_stars: 26565
---

Automated grading and evaluation logic for LLM outputs (redteam graders, eval scoring, result interchange) must base pass/fail decisions on all available evidence, not on a narrow signal that is convenient to check. Do not shortcut grading on an empty or trivial final response text when other signals (e.g. a trace summary showing an actual tool call, side effect, or policy violation) are present — an empty `llmOutput` should only auto-pass when there is no other evidence of harmful behavior:

```ts
const images = gradingContext?.imageOutputs ?? gradingContext?.providerResponse?.images;
const hasTraceEvidence = Boolean(gradingContext?.traceSummary);
if (isEmptyResponse(llmOutput) && !images?.length && !hasTraceEvidence) {
  return { grade: { pass: true, score: 1, reason: 'Empty response, no other evidence' } };
}
```

Likewise, heuristic/regex-based detectors used ahead of or instead of an LLM judge must be precise enough to avoid both false positives (e.g. a bare `SYSTEM:` label matching ordinary status text) and false negatives; every such pattern needs paired positive and negative regression tests proving it fires only on genuine attack/directive language.

When converting between evaluation formats or persisting grading results (e.g. EvalPort import/export), preserve the original assertion values, config, scores, and named-score keys losslessly rather than re-deriving or approximating them from a transformed shape — round-trip tests should assert that metrics, thresholds, and labels survive exactly. Together, these practices ensure evaluation metrics and security grading remain trustworthy and auditable.