---
title: Prioritize descriptive naming
description: Choose clear, self-explanatory names that prioritize readability over
  brevity. Avoid abbreviations, obscure identifiers, and names that require domain
  knowledge to understand. Names should be immediately comprehensible to newcomers
  and future maintainers.
repository: cloudflare/workerd
label: Naming Conventions
language: Other
comments_count: 8
repository_stars: 6989
---

Choose clear, self-explanatory names that prioritize readability over brevity. Avoid abbreviations, obscure identifiers, and names that require domain knowledge to understand. Names should be immediately comprehensible to newcomers and future maintainers.

Key principles:
- Expand abbreviations to full words (e.g., `toNetworkOrderHex()` instead of `toNEHex()`)
- Use semantically meaningful names that describe purpose (e.g., `kjExceptionToJs()` instead of `makeInternalError()`)
- Avoid double negatives in boolean names (e.g., `allowNonObjects` instead of `ignoreNonObjects`)
- Add comments for unavoidably obscure identifiers like `$class` that use special syntax
- Choose familiar terminology over internal jargon (e.g., `typescriptErasableSyntax` over custom terms)

Example:
```cpp
// Poor: Abbreviation unclear to newcomers
kj::String toNEHex() const;

// Better: Full descriptive name
kj::String toNetworkOrderHex() const;

// Poor: Obscure identifier without context
auto actorClass = options.$class->getChannel(ioCtx);

// Better: Add explanatory comment
// $class uses $ prefix to avoid keyword conflicts in JSG API
auto actorClass = options.$class->getChannel(ioCtx);
```

This approach reduces cognitive load, improves code maintainability, and helps onboard new team members more effectively.