---
title: Accurate, scoped documentation
description: 'Documentation changes should be accurate, verified, and placed in the
  right location for their audience.


  - Verify behavior before documenting it. Check the actual implementation (e.g.,
  how template/blueprint loader precedence works) rather than guessing, and phrase
  the explanation to match real behavior instead of implying errors or requirements
  that don''t...'
repository: pallets/flask#x
label: Documentation
language: Other
comments_count: 10
repository_stars: 75163
---

Documentation changes should be accurate, verified, and placed in the right location for their audience.

- Verify behavior before documenting it. Check the actual implementation (e.g., how template/blueprint loader precedence works) rather than guessing, and phrase the explanation to match real behavior instead of implying errors or requirements that don't exist. For example, prefer "the first registered blueprint's template takes precedence" over vague wording that implies a conflict error.
- Keep changelog entries (`CHANGES.rst`) limited to changes that affect library users (new features, bug fixes, behavior changes). Documentation-only edits or internal tooling changes should not get a changelog entry.
- Keep tutorials and quickstart guides concise and example-driven; link out to the full API/reference docs for exhaustive details (e.g., full converter lists) instead of duplicating them inline, so the tutorial doesn't become a secondary reference that can drift out of sync.
- Use correct, idiomatic code in examples (e.g., `print('msg')` or `click.echo('msg')` instead of the Python 2 `print` statement) and correct markup/terminology (e.g., double backticks for inline code in reStructuredText, calling `sqlite3.Row` a `namedtuple`-like object rather than just "a tuple").
- When recommending third-party tools or alternatives (e.g., production WSGI servers), stay neutral and generic—mention one example with a note that other options exist, rather than listing/endorsing a curated set that may become outdated or biased.

Applying these checks keeps docs trustworthy, maintainable, and useful to their intended audience.</description>
