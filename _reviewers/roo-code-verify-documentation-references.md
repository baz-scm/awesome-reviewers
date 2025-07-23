---
title: Verify documentation references
description: Ensure all references in documentation (file paths, commands, code examples)
  actually exist in the codebase and accurately reflect the current system state.
  Additionally, verify that translations maintain correct meaning and grammar in all
  supported languages.
repository: RooCodeInc/Roo-Code
label: Documentation
language: Markdown
comments_count: 2
repository_stars: 17288
---

Ensure all references in documentation (file paths, commands, code examples) actually exist in the codebase and accurately reflect the current system state. Additionally, verify that translations maintain correct meaning and grammar in all supported languages.

Examples:

```bash
# Incorrect - referencing non-existent script
node test-claude-code-integration.js

# Correct - reference actual test command
npm test -- claude-code.spec.ts
```

For translated content:
```
# Incorrect Hindi phrase
हमारी इस डेटा तक पहुंच नहीं है

# Correct Hindi phrase
हमें इस डेटा तक पहुंच नहीं है
```

Before submitting documentation changes, verify all referenced components exist and translations are grammatically correct and contextually accurate. This ensures documentation remains trustworthy and avoids confusion for developers using it as a reference.