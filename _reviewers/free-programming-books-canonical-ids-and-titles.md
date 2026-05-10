---
title: Canonical IDs and Titles
description: 'Adopt canonical naming rules for both **identifiers (anchors/ids)**
  and **display names (titles)** to prevent broken links and inconsistent labeling.

  '
repository: EbookFoundation/free-programming-books
label: Naming Conventions
language: Markdown
comments_count: 5
repository_stars: 388003
---

Adopt canonical naming rules for both **identifiers (anchors/ids)** and **display names (titles)** to prevent broken links and inconsistent labeling.

## Rules
1. **Anchor ids must be explicit and stable**
   - If a section/subsection is referenced by an in-page link, ensure there is an explicit matching `id`.
2. **Use consistent casing for ids**
   - Prefer **lowercase ids** (avoid relying on markdown-generated casing differences).
3. **Keep anchor sections ordered predictably**
   - When adding headings/anchors, place them in **alphabetical order** within their group.
4. **Do not invent or paraphrase resource titles**
   - Use the **exact title** provided by the resource/creator.
5. **Avoid honorifics/extra prefixes in names**
   - Don’t add titles like “Professor” or similar honorifics to the listed display name.

## Example (anchor/id)
```md
### <a id="yapay-zeka"></a>Yapay Zeka

<!-- later: link must match the id exactly -->
[Go to Yapay Zeka](#yapay-zeka)
```

## Example (title)
```md
<!-- Good: exact source title -->
* [TypeScript — Frontend & Backend (file setup, types, generics, React + TS)](https://github.com/...)

<!-- Avoid: modified/invented title -->
* [TypeScript Cheatsheet](https://github.com/...)  <!-- only if this is the exact resource title -->
```