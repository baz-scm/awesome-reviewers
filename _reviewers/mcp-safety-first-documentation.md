---
title: Safety-First Documentation
description: Any technical documentation that includes operational steps (especially
  schema changes, data deletion, bucket/table cleanup, or “fix by deleting”) must
  be both safe and unambiguous.
repository: awslabs/mcp
label: Documentation
language: Markdown
comments_count: 7
repository_stars: 9545
---

Any technical documentation that includes operational steps (especially schema changes, data deletion, bucket/table cleanup, or “fix by deleting”) must be both safe and unambiguous.

Apply these rules:
1) **Mark destructive actions as irreversible**
   - If a step deletes data or breaks replication, add an explicit warning like: “⚠️ irreversible — confirm with the user first”.
   - Do not present deletion as a routine equivalent to safe options.

2) **Lead with the safer alternative**
   - For field-type conflicts, prefer non-destructive remediation first (e.g., write to a new field name and update queries).
   - Only mention delete/rewrite as a last resort, behind the irreversibility warning.

3) **Version/edition/protocol correctness checks**
   - Qualify limits and capabilities by **engine version** and **edition** (e.g., Core vs Enterprise table limits).
   - Ensure SQL vs InfluxQL vs Flux guidance doesn’t mix selectors/keywords across query languages.
   - Scope claims like “SQL/Flux supported” to the correct engine version.

4) **Make copy/paste examples substitution-safe**
   - Use a consistent placeholder style and explicitly state what values to substitute (avoid literal placeholders that cause authentication/command failures).

Example pattern for destructive remediation (use as a template in your docs):
```md
Resolution (field type conflicts):
1) Preferred (non-destructive): Write to a new field name (e.g., `temp_f`) and update queries.
2) Last resort (destructive):
   - ⚠️ irreversible — confirm with the user first
   - Delete all data in the table/measurement and rewrite with the correct type.
```

Enforce this with a lightweight doc checklist in PRs: (a) destructive warning present, (b) safer option first, (c) version/edition qualifiers, (d) correct protocol/keywords, (e) examples have explicit substitutions.