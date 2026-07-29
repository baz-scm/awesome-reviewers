---
title: Documentation consistency
description: 'Documentation and doc-driven instructions must stay truthful and self-consistent
  with the underlying code and the document’s structure.


  **Apply this checklist when writing or editing docs/specs/templates:**'
repository: QwenLM/qwen-code
label: Documentation
language: Markdown
comments_count: 4
repository_stars: 26407
---

Documentation and doc-driven instructions must stay truthful and self-consistent with the underlying code and the document’s structure.

**Apply this checklist when writing or editing docs/specs/templates:**
1. **Match the real code scope**: if a section claims something is “Correct” or “stored in X,” confirm the referenced symbol/function/path actually exists and is used within the stated directory/runtime.
2. **Avoid stale or positional cross-references**: don’t say “tables above”/“item 7” when the document is reorganized. Prefer stable anchors like section/table names, or update directional wording whenever content moves.
3. **State claims at the right strength**: if a metric only bounds an effect (not isolates it), phrase it as an **upper bound / diagnostic** rather than an estimate of a specific subsystem.
4. **Keep behavior descriptions aligned**: ensure wording about failure modes and side effects matches the implementation (e.g., “fails rather than drops” vs the actual “fails and drops”).
5. **Use concrete evidence** when relevant (function names, file paths, or file:line quotes) so a reader or scan tool can verify the claim.

**Example pattern (robust cross-reference):**
- ❌ “Cite the tables above by name” (breaks after reordering)
- ✅ “Cite **A/B table** and **verdict table** by name” (survives movement)