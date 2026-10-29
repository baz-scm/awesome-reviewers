---
title: Classify and isolate failures
description: 'When a response, stream, or batch item can fail independently, explicitly
  validate it and keep that failure from corrupting unrelated results or silently
  becoming a "pass." Two rules apply broadly:'
repository: promptfoo/promptfoo
label: Error Handling
language: TypeScript
comments_count: 11
repository_stars: 26565
---

When a response, stream, or batch item can fail independently, explicitly validate it and keep that failure from corrupting unrelated results or silently becoming a "pass." Two rules apply broadly:

1. Validate before trusting: never treat an unconfirmed or malformed response as success. Check HTTP status, required fields, and type before using a value (e.g. reject a non-200 or missing-`total_score` response before scoring, reject an empty `classification` unless the provider explicitly confirms `noLabelsDetected`, reject a streamed tool call that never received its arguments). Skipping this check lets `not-x` assertions invert an error into a false pass.

2. Isolate and tag failures at their source: wrap per-item processing (rendering a single template var, serializing one span, exporting one batch) in its own try/catch so one bad item doesn't abort the whole operation — but only suppress the failure when it's truly inconsequential (e.g. an unreferenced template value), and always re-validate types before calling methods like `.trim()` rather than assuming the shape of upstream/SDK data. When an internal grading/execution error does occur, tag it distinctly (e.g. `metadata.graderError`) so downstream code reports it as an infrastructure ERROR rather than an ordinary assertion failure, and so it is never auto-passed by negation.

Example:
```ts
// Bad: assumes success, lets an error become a pass/fail
const resp = await matchesScore(...);
return finalize(resp, assertion, inverse);

// Good: validate first, so negation can't invert a failed call into a pass
if (resp.status !== 200 || typeof resp.total_score !== 'number') {
  return { pass: false, score: 0, reason: `Scoring failed: ${resp.status}`, metadata: { graderError: true } };
}
return finalize(resp, assertion, inverse);
```
Apply this pattern whenever code consumes an external response, a streamed event, or a batch of independent items: confirm it actually succeeded, keep one failure from taking down others, and mark true infrastructure failures so they aren't mistaken for a normal negative result.