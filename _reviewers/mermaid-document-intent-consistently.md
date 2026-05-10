---
title: Document intent consistently
description: When code changes affect how people understand or use behavior—especially
  grammar directives/annotations or feature support—add documentation that explains
  intent and keeps docs aligned with current functionality.
repository: mermaid-js/mermaid
label: Documentation
language: Other
comments_count: 2
repository_stars: 87952
---

When code changes affect how people understand or use behavior—especially grammar directives/annotations or feature support—add documentation that explains intent and keeps docs aligned with current functionality.

Apply this in two ways:
1) For non-obvious inline constructs (e.g., grammar annotations), add an immediate “what/why” comment so readers don’t need to infer meaning from implementation.
2) For user-facing feature support changes (e.g., removing directive support in favor of YAML frontmatter), ensure the relevant developer/user documentation is updated (or explicitly tracked via a follow-up PR) so there’s no mismatch between code and guidance.

Example (grammar annotation):
```text
terminal SANKEY_LINK_VALUE returns number: /"(0|[1-9][0-9]*)(\.[0-9]+)?"|.../;
/**
 * @greedy
 * This token should be matched late so it doesn’t preempt other token rules.
 */
@greedy
```