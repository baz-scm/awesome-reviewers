---
title: Document with examples
description: Always include clear, contextual examples when documenting APIs, interfaces,
  or command-line functionality. Examples significantly improve understanding and
  reduce ambiguity, particularly for new or complex features. Maintain consistent
  terminology throughout documentation, avoiding unexplained jargon or abbreviations.
repository: opentofu/opentofu
label: API
language: Markdown
comments_count: 5
repository_stars: 25901
---

Always include clear, contextual examples when documenting APIs, interfaces, or command-line functionality. Examples significantly improve understanding and reduce ambiguity, particularly for new or complex features. Maintain consistent terminology throughout documentation, avoiding unexplained jargon or abbreviations.

For changelog entries:
```diff
- * Added"force-unlock" support for the HTTP backend: ([#2381](https://github.com/opentofu/opentofu/pull/2381))
+ * "force-unlock" option is now supported by the HTTP backend. ([#2381](https://github.com/opentofu/opentofu/pull/2381))

- * Provider defined functions are now available.  They may be referenced via `provider::alias::funcname(args)`.
+ * Provider defined functions are now available.  They may be referenced via `provider::provider_alias::funcname(args)`. Example: `aws::default::vpc_id(region)`.
```

For API/protocol documentation:
1. Provide examples for common use cases
2. Show exact request/response formats
3. Explain each parameter's purpose and constraints
4. Include links to related concepts for additional context
5. Use consistent terminology when referring to similar concepts (e.g., clarify differences between "plugin" vs "provider")