---
title: Use Approved Naming
description: Use precise, guideline-approved naming for identifiers (tags), technical
  terminology, and headings—so names are unambiguous, consistent, and match the actual
  meaning.
repository: kamranahmedse/developer-roadmap
label: Naming Conventions
language: Markdown
comments_count: 4
repository_stars: 354523
---

Use precise, guideline-approved naming for identifiers (tags), technical terminology, and headings—so names are unambiguous, consistent, and match the actual meaning.

Apply this by:
- Tags/identifiers: Only use tag names that are valid and supported by the project’s contribution guide; don’t invent or repurpose tags. Ensure the tag is appropriate for the resource’s type/category.
- Technical terms: Use terminology that accurately reflects the concept and readers’ expectations (prefer “cache/caches” when the mechanism is caching; avoid unclear synonyms).
- Structural headings/categories: Follow the established naming/format patterns used elsewhere in the repo for section/category titles.

Examples:
- Tag naming (before → after):
  - `[@website@Cursor]` → `[@official@Cursor]` (when the contribution guide/category expects an “official” tag)
- Technical wording:
  - “`useMemo`… memorizes the result” → “`useMemo`… memoizes (i.e., caches) the result” / “caches the result” (only if it’s accurate and clearer to readers)
- Category/heading naming:
  - Don’t introduce one-off heading text that breaks the repo’s established category naming pattern; align with the documented example structure used by similar pages.