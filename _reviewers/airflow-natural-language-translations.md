---
title: Natural language translations
description: When providing translations for user interface elements and documentation,
  prioritize natural and idiomatic expressions in the target language rather than
  literal translations. Consider the grammatical rules and cultural context of each
  language to ensure the translated text sounds native to users.
repository: apache/airflow
label: Documentation
language: Json
comments_count: 2
repository_stars: 40858
---

When providing translations for user interface elements and documentation, prioritize natural and idiomatic expressions in the target language rather than literal translations. Consider the grammatical rules and cultural context of each language to ensure the translated text sounds native to users.

Follow these best practices:
1. Consult with native speakers when possible
2. Use terminology that aligns with how the feature is commonly described in the target language
3. Ensure grammatical correctness specific to the target language
4. Consider context when translating UI components

Example:
```
// Instead of literal translation
"wrap": {
  "tooltip": "Pressione {{hotkey}} para alternar o wrap",
  "unwrap": "Desembrulhar",
  "wrap": "Embrulhar"
}

// Use natural, context-appropriate translation
"wrap": {
  "tooltip": "Pressione {{hotkey}} para expandir ou recolher a secção",
  "unwrap": "Expandir",
  "wrap": "Recolher"
}
```

This approach makes the documentation and UI more intuitive and accessible to international users, improving the overall user experience across different language contexts.