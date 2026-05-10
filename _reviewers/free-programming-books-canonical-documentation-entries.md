---
title: Canonical Documentation Entries
description: When adding or updating documentation entries (e.g., course/resource
  lists), use canonical metadata and URLs so links don’t break, don’t leak tracking,
  and render correctly.
repository: EbookFoundation/free-programming-books
label: Documentation
language: Markdown
comments_count: 47
repository_stars: 388003
---

When adding or updating documentation entries (e.g., course/resource lists), use canonical metadata and URLs so links don’t break, don’t leak tracking, and render correctly.

Apply this checklist:
- Use the exact title from the source (don’t invent/reshape titles).
- Always include the producer/creator/channel/author name where applicable.
- URL rules:
  - No shortened URLs.
  - For YouTube, prefer `www.youtube.com` **playlist** links over single videos.
  - Remove tracking/query params (e.g., `si=...`, `feature=...`, `&t=...`, `&list=...` duplicates when not part of a playlist canonical link).
- Markdown rules:
  - Escape `|` in titles as `\|`.
  - Avoid emojis in titles.
- Keep internal doc structure consistent (headings/anchors/categories/index) so navigation works.

Example (YouTube playlist bullet):
```md
* [React JS Tutorial Series (Kannada)](https://www.youtube.com/playlist?list=<PLAYLIST_ID>) - <Channel/Creator Name>
```
Example (escape pipe):
```md
* [Material UI Complete in One Video \| (Hindi)](https://www.youtube.com/playlist?list=<PLAYLIST_ID>) - <Creator>
```