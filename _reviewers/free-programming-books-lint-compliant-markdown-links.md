---
title: Lint-Compliant Markdown Links
description: 'When adding/updating entries in markdown lists, follow the repository’s
  lint-safe formatting and platform/link conventions.


  Checklist:

  - Escape special markdown characters in titles/labels: use `\|` instead of `|`.'
repository: EbookFoundation/free-programming-books
label: Code Style
language: Markdown
comments_count: 12
repository_stars: 388003
---

When adding/updating entries in markdown lists, follow the repository’s lint-safe formatting and platform/link conventions.

Checklist:
- Escape special markdown characters in titles/labels: use `\|` instead of `|`.
- Do not add stray Unicode control characters (e.g., RTL marks) to link text.
- Use the resource’s original title—don’t “improve” or invent names just to fit style.
- For YouTube entries, prefer playlist URLs when applicable and include the producer/creator as used elsewhere in the file.
- Keep entry format consistent across files (same `* [Title](URL) - Creator` pattern).
- Avoid emoji and other characters that can break lint/rendering.
- Follow ordering/structure requirements enforced by lint (alphabetical order in the section, correct blank lines, correct header levels).
- Follow URL formatting rules enforced by lint (e.g., remove trailing `/` when required).
- If mixing HTML and markdown, add appropriate spacing/newlines so markdown renders correctly (don’t rely on implicit formatting).

Example (correct pipe escaping):
```md
* [React JS Tutorial in Hindi \| React JS for Beginner to Advanced \| Step by Step Video Tutorials](https://www.youtube.com/playlist?list=PLjVLYmrlmjGdnIQKgnTeR1T9-1ltJEaJh) - WsCubeTech
```

Example (avoid invented titles/ensure lint-safe formatting):
```md
* [.NET Rocks!](https://dotnetrocks.com) - Carl Franklin, Richard Campbell (podcast)
```