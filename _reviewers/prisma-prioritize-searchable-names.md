---
title: Prioritize searchable names
description: Choose names that are easily searchable and immediately understandable,
  avoiding unclear abbreviations and symbols that hinder discoverability. Names should
  communicate their purpose clearly without requiring domain knowledge to decode.
repository: prisma/prisma
label: Naming Conventions
language: Yaml
comments_count: 2
repository_stars: 42967
---

Choose names that are easily searchable and immediately understandable, avoiding unclear abbreviations and symbols that hinder discoverability. Names should communicate their purpose clearly without requiring domain knowledge to decode.

Avoid unclear acronyms that aren't established in your codebase - if "DA" isn't used elsewhere, spell out "Driver Adapter". Similarly, avoid symbols like emojis in contexts where searchability matters, as they make it difficult to find and reference specific components.

Example from GitHub workflows:
```yaml
# Avoid - unclear acronym
name: DA Unit Tests [v${{ matrix.node }}]

# Avoid - not searchable
name: 🧪

# Better - clear and searchable
name: Driver Adapter Unit Tests [v${{ matrix.node }}]
name: Tests
```

When space constraints exist, prioritize clarity over brevity. A slightly longer name that clearly communicates purpose is preferable to a short name that requires explanation or context to understand.