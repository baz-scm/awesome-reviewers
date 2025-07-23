---
title: Layer documentation by complexity
description: Structure documentation to be approachable for beginners while remaining
  comprehensive for all users. Keep main pages focused on common use cases with simplified
  examples, and move advanced configurations to separate, linked sections. When documenting
  features, start with basic usage before detailing exceptions or edge cases.
repository: continuedev/continue
label: Documentation
language: Other
comments_count: 2
repository_stars: 27819
---

Structure documentation to be approachable for beginners while remaining comprehensive for all users. Keep main pages focused on common use cases with simplified examples, and move advanced configurations to separate, linked sections. When documenting features, start with basic usage before detailing exceptions or edge cases.

For example, instead of including complex configuration options in introductory documentation:
```json
{
  "embeddingsProvider": {
    "provider": "ollama",
    "embeddingPrefixes": [
      // complex configuration...
    ]
  }
}
```

Present a simpler initial example:
```json
{
  "embeddingsProvider": {
    "provider": "ollama",
    "model": "nomic-embed-text"
  }
}
```

With a clear link to advanced configuration options for users who need them. This progressive disclosure approach ensures new users aren't overwhelmed while giving experienced users access to the depth they need.