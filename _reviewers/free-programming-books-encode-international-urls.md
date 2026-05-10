---
title: Encode International URLs
description: When adding or modifying external URLs, ensure international/non-ASCII
  URLs are **percent-encoded** (UTF-8 → percent-encoding). Do not treat “escape” as
  a vague idea—use proper URL encoding so links render correctly across clients and
  avoid malformed/ambiguous URL behavior.
repository: EbookFoundation/free-programming-books
label: Security
language: Markdown
comments_count: 1
repository_stars: 388003
---

When adding or modifying external URLs, ensure international/non-ASCII URLs are **percent-encoded** (UTF-8 → percent-encoding). Do not treat “escape” as a vague idea—use proper URL encoding so links render correctly across clients and avoid malformed/ambiguous URL behavior.

Apply this during link updates:
- Percent-encode international characters in the URL path/query (e.g., Tamil, accented characters).
- Ensure the final URL string is valid and copy-pastable.

Example (conceptual):
```text
Incorrect (not encoded):  http://example.com/புத்தகம்?q=தேர்வு
Correct (encoded):        http://example.com/%E0%AE/....?q=%E0%AE/....
```

If you’re unsure, re-encode the URL using your language/runtime’s URL/URI utilities before committing documentation or code changes.