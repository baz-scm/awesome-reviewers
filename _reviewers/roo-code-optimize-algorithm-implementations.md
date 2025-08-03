---
title: Optimize algorithm implementations
description: 'When implementing algorithms, ensure they are both efficient and correct
  across all input cases. Key considerations:


  1. **Pattern matching edge cases**: Ensure regex patterns handle all edge cases,
  including matches at the beginning of strings. For example, replace `/[^\\]`[^`\n]+`/`
  with `/(?:^|[^\\])`[^`\n]+`/` to catch backticks at string start.'
repository: RooCodeInc/Roo-Code
label: Algorithms
language: TypeScript
comments_count: 4
repository_stars: 17288
---

When implementing algorithms, ensure they are both efficient and correct across all input cases. Key considerations:

1. **Pattern matching edge cases**: Ensure regex patterns handle all edge cases, including matches at the beginning of strings. For example, replace `/[^\\]`[^`\n]+`/` with `/(?:^|[^\\])`[^`\n]+`/` to catch backticks at string start.

2. **Algorithmic complexity**: Prevent potential denial-of-service vulnerabilities by analyzing time complexity of algorithms, especially regular expressions on user input. For example, avoid patterns like `/^\[([^\]]*)\]\s*(.*)$/` that can cause performance issues with certain inputs.

3. **False positive prevention**: Configure pattern detection algorithms to avoid false matches. Start pattern searches from length 2 instead of 1 to prevent single repeated elements from being incorrectly identified as patterns:
```typescript
// Instead of:
for (let patternLength = 1; patternLength <= maxPatternLength; patternLength++) {
// Use:
for (let patternLength = 2; patternLength <= maxPatternLength; patternLength++) {
```

4. **Precise matching**: For keyword detection, use word boundaries instead of simple substring matching to improve accuracy:
```typescript
// Instead of:
return keywords.some((keyword) => text.includes(keyword))
// Use:
return keywords.some((keyword) => new RegExp(`\\b${keyword}\\b`).test(text))
```

Following these practices helps create algorithms that are not only computationally efficient but also robust against edge cases and potential security exploits.