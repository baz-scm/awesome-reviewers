---
title: Unicode homoglyph validation
description: Validate Unicode characters and detect potential homoglyph attacks where
  visually similar characters from different scripts could be used maliciously. Avoid
  overly broad patterns that automatically allow non-ASCII characters without proper
  validation, as these can hide security vulnerabilities.
repository: microsoft/terminal
label: Security
language: Txt
comments_count: 1
repository_stars: 99242
---

Validate Unicode characters and detect potential homoglyph attacks where visually similar characters from different scripts could be used maliciously. Avoid overly broad patterns that automatically allow non-ASCII characters without proper validation, as these can hide security vulnerabilities.

When processing text input or configuration patterns, be cautious of Unicode characters that could be used to bypass security measures. For example, a Cyrillic 'а' (U+0430) looks identical to Latin 'a' (U+0061) but could be used to create deceptive URLs, variable names, or bypass filtering rules.

Instead of using broad Unicode acceptance patterns like:
```
[a-zA-Z]*[ÀÁÂÃÄÅÆČÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝßàáâãäåæčçèéêëìíîïðñòóôõöøùúûüýÿ][a-zA-Z]{3}[a-zA-Z]*
```

Consider explicitly allowlisting known legitimate Unicode words or implementing homoglyph detection to identify suspicious character substitutions. This prevents cases where malicious characters like `é` instead of `,` could be hidden by overly permissive patterns, as such substitutions have been used in real-world attacks.