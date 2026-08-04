---
title: Behavior-Correct, Versionless Docs
description: 'Documentation and inline comments should be (1) strictly aligned with
  what the code actually does and (2) resilient to future version bumps.


  Actionable standards:'
repository: awslabs/aidlc-workflows
label: Documentation
language: TypeScript
comments_count: 2
repository_stars: 3849
---

Documentation and inline comments should be (1) strictly aligned with what the code actually does and (2) resilient to future version bumps.

Actionable standards:
1) Scope lifecycle claims to real execution
- When describing merges/copies/invalidation/reconciliation, verify which commands run and what they merge.
- If generated application source is not copied/merged during a lifecycle step, don’t imply it is. Be explicit about what data *is* merged (e.g., “AIDLC state/audit/runtime metadata only”).

2) Avoid hard-coded version strings in shipped prose
- Don’t embed literal strings like “as of 2.2.2” across code/docs/examples unless tests guarantee all instances are updated.
- Prefer versionless phrasing that remains true across re-bumps (e.g., “the framework ships nine discovery defaults”).

3) Keep version artifacts consistent
- When bumping a framework version constant, ensure the corresponding CHANGELOG heading is unique to prevent CI/test failures.

Example (versionless prose)
- Avoid:
  - “As of 2.2.2, the framework ships nine discovery defaults.”
- Prefer:
  - “The framework ships nine discovery defaults.”

Example (behavior-correct comment)
- Avoid implying a lifecycle step merges application source when it doesn’t.
- Prefer wording like:
  - “This step merges AIDLC metadata only; application source is not copied back into the main workspace.”